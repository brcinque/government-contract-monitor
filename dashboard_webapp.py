#!/usr/bin/env python3
"""
Simple Flask web dashboard for Government Contract Monitor
Run this to get a web interface for your monitoring data
"""

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

app = Flask(__name__)

class DashboardData:
    def __init__(self, db_path: str = "government_monitor.db"):
        self.db_path = db_path
    
    def get_summary_stats(self):
        """Get high-level summary statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total contracts and spending
        cursor.execute('''
            SELECT COUNT(*) as total_contracts,
                   SUM(award_amount) as total_spending,
                   COUNT(DISTINCT recipient_name) as unique_companies
            FROM contracts
        ''')
        totals = cursor.fetchone()
        
        # Recent activity (last 30 days)
        cursor.execute('''
            SELECT COUNT(*) as recent_contracts,
                   SUM(award_amount) as recent_spending
            FROM contracts 
            WHERE award_date >= date('now', '-30 days')
        ''')
        recent = cursor.fetchone()
        
        # No-bid contracts percentage
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN competition_type LIKE '%sole%source%' 
                           OR competition_type LIKE '%no%bid%' 
                           OR competition_type LIKE '%not%competed%'
                           THEN 1 END) as no_bid_count,
                COUNT(*) as total_count
            FROM contracts 
            WHERE award_date >= date('now', '-30 days')
        ''')
        competition = cursor.fetchone()
        
        conn.close()
        
        no_bid_percentage = (competition[0] / competition[1] * 100) if competition[1] > 0 else 0
        
        return {
            'total_contracts': totals[0],
            'total_spending': totals[1] or 0,
            'unique_companies': totals[2],
            'recent_contracts': recent[0],
            'recent_spending': recent[1] or 0,
            'no_bid_percentage': round(no_bid_percentage, 1)
        }
    
    def get_spending_trends(self):
        """Get monthly spending trends"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('''
            SELECT DATE(award_date, 'start of month') as month,
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount,
                   COUNT(CASE WHEN competition_type LIKE '%sole%source%' 
                              OR competition_type LIKE '%no%bid%' 
                              THEN 1 END) as no_bid_count
            FROM contracts 
            WHERE award_date >= date('now', '-12 months')
            GROUP BY month
            ORDER BY month
        ''', conn)
        conn.close()
        
        return df.to_dict('records')
    
    def get_top_contractors(self, days=90, limit=15):
        """Get top contractors by spending"""
        conn = sqlite3.connect(self.db_path)
        
        # First try last 90 days, if no data, expand to all data
        df = pd.read_sql_query('''
            SELECT recipient_name,
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount,
                   AVG(award_amount) as avg_amount
            FROM contracts 
            WHERE award_date >= date('now', '-{} days')
            GROUP BY recipient_name
            ORDER BY total_amount DESC
            LIMIT {}
        '''.format(days, limit), conn)
        
        # Always show all-time data since most contracts are historical
        df = pd.read_sql_query('''
            SELECT recipient_name,
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount,
                   AVG(award_amount) as avg_amount
            FROM contracts 
            GROUP BY recipient_name
            ORDER BY total_amount DESC
            LIMIT {}
        '''.format(limit), conn)
        
        conn.close()
        return df.to_dict('records')
    
    def get_recent_alerts(self, limit=20):
        """Get recent alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT alert_type, message, created_date, data
            FROM alerts 
            ORDER BY created_date DESC 
            LIMIT ?
        ''', (limit,))
        
        alerts = []
        for row in cursor.fetchall():
            alert_data = json.loads(row[3]) if row[3] else {}
            alerts.append({
                'type': row[0],
                'message': row[1],
                'date': row[2],
                'severity': alert_data.get('severity', 'medium')
            })
        
        conn.close()
        return alerts
    
    def get_agency_breakdown(self):
        """Get spending breakdown by agency"""
        conn = sqlite3.connect(self.db_path)
        
        # First try last 90 days, if no data, expand to all data
        df = pd.read_sql_query('''
            SELECT awarding_agency,
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount
            FROM contracts 
            WHERE award_date >= date('now', '-90 days')
            GROUP BY awarding_agency
            ORDER BY total_amount DESC
            LIMIT 10
        ''', conn)
        
        # Always show all-time data since most contracts are historical  
        df = pd.read_sql_query('''
            SELECT awarding_agency,
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount
            FROM contracts 
            GROUP BY awarding_agency
            ORDER BY total_amount DESC
            LIMIT 10
        ''', conn)
        
        conn.close()
        return df.to_dict('records')

dashboard_data = DashboardData()

