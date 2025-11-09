#!/usr/bin/env python3
"""
Ultimate Collection Script - Maximum Government Contract Data Collection
Runs ALL available collectors for comprehensive contract discovery
"""

from comprehensive_collector import UltimateGovernmentMonitor
from datetime import datetime
import sys

def main():
    """Main ultimate collection function"""
    print("🚀 ULTIMATE Government Contract Collection")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("📊 Data Sources:")
    print("   ✅ USASpending.gov Enhanced - Multiple query strategies")
    print("   ✅ DoD Contract Scraper - defense.gov announcements")
    print("   ✅ Data.gov Bulk Datasets - Contract data files")
    print("   ✅ Federal Register - Contract notices")
    print("   ✅ Agency Press Releases - NASA, GSA, VA, DOD, DHS, DOE")
    print("   ✅ Small Business Contracts - SBA awards")
    print("   ✅ Contract Modifications - Change tracking")
    print()
    print("⏱️  Estimated time: 5-7 minutes for comprehensive scan")
    print()
    
    try:
        # Initialize ultimate monitor
        monitor = UltimateGovernmentMonitor()
        
        # Run ultimate collection
        results = monitor.run_ultimate_collection(days_back=30)
        
        if results.get('error'):
            print(f"\n❌ Collection failed: {results['error']}")
            return 1
        
        # Success summary
        print(f"\n✅ SUCCESS! Ultimate collection completed successfully.")
        print(f"   📈 Database now contains {results.get('new_contracts_saved', 0)} additional contracts")
        print(f"   🎯 Ready for dashboard analysis at http://127.0.0.1:8080")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Collection interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
