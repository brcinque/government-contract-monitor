#!/usr/bin/env python3
"""
Government Contract Monitoring System
Personal use system for tracking federal contracting patterns
"""

import requests
import sqlite3
import pandas as pd
import json
from datetime import datetime, timedelta
import time
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Contract:
    award_id: str
    recipient_name: str
    award_amount: float
    awarding_agency: str
    award_date: str
    award_type: str
    competition_type: str
    description: str

class DatabaseManager:
    def __init__(self, db_path: str = "government_monitor.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Contracts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contracts (
                award_id TEXT PRIMARY KEY,
                recipient_name TEXT,
                award_amount REAL,
                awarding_agency TEXT,
                award_date TEXT,
                award_type TEXT,
                competition_type TEXT,
                description TEXT,
                collected_date TEXT
            )
        ''')
        
        # Company tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS company_tracking (
                company_name TEXT,
                total_contracts INTEGER,
                total_amount REAL,
                first_contract_date TEXT,
                last_contract_date TEXT,
                no_bid_contracts INTEGER,
                emergency_contracts INTEGER,
                PRIMARY KEY (company_name)
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alert_type TEXT,
                message TEXT,
                data TEXT,
                created_date TEXT,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_contracts(self, contracts: List[Contract]):
        """Save contracts to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for contract in contracts:
            cursor.execute('''
                INSERT OR REPLACE INTO contracts 
                (award_id, recipient_name, award_amount, awarding_agency, 
                 award_date, award_type, competition_type, description, collected_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                contract.award_id, contract.recipient_name, contract.award_amount,
                contract.awarding_agency, contract.award_date, contract.award_type,
                contract.competition_type, contract.description, datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def get_company_summary(self, company_name: str) -> Dict:
        """Get summary statistics for a specific company"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_contracts,
                SUM(award_amount) as total_amount,
                MIN(award_date) as first_contract,
                MAX(award_date) as last_contract,
                COUNT(CASE WHEN competition_type LIKE '%no%bid%' THEN 1 END) as no_bid_count
            FROM contracts 
            WHERE recipient_name LIKE ?
        ''', (f'%{company_name}%',))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'company': company_name,
            'total_contracts': result[0],
            'total_amount': result[1] or 0,
            'first_contract': result[2],
            'last_contract': result[3],
            'no_bid_contracts': result[4]
        }

class USASpendingCollector:
    def __init__(self):
        self.base_url = "https://api.usaspending.gov/api/v2/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Government-Monitor/1.0'
        })
    
    def collect_recent_contracts(self, days_back: int = 7) -> List[Contract]:
        """Collect contracts from last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        url = f"{self.base_url}search/spending_by_award/"
        
        payload = {
            "filters": {
                "time_period": [{
                    "start_date": start_date.strftime('%Y-%m-%d'),
                    "end_date": end_date.strftime('%Y-%m-%d')
                }],
                "award_type_codes": ["A", "B", "C", "D"],  # Contract types
                "award_amounts": [{"lower_bound": 1000000}]  # Only contracts > $1M
            },
            "fields": [
                "Award ID", "Recipient Name", "Award Amount", 
                "Awarding Agency", "Start Date", "Award Type",
                "Contract Award Type", "Description"
            ],
            "page": 1,
            "limit": 100
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            contracts = []
            
            for item in data.get('results', []):
                contract = Contract(
                    award_id=item.get('Award ID', ''),
                    recipient_name=item.get('Recipient Name', ''),
                    award_amount=float(item.get('Award Amount', 0)),
                    awarding_agency=item.get('Awarding Agency', ''),
                    award_date=item.get('Start Date', ''),
                    award_type=item.get('Award Type', ''),
                    competition_type=item.get('Contract Award Type', ''),
                    description=item.get('Description', '')
                )
                contracts.append(contract)
            
            logger.info(f"Collected {len(contracts)} contracts from USASpending.gov")
            return contracts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error collecting from USASpending.gov: {e}")
            return []

class PatternAnalyzer:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def detect_rapid_accumulation(self, days: int = 30, min_contracts: int = 3) -> List[Dict]:
        """Detect companies getting multiple contracts quickly"""
        conn = sqlite3.connect(self.db.db_path)
        
        query = '''
            SELECT recipient_name, 
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount,
                   MIN(award_date) as first_date,
                   MAX(award_date) as last_date
            FROM contracts 
            WHERE award_date >= date('now', '-{} days')
            GROUP BY recipient_name
            HAVING COUNT(*) >= {}
            ORDER BY contract_count DESC, total_amount DESC
        '''.format(days, min_contracts)
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        alerts = []
        for _, row in df.iterrows():
            alerts.append({
                'type': 'rapid_accumulation',
                'company': row['recipient_name'],
                'contract_count': row['contract_count'],
                'total_amount': row['total_amount'],
                'time_span_days': days,
                'severity': 'high' if row['contract_count'] >= 5 else 'medium'
            })
        
        return alerts
    
    def detect_no_bid_patterns(self, min_amount: float = 10_000_000) -> List[Dict]:
        """Detect large no-bid contracts"""
        conn = sqlite3.connect(self.db.db_path)
        
        query = '''
            SELECT recipient_name, award_amount, awarding_agency, 
                   award_date, competition_type, description
            FROM contracts 
            WHERE (competition_type LIKE '%sole%source%' 
                   OR competition_type LIKE '%no%bid%'
                   OR competition_type LIKE '%not%competed%')
              AND award_amount >= ?
              AND award_date >= date('now', '-30 days')
            ORDER BY award_amount DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=[min_amount])
        conn.close()
        
        alerts = []
        for _, row in df.iterrows():
            alerts.append({
                'type': 'large_no_bid',
                'company': row['recipient_name'],
                'amount': row['award_amount'],
                'agency': row['awarding_agency'],
                'date': row['award_date'],
                'competition_type': row['competition_type'],
                'severity': 'high' if row['award_amount'] >= 50_000_000 else 'medium'
            })
        
        return alerts
    
    def analyze_trends(self) -> Dict:
        """Analyze overall trends in contracting"""
        conn = sqlite3.connect(self.db.db_path)
        
        # Total spending trends
        monthly_spending = pd.read_sql_query('''
            SELECT DATE(award_date, 'start of month') as month,
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount
            FROM contracts 
            WHERE award_date >= date('now', '-12 months')
            GROUP BY month
            ORDER BY month
        ''', conn)
        
        # Top contractors by amount
        top_contractors = pd.read_sql_query('''
            SELECT recipient_name,
                   COUNT(*) as contract_count,
                   SUM(award_amount) as total_amount
            FROM contracts 
            WHERE award_date >= date('now', '-90 days')
            GROUP BY recipient_name
            ORDER BY total_amount DESC
            LIMIT 20
        ''', conn)
        
        # No-bid ratio trends
        no_bid_ratio = pd.read_sql_query('''
            SELECT DATE(award_date, 'start of month') as month,
                   COUNT(*) as total_contracts,
                   COUNT(CASE WHEN competition_type LIKE '%sole%source%' 
                              OR competition_type LIKE '%no%bid%' 
                              THEN 1 END) as no_bid_contracts
            FROM contracts 
            WHERE award_date >= date('now', '-12 months')
            GROUP BY month
            ORDER BY month
        ''', conn)
        
        conn.close()
        
        return {
            'monthly_spending': monthly_spending.to_dict('records'),
            'top_contractors': top_contractors.to_dict('records'),
            'no_bid_trends': no_bid_ratio.to_dict('records')
        }

class AlertManager:
    def __init__(self, db_manager: DatabaseManager, email_config: Optional[Dict] = None):
        self.db = db_manager
        self.email_config = email_config
    
    def process_alerts(self, alerts: List[Dict]):
        """Process and store alerts"""
        if not alerts:
            return
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        for alert in alerts:
            cursor.execute('''
                INSERT INTO alerts (alert_type, message, data, created_date)
                VALUES (?, ?, ?, ?)
            ''', (
                alert['type'],
                self._format_alert_message(alert),
                json.dumps(alert),
                datetime.now().isoformat()
            ))
            
            logger.warning(f"ALERT: {alert['type']} - {self._format_alert_message(alert)}")
        
        conn.commit()
        conn.close()
        
        # Send email if configured
        if self.email_config and alerts:
            self._send_email_alerts(alerts)
    
    def _format_alert_message(self, alert: Dict) -> str:
        """Format alert for display"""
        if alert['type'] == 'rapid_accumulation':
            return f"{alert['company']} received {alert['contract_count']} contracts worth ${alert['total_amount']:,.0f} in {alert['time_span_days']} days"
        elif alert['type'] == 'large_no_bid':
            return f"{alert['company']} received ${alert['amount']:,.0f} no-bid contract from {alert['agency']}"
        else:
            return f"Unknown alert type: {alert}"
    
    def _send_email_alerts(self, alerts: List[Dict]):
        """Send email notifications for alerts"""
        if not self.email_config:
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = self.email_config['to_email']
            msg['Subject'] = f"Government Contract Alerts - {len(alerts)} new alerts"
            
            body = "New government contracting alerts:\n\n"
            for alert in alerts:
                body += f"• {self._format_alert_message(alert)}\n"
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Sent email alert with {len(alerts)} alerts")
            
        except Exception as e:
            logger.error(f"Failed to send email alerts: {e}")

class GovernmentMonitor:
    def __init__(self, email_config: Optional[Dict] = None):
        self.db = DatabaseManager()
        self.collector = USASpendingCollector()
        self.analyzer = PatternAnalyzer(self.db)
        self.alert_manager = AlertManager(self.db, email_config)
    
    def run_daily_collection(self):
        """Main daily collection and analysis routine"""
        logger.info("Starting daily government contract collection...")
        
        # Collect new contracts
        contracts = self.collector.collect_recent_contracts(days_back=1)
        if contracts:
            self.db.save_contracts(contracts)
        
        # Run pattern analysis
        rapid_alerts = self.analyzer.detect_rapid_accumulation()
        no_bid_alerts = self.analyzer.detect_no_bid_patterns()
        
        # Process alerts
        all_alerts = rapid_alerts + no_bid_alerts
        self.alert_manager.process_alerts(all_alerts)
        
        # Generate summary
        trends = self.analyzer.analyze_trends()
        logger.info(f"Collection complete. Found {len(all_alerts)} new alerts.")
        
        return {
            'contracts_collected': len(contracts),
            'alerts_generated': len(all_alerts),
            'trends': trends
        }
    
    def get_company_report(self, company_name: str) -> Dict:
        """Generate detailed report for specific company"""
        summary = self.db.get_company_summary(company_name)
        
        # Get recent contracts
        conn = sqlite3.connect(self.db.db_path)
        recent_contracts = pd.read_sql_query('''
            SELECT award_id, award_amount, awarding_agency, 
                   award_date, competition_type, description
            FROM contracts 
            WHERE recipient_name LIKE ?
              AND award_date >= date('now', '-90 days')
            ORDER BY award_date DESC
        ''', conn, params=[f'%{company_name}%'])
        conn.close()
        
        return {
            'summary': summary,
            'recent_contracts': recent_contracts.to_dict('records')
        }

def main():
    """Example usage"""
    
    # Optional email configuration
    email_config = {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'your-email@gmail.com',
        'password': 'your-app-password',
        'from_email': 'your-email@gmail.com',
        'to_email': 'your-email@gmail.com'
    }
    
    # Initialize monitor (remove email_config if you don't want email alerts)
    monitor = GovernmentMonitor()  # or GovernmentMonitor(email_config)
    
    # Run daily collection
    results = monitor.run_daily_collection()
    print(f"Results: {results}")
    
    # Get report for specific company
    # company_report = monitor.get_company_report("Palantir")
    # print(json.dumps(company_report, indent=2))

if __name__ == "__main__":
    main()
