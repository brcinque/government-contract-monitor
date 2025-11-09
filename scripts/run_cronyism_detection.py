#!/usr/bin/env python3
"""
Cronyism Detection Script - Your Ultimate Anti-Corruption Contract Monitor
Specifically designed to detect the scenarios you outlined
"""

from comprehensive_collector import UltimateGovernmentMonitor
from scenario_monitoring import ScenarioMonitor
from datetime import datetime
import sys

def main():
    """Main cronyism detection function"""
    print("🔍 GOVERNMENT CONTRACT CRONYISM DETECTION")
    print("=" * 60)
    print("🎯 Monitoring for corruption patterns:")
    print("   • National Emergency acceleration")
    print("   • Economic Patriotism traps") 
    print("   • Information Sovereignty gambits")
    print("   • Financial Security consolidation")
    print("   • Connected network accumulation")
    print()
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Run comprehensive data collection
        print("📊 Phase 1: Comprehensive data collection...")
        monitor = UltimateGovernmentMonitor()
        collection_results = monitor.run_ultimate_collection(days_back=30)
        
        # Run scenario-based analysis
        print("\n🚨 Phase 2: Scenario-based pattern detection...")
        scenario_monitor = ScenarioMonitor()
        scenario_results = scenario_monitor.run_full_scenario_analysis()
        
        # Print results
        print(f"\n🎯 CRONYISM DETECTION RESULTS")
        print(f"=" * 50)
        
        # Collection summary
        print(f"📊 DATA COLLECTION:")
        print(f"   • New contracts found: {collection_results.get('new_contracts_saved', 0)}")
        print(f"   • Total database contracts: {collection_results.get('unique_contracts', 0)}")
        print(f"   • Sources accessed: {len(collection_results.get('sources_used', []))}")
        
        # Scenario analysis results
        print(f"\n🚨 SCENARIO ANALYSIS:")
        total_alerts = 0
        high_risk_alerts = 0
        
        for scenario_name, alerts in scenario_results.items():
            alert_count = len(alerts)
            total_alerts += alert_count
            
            if alert_count > 0:
                high_severity = len([a for a in alerts if a.severity == 'HIGH'])
                high_risk_alerts += high_severity
                print(f"   🔴 {scenario_name.replace('_', ' ').title()}: {alert_count} alerts ({high_severity} HIGH)")
                
                # Show top alert
                if alerts:
                    top_alert = max(alerts, key=lambda x: x.risk_score)
                    print(f"      Top risk: {top_alert.company} - ${top_alert.amount:,.0f}")
                    print(f"      Pattern: {top_alert.pattern_detected}")
            else:
                print(f"   ✅ {scenario_name.replace('_', ' ').title()}: No alerts")
        
        # Summary
        print(f"\n📋 SUMMARY:")
        if total_alerts > 0:
            print(f"   🚨 {total_alerts} total alerts generated")
            print(f"   🔴 {high_risk_alerts} high-risk patterns detected")
            print(f"   ⚠️  Recommend manual review of flagged contracts")
        else:
            print(f"   ✅ No concerning patterns detected")
            print(f"   📊 System operational and monitoring")
        
        print(f"\n🎯 NEXT STEPS:")
        print(f"   • View dashboard: http://127.0.0.1:8080")
        print(f"   • Run daily: python3 run_cronyism_detection.py")
        print(f"   • Monitor alerts for pattern development")
        print(f"   • Watch for emergency procurement increases")
        
        # Generate detailed report if alerts found
        if total_alerts > 0:
            report = scenario_monitor.generate_scenario_report()
            print(f"\n📄 DETAILED SCENARIO REPORT:")
            print("-" * 50)
            print(report)
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Monitoring interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error during monitoring: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
