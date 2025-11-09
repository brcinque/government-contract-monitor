#!/usr/bin/env python3
"""
Comprehensive Government Contract Collector
Integrates ALL available data sources for maximum contract discovery
"""

from government_monitor_system import GovernmentMonitor, DatabaseManager
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'archive'))

from enhanced_collectors import ComprehensiveCollector
from missing_sources_collectors import MissingSourcesCollector
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UltimateGovernmentMonitor(GovernmentMonitor):
    """Ultimate monitor with ALL available data sources"""
    
    def __init__(self, email_config=None):
        super().__init__(email_config)
        self.enhanced_collector = ComprehensiveCollector()
        self.missing_sources_collector = MissingSourcesCollector()
    
    def run_ultimate_collection(self, days_back=30):
        """Collect from ALL available government data sources"""
        logger.info("=== ULTIMATE Multi-Source Collection ===")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚀 Collecting from MAXIMUM available government data sources...")
        print()
        
        all_source_results = {}
        total_collected = 0
        
        try:
            # 1. Enhanced collectors (USASpending.gov, DoD, Data.gov)
            print("📊 Phase 1: Enhanced USASpending.gov + DoD + Data.gov...")
            enhanced_results = self.enhanced_collector.collect_all_available_data(days_back)
            all_source_results.update(enhanced_results)
            
            enhanced_total = sum(len(contracts) for contracts in enhanced_results.values())
            total_collected += enhanced_total
            print(f"   ✅ Enhanced sources: {enhanced_total} contracts")
            
            time.sleep(3)  # Rate limiting between phases
            
            # 2. Missing sources (Federal Register, Agency Press, Small Business)
            print("📋 Phase 2: Federal Register + Agency Press + Small Business...")
            missing_results = self.missing_sources_collector.collect_all_missing_sources(days_back)
            
            # Prefix keys to avoid conflicts
            for key, value in missing_results.items():
                all_source_results[f"missing_{key}"] = value
            
            missing_total = sum(len(contracts) for contracts in missing_results.values())
            total_collected += missing_total
            print(f"   ✅ Missing sources: {missing_total} contracts")
            
            # 3. Merge and deduplicate ALL sources
            print("🔄 Phase 3: Merging and deduplicating across ALL sources...")
            all_contracts = self._merge_all_sources(all_source_results)
            
            # 4. Save new contracts to database
            new_contracts = self._save_new_contracts(all_contracts)
            
            # 5. Run pattern analysis on ALL data
            print("🔍 Phase 4: Running pattern analysis...")
            rapid_alerts = self.analyzer.detect_rapid_accumulation()
            no_bid_alerts = self.analyzer.detect_no_bid_patterns()
            all_alerts = rapid_alerts + no_bid_alerts
            self.alert_manager.process_alerts(all_alerts)
            
            # Generate comprehensive results
            results = {
                'collection_type': 'ULTIMATE',
                'sources_used': list(all_source_results.keys()),
                'contracts_by_source': {k: len(v) for k, v in all_source_results.items()},
                'total_collected': total_collected,
                'unique_contracts': len(all_contracts),
                'new_contracts_saved': new_contracts,
                'alerts_generated': len(all_alerts),
                'collection_timestamp': datetime.now().isoformat(),
                'phase_1_enhanced': enhanced_total,
                'phase_2_missing': missing_total
            }
            
            self._print_ultimate_summary(results)
            return results
            
        except Exception as e:
            logger.error(f"Ultimate collection failed: {e}")
            print(f"❌ Ultimate collection failed: {e}")
            return {
                'collection_type': 'ULTIMATE',
                'sources_used': [],
                'contracts_by_source': {},
                'total_collected': 0,
                'unique_contracts': 0,
                'new_contracts_saved': 0,
                'alerts_generated': 0,
                'error': str(e)
            }
    
    def _merge_all_sources(self, all_source_results):
        """Merge contracts from ALL sources with advanced deduplication"""
        all_contracts = []
        seen_signatures = set()
        source_stats = {}
        
        for source_name, contracts in all_source_results.items():
            source_stats[source_name] = {'total': len(contracts), 'unique': 0}
            
            for contract in contracts:
                # Create comprehensive signature for deduplication
                signature = self._create_contract_signature(contract)
                
                if signature not in seen_signatures:
                    contract.data_source = source_name
                    all_contracts.append(contract)
                    seen_signatures.add(signature)
                    source_stats[source_name]['unique'] += 1
        
        print(f"   📊 Deduplication results:")
        for source, stats in source_stats.items():
            print(f"      {source}: {stats['unique']}/{stats['total']} unique")
        
        logger.info(f"Merged to {len(all_contracts)} unique contracts from {len(all_source_results)} sources")
        return all_contracts
    
    def _create_contract_signature(self, contract):
        """Create comprehensive signature for deduplication"""
        # Normalize company name
        company = contract.recipient_name.lower().strip()
        company = company.replace('inc.', 'inc').replace('corp.', 'corp').replace('llc.', 'llc')
        
        # Create signature with multiple fields
        signature = f"{company}_{contract.award_amount}_{contract.award_date}_{contract.awarding_agency.lower()[:20]}"
        return signature
    
    def _save_new_contracts(self, all_contracts):
        """Save new contracts to database"""
        if not all_contracts:
            return 0
        
        existing_ids = self._get_existing_contract_ids()
        new_contracts_list = []
        
        for contract in all_contracts:
            if contract.award_id not in existing_ids:
                new_contracts_list.append(contract)
        
        if new_contracts_list:
            self.db.save_contracts(new_contracts_list)
            logger.info(f"Saved {len(new_contracts_list)} new contracts to database")
            return len(new_contracts_list)
        
        return 0
    
    def _get_existing_contract_ids(self):
        """Get set of existing contract IDs"""
        import sqlite3
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT award_id FROM contracts')
        existing_ids = {row[0] for row in cursor.fetchall()}
        conn.close()
        return existing_ids
    
    def _print_ultimate_summary(self, results):
        """Print comprehensive collection summary"""
        print(f"\n🎉 ULTIMATE Collection Complete!")
        print(f"=" * 60)
        print(f"📊 COLLECTION STATISTICS:")
        print(f"   • Sources accessed: {len(results['sources_used'])}")
        print(f"   • Total contracts collected: {results['total_collected']}")
        print(f"   • Unique contracts (after dedup): {results['unique_contracts']}")
        print(f"   • NEW contracts saved: {results['new_contracts_saved']}")
        print(f"   • Alerts generated: {results['alerts_generated']}")
        print()
        
        print(f"📋 BY COLLECTION PHASE:")
        print(f"   • Phase 1 (Enhanced): {results['phase_1_enhanced']} contracts")
        print(f"   • Phase 2 (Missing Sources): {results['phase_2_missing']} contracts")
        print()
        
        print(f"🔍 BY DATA SOURCE:")
        for source, count in results['contracts_by_source'].items():
            if count > 0:
                print(f"   • {source}: {count} contracts")
        print()
        
        # Database status
        database_stats = self._get_database_stats()
        print(f"💾 DATABASE STATUS:")
        print(f"   • Total contracts in database: {database_stats['total_contracts']}")
        print(f"   • Database size: {database_stats['db_size_mb']:.1f} MB")
        print(f"   • Date range: {database_stats['date_range']}")
        print()
        
        print(f"🎯 NEXT STEPS:")
        print(f"   • View dashboard: http://127.0.0.1:5000")
        print(f"   • Run daily: python3 run_ultimate_collection.py")
        print(f"   • Check alerts for new patterns")
    
    def _get_database_stats(self):
        """Get current database statistics"""
        import sqlite3
        import os
        
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        # Total contracts
        cursor.execute('SELECT COUNT(*) FROM contracts')
        total_contracts = cursor.fetchone()[0]
        
        # Date range
        cursor.execute('SELECT MIN(award_date), MAX(award_date) FROM contracts')
        date_range = cursor.fetchone()
        date_range_str = f"{date_range[0]} to {date_range[1]}" if date_range[0] else "No data"
        
        conn.close()
        
        # Database file size
        db_size_bytes = os.path.getsize(self.db.db_path)
        db_size_mb = db_size_bytes / (1024 * 1024)
        
        return {
            'total_contracts': total_contracts,
            'db_size_mb': db_size_mb,
            'date_range': date_range_str
        }
    
    def get_comprehensive_source_breakdown(self):
        """Get detailed breakdown by all data sources"""
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
                COALESCE(data_source, 'original') as source,
                COUNT(*) as count,
                SUM(award_amount) as total_amount,
                AVG(award_amount) as avg_amount,
                MIN(award_date) as earliest_date,
                MAX(award_date) as latest_date
            FROM contracts 
            GROUP BY data_source
            ORDER BY count DESC
        ''')
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'source': row[0],
                'contract_count': row[1],
                'total_amount': row[2] or 0,
                'avg_amount': row[3] or 0,
                'earliest_date': row[4],
                'latest_date': row[5]
            })
        
        conn.close()
        return results

def main():
    """Main ultimate collection function"""
    print("🚀 ULTIMATE Government Contract Monitor")
    print("=" * 50)
    print("Collecting from ALL available government data sources...")
    print()
    
    # Initialize ultimate monitor
    monitor = UltimateGovernmentMonitor()
    
    # Run ultimate collection
    results = monitor.run_ultimate_collection(days_back=30)
    
    if results.get('error'):
        print(f"\n❌ Collection encountered errors")
        return 1
    
    # Show comprehensive source breakdown
    print(f"\n📊 COMPREHENSIVE DATA SOURCE ANALYSIS:")
    print(f"-" * 60)
    source_breakdown = monitor.get_comprehensive_source_breakdown()
    
    for source_info in source_breakdown:
        print(f"📋 {source_info['source']}:")
        print(f"   • Contracts: {source_info['contract_count']}")
        print(f"   • Total value: ${source_info['total_amount']:,.0f}")
        print(f"   • Average value: ${source_info['avg_amount']:,.0f}")
        print(f"   • Date range: {source_info['earliest_date']} to {source_info['latest_date']}")
        print()
    
    return 0

if __name__ == "__main__":
    exit(main())
