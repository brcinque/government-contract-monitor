#!/usr/bin/env python3
"""
Enhanced Collection Script - Integrates multi-source collection with existing system
"""

from government_monitor_system import GovernmentMonitor, DatabaseManager
from enhanced_collectors import ComprehensiveCollector
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedGovernmentMonitor(GovernmentMonitor):
    """Enhanced monitor with multi-source collection"""
    
    def __init__(self, email_config=None):
        super().__init__(email_config)
        self.multi_collector = ComprehensiveCollector()
    
    def run_comprehensive_collection(self, days_back=30):
        """Run collection from all available sources"""
        logger.info("=== Enhanced Multi-Source Collection ===")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Collect from all sources
            print("🔄 Collecting from multiple government data sources...")
            source_results = self.multi_collector.collect_all_available_data(days_back)
            
            # Merge and deduplicate
            all_contracts = self.multi_collector.merge_and_deduplicate(source_results)
            
            # Save new contracts to database
            new_contracts = 0
            if all_contracts:
                # Check which contracts are new
                existing_ids = self._get_existing_contract_ids()
                new_contracts_list = []
                
                for contract in all_contracts:
                    if contract.award_id not in existing_ids:
                        new_contracts_list.append(contract)
                
                if new_contracts_list:
                    self.db.save_contracts(new_contracts_list)
                    new_contracts = len(new_contracts_list)
                    logger.info(f"Saved {new_contracts} new contracts to database")
            
            # Run pattern analysis
            rapid_alerts = self.analyzer.detect_rapid_accumulation()
            no_bid_alerts = self.analyzer.detect_no_bid_patterns()
            all_alerts = rapid_alerts + no_bid_alerts
            self.alert_manager.process_alerts(all_alerts)
            
            # Generate summary
            results = {
                'sources_used': list(source_results.keys()),
                'contracts_by_source': {k: len(v) for k, v in source_results.items()},
                'total_collected': len(all_contracts),
                'new_contracts_saved': new_contracts,
                'alerts_generated': len(all_alerts),
                'collection_timestamp': datetime.now().isoformat()
            }
            
            print(f"\n✅ Enhanced Collection Complete!")
            print(f"   📊 Sources used: {', '.join(results['sources_used'])}")
            for source, count in results['contracts_by_source'].items():
                print(f"   📄 {source}: {count} contracts")
            print(f"   🆕 New contracts saved: {results['new_contracts_saved']}")
            print(f"   🚨 Alerts generated: {results['alerts_generated']}")
            
            return results
            
        except Exception as e:
            logger.error(f"Enhanced collection failed: {e}")
            print(f"❌ Collection failed: {e}")
            return {
                'sources_used': [],
                'contracts_by_source': {},
                'total_collected': 0,
                'new_contracts_saved': 0,
                'alerts_generated': 0,
                'error': str(e)
            }
    
    def _get_existing_contract_ids(self):
        """Get set of existing contract IDs to avoid duplicates"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT award_id FROM contracts')
        existing_ids = {row[0] for row in cursor.fetchall()}
        conn.close()
        return existing_ids
    
    def get_source_breakdown(self):
        """Get breakdown of contracts by data source"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Add data_source column if it doesn't exist
        try:
            cursor.execute('ALTER TABLE contracts ADD COLUMN data_source TEXT')
            conn.commit()
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        cursor.execute('''
            SELECT 
                COALESCE(data_source, 'legacy') as source,
                COUNT(*) as count,
                SUM(award_amount) as total_amount
            FROM contracts 
            GROUP BY data_source
            ORDER BY count DESC
        ''')
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'source': row[0],
                'contract_count': row[1],
                'total_amount': row[2] or 0
            })
        
        conn.close()
        return results

def main():
    """Main enhanced collection function"""
    print("=== Government Contract Monitor - Enhanced Collection ===")
    
    # Initialize enhanced monitor
    monitor = EnhancedGovernmentMonitor()
    
    # Run comprehensive collection
    results = monitor.run_comprehensive_collection(days_back=30)
    
    if results.get('error'):
        print(f"\n❌ Collection encountered errors")
        return 1
    
    # Show source breakdown
    print(f"\n📊 Data Source Breakdown:")
    source_breakdown = monitor.get_source_breakdown()
    for source_info in source_breakdown:
        print(f"   {source_info['source']}: {source_info['contract_count']} contracts, ${source_info['total_amount']:,.0f}")
    
    print(f"\n🎯 Next Steps:")
    print(f"   • View dashboard: http://127.0.0.1:8080")
    print(f"   • Run daily: python3 run_enhanced_collection.py")
    print(f"   • Check alerts in dashboard for new patterns")
    
    return 0

if __name__ == "__main__":
    exit(main())