# HTML Template for the dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Government Contract Monitor</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
        .stat-number { font-size: 2em; font-weight: bold; color: #333; }
        .stat-label { color: #666; margin-top: 5px; }
        .chart-container { background: white; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .alerts { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .alert-item { padding: 10px; border-left: 4px solid #ff6b6b; margin: 10px 0; background: #fff5f5; }
        .alert-high { border-color: #ff6b6b; background: #fff5f5; }
        .alert-medium { border-color: #ffa726; background: #fff8e1; }
        .alert-low { border-color: #66bb6a; background: #f1f8e9; }
        .table { width: 100%; border-collapse: collapse; }
        .table th, .table td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        .table th { background-color: #f8f9fa; }
        .refresh-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Government Contract Monitor</h1>
            <p>Real-time tracking of federal contracting patterns</p>
            <button class="refresh-btn" onclick="location.reload()">Refresh Data</button>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_contracts }}</div>
                <div class="stat-label">Total Contracts</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${{ "%.1f"|format(stats.total_spending/1000000000) }}B</div>
                <div class="stat-label">Total Spending</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.unique_companies }}</div>
                <div class="stat-label">Unique Companies</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.recent_contracts }}</div>
                <div class="stat-label">Recent Contracts (30d)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${{ "%.1f"|format(stats.recent_spending/1000000) }}M</div>
                <div class="stat-label">Recent Spending (30d)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ stats.no_bid_percentage }}%</div>
                <div class="stat-label">No-Bid Contracts (30d)</div>
            </div>
        </div>
        
        <div class="chart-container">
            <h3>Monthly Spending Trends</h3>
            <div id="spending-chart"></div>
        </div>
        
        <div class="chart-container">
            <h3>Top Contractors (All-Time Data)</h3>
            <div id="contractors-chart"></div>
        </div>
        
        <div class="chart-container">
            <h3>Agency Spending Breakdown (All-Time Data)</h3>
            <div id="agency-chart"></div>
        </div>
        
        <div class="alerts">
            <h3>Recent Alerts</h3>
            {% for alert in alerts %}
            <div class="alert-item alert-{{ alert.severity }}">
                <strong>{{ alert.type.replace('_', ' ').title() }}:</strong> {{ alert.message }}
                <small style="float: right;">{{ alert.date.split('T')[0] }}</small>
            </div>
            {% endfor %}
        </div>
    </div>
    
    <script>
        // Spending trends chart
        var spendingData = {{ spending_trends | safe }};
        var spendingTrace = {
            x: spendingData.map(d => d.month),
            y: spendingData.map(d => d.total_amount / 1000000),
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Monthly Spending ($M)',
            line: {color: '#007bff'}
        };
        var spendingLayout = {
            title: '',
            xaxis: {title: 'Month'},
            yaxis: {title: 'Spending (Millions $)'},
            showlegend: false
        };
        Plotly.newPlot('spending-chart', [spendingTrace], spendingLayout);
        
        // Top contractors chart
        var contractorsData = {{ top_contractors | safe }};
        var contractorsTrace = {
            x: contractorsData.map(d => d.total_amount / 1000000),
            y: contractorsData.map(d => d.recipient_name.substring(0, 30)),
            type: 'bar',
            orientation: 'h',
            marker: {color: '#28a745'}
        };
        var contractorsLayout = {
            title: '',
            xaxis: {title: 'Total Amount (Millions $)'},
            yaxis: {title: ''},
            margin: {l: 200}
        };
        Plotly.newPlot('contractors-chart', [contractorsTrace], contractorsLayout);
        
        // Agency breakdown chart
        var agencyData = {{ agency_breakdown | safe }};
        var agencyTrace = {
            labels: agencyData.map(d => d.awarding_agency.substring(0, 20)),
            values: agencyData.map(d => d.total_amount),
            type: 'pie'
        };
        var agencyLayout = {
            title: ''
        };
        Plotly.newPlot('agency-chart', [agencyTrace], agencyLayout);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    stats = dashboard_data.get_summary_stats()
    spending_trends = dashboard_data.get_spending_trends()
    top_contractors = dashboard_data.get_top_contractors()
    alerts = dashboard_data.get_recent_alerts()
    agency_breakdown = dashboard_data.get_agency_breakdown()
    
    return render_template_string(
        DASHBOARD_HTML,
        stats=stats,
        spending_trends=json.dumps(spending_trends),
        top_contractors=json.dumps(top_contractors),
        alerts=alerts,
        agency_breakdown=json.dumps(agency_breakdown)
    )

@app.route('/api/company/<company_name>')
def company_api(company_name):
    """API endpoint for company-specific data"""
    conn = sqlite3.connect(dashboard_data.db_path)
    
    # Company summary
    summary_query = '''
        SELECT 
            COUNT(*) as total_contracts,
            SUM(award_amount) as total_amount,
            MIN(award_date) as first_contract,
            MAX(award_date) as last_contract,
            COUNT(CASE WHEN competition_type LIKE '%no%bid%' 
                       OR competition_type LIKE '%sole%source%' 
                       THEN 1 END) as no_bid_count
        FROM contracts 
        WHERE recipient_name LIKE ?
    '''
    
    cursor = conn.cursor()
    cursor.execute(summary_query, (f'%{company_name}%',))
    summary = cursor.fetchone()
    
    # Recent contracts
    recent_query = '''
        SELECT award_id, award_amount, awarding_agency, award_date, competition_type
        FROM contracts 
        WHERE recipient_name LIKE ?
          AND award_date >= date('now', '-90 days')
        ORDER BY award_date DESC
        LIMIT 20
    '''
    
    df = pd.read_sql_query(recent_query, conn, params=[f'%{company_name}%'])
    conn.close()
    
    return jsonify({
        'company': company_name,
        'summary': {
            'total_contracts': summary[0],
            'total_amount': summary[1] or 0,
            'first_contract': summary[2],
            'last_contract': summary[3],
            'no_bid_contracts': summary[4]
        },
        'recent_contracts': df.to_dict('records')
    })

@app.route('/api/alerts')
def alerts_api():
    """API endpoint for recent alerts"""
    alerts = dashboard_data.get_recent_alerts()
    return jsonify(alerts)

@app.route('/api/trends')
def trends_api():
    """API endpoint for trend data"""
    return jsonify({
        'spending_trends': dashboard_data.get_spending_trends(),
        'top_contractors': dashboard_data.get_top_contractors(),
        'agency_breakdown': dashboard_data.get_agency_breakdown()
    })

if __name__ == '__main__':
    print("📊 Government Contract Dashboard")
    print("=" * 35)
    print("Dashboard URL: http://127.0.0.1:8080")
    print("Press Ctrl+C to stop the server")
    print()
    app.run(debug=False, host='127.0.0.1', port=8080)