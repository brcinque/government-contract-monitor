#!/usr/bin/env python3
"""
Government Contract Monitor - Main Interface
Streamlined cronyism detection system
"""

import sys
import os
from datetime import datetime

# Add core directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from comprehensive_collector import UltimateGovernmentMonitor
from scenario_monitoring import ScenarioMonitor

def main():
    """Main interface for government contract monitoring"""
    print("🔍 GOVERNMENT CONTRACT MONITOR")
    print("=" * 50)
    print("Choose monitoring mode:")
    print("  1. Full Cronyism Detection (Recommended)")
    print("  2. Data Collection Only") 
    print("  3. Dashboard Only")
    print("  4. Quick Status Check")
    print()
    
    try:
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == "1":
            run_cronyism_detection()
        elif choice == "2":
            run_data_collection()
        elif choice == "3":
            run_dashboard()
        elif choice == "4":
            show_status()
        else:
            print("Invalid choice. Running cronyism detection...")
            run_cronyism_detection()
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

def run_cronyism_detection():
    """Run full cronyism detection"""
    print("\n🚨 CRONYISM DETECTION MODE")
    print("-" * 30)
    
    # Data collection
    print("📊 Collecting data from all sources...")
    monitor = UltimateGovernmentMonitor()
    results = monitor.run_ultimate_collection(days_back=30)
    
    # Scenario analysis
    print("🔍 Analyzing for corruption patterns...")
    scenario_monitor = ScenarioMonitor()
    scenarios = scenario_monitor.run_full_scenario_analysis()
    
    # Results
    total_alerts = sum(len(alerts) for alerts in scenarios.values())
    
    print(f"\n✅ ANALYSIS COMPLETE")
    print(f"   New contracts: {results.get('new_contracts_saved', 0)}")
    print(f"   Alerts generated: {total_alerts}")
    
    if total_alerts > 0:
        print(f"\n🚨 ALERTS DETECTED - Review recommended")
        report = scenario_monitor.generate_scenario_report()
        print(report)
    else:
        print(f"\n✅ No concerning patterns detected")
    
    print(f"\n📊 View dashboard: http://127.0.0.1:8080")

def run_data_collection():
    """Run data collection only"""
    print("\n📊 DATA COLLECTION MODE")
    print("-" * 25)
    
    monitor = UltimateGovernmentMonitor()
    results = monitor.run_ultimate_collection(days_back=7)
    
    print(f"\n✅ Collection complete:")
    print(f"   New contracts: {results.get('new_contracts_saved', 0)}")
    print(f"   Database total: {results.get('unique_contracts', 0)}")

def run_dashboard():
    """Launch dashboard"""
    print("\n📊 DASHBOARD MODE")
    print("-" * 17)
    print("Starting web dashboard...")
    
    import subprocess
    import webbrowser
    import time
    import threading
    
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://127.0.0.1:8080')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Import and run dashboard
    from dashboard_webapp import app
    print("Dashboard available at: http://127.0.0.1:8080")
    print("Press Ctrl+C to stop")
    app.run(host='127.0.0.1', port=8080, debug=False)

def show_status():
    """Show quick system status"""
    print("\n📊 SYSTEM STATUS")
    print("-" * 15)
    
    import sqlite3
    try:
        conn = sqlite3.connect('government_monitor.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM contracts')
        total_contracts = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(award_amount) FROM contracts')
        total_value = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT MAX(award_date) FROM contracts')
        latest_date = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts')
        total_alerts = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"📄 Contracts: {total_contracts:,}")
        print(f"💰 Total Value: ${total_value:,.0f}")
        print(f"📅 Latest Contract: {latest_date}")
        print(f"🚨 Total Alerts: {total_alerts}")
        print(f"✅ System operational")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    exit(main())
