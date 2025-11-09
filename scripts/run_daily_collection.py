#!/usr/bin/env python3
"""
Daily collection script - run this daily to collect new contract data
"""

from government_monitor_system import GovernmentMonitor
from datetime import datetime

def main():
    print(f"=== Government Contract Monitor - Daily Collection ===")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize monitor (no email alerts for now)
    monitor = GovernmentMonitor()
    
    # Run daily collection
    try:
        results = monitor.run_daily_collection()
        
        print(f"\n✅ Collection Complete:")
        print(f"   📄 Contracts collected: {results['contracts_collected']}")
        print(f"   🚨 Alerts generated: {results['alerts_generated']}")
        print(f"   📊 Database updated successfully")
        
        if results['alerts_generated'] > 0:
            print(f"\n⚠️  New alerts detected! Check the dashboard for details.")
            
    except Exception as e:
        print(f"\n❌ Collection failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
