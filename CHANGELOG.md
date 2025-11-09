# 📋 Changelog

## 🎯 Recent Updates

### Interactive Dashboard Features (Latest)
**Added clickable stat cards with detailed modal popups**

#### New Features:
- **Clickable Stat Cards**: Rapid Accumulation and Large Contracts cards now clickable
- **Modal Popups**: Detailed views with company information and contract details
- **Real-time Data**: API endpoints fetch live data when cards are clicked
- **Enhanced UX**: Hover effects, click hints, and professional modal design

#### Files Modified:
- `enhanced_dashboard.py` - Added modals, JavaScript functions, and API endpoints

#### New API Endpoints:
- `/api/rapid-accumulation` - Companies with multiple contracts in 90 days
- `/api/large-contracts` - Contracts >$50M from last 6 months

#### Interactive Elements:
1. **Rapid Accumulation Companies (2)** - Click to see:
   - Company names and contract counts
   - Total amounts and averages
   - Timeline of contract accumulation
   - Pattern analysis (contracts per day span)

2. **Large Contracts (1)** - Click to see:
   - Contract recipients and amounts
   - Awarding agencies and dates
   - Competition types
   - Contract descriptions

#### Impact:
- ✅ **Fully interactive dashboard** - No more static numbers
- ✅ **Detailed drill-down capability** - Click any stat for details
- ✅ **Professional modal design** - Clean, readable popups
- ✅ **Real-time data loading** - Fresh data on every click
- ✅ **Enhanced user experience** - Visual feedback and smooth animations

### Port Conflict Fix
**Changed dashboard port from 5000 to 8080 to avoid macOS AirPlay conflicts**

#### Issue:
- Port 5000 was blocked by macOS ControlCenter (AirPlay Receiver)
- Users getting "Access denied" when trying to access dashboard

#### Files Modified:
- `enhanced_dashboard.py`
- `dashboard_webapp.py` 
- `monitor.py`
- `scripts/run_dashboard.py`
- `scripts/run_cronyism_detection.py`
- `scripts/run_ultimate_collection.py`
- `scripts/run_enhanced_collection.py`
- `README.md`

#### Changes Made:
- **Before**: All dashboards used port 5000
- **After**: All dashboards now use port 8080
- Updated all URL references in scripts and documentation
- Added startup messages showing correct URL

#### Impact:
- ✅ Dashboard now accessible without port conflicts
- ✅ Works on macOS systems with AirPlay enabled
- ✅ Consistent port usage across all components
- ✅ Clear startup messages with correct URLs

### High-Risk View Filter Update
**Changed high-risk contract filtering from 365 days to 12 months**

#### Files Modified:
- `enhanced_dashboard.py`

#### Changes Made:
1. **Emergency Contracts Filter**
   - **Before**: `date('now', '-365 days')`
   - **After**: `date('now', '-12 months')`
   - **Function**: `get_emergency_contracts()`

2. **Agency Risk Analysis Filter**
   - **Before**: `date('now', '-365 days')`
   - **After**: `date('now', '-12 months')`
   - **Function**: `get_agency_risk_analysis()`

3. **UI Updates**
   - Updated section header to "Emergency/No-Bid Contracts (Last 12 Months)"
   - Updated function documentation to reflect 12-month timeframe

#### Impact:
- ✅ High-risk view no longer shows old contracts from 2022
- ✅ Focus on most recent 12 months of activity
- ✅ More relevant and actionable alerts
- ✅ Consistent timeframe across all high-risk analysis

#### Testing:
- ✅ Functions import and execute correctly
- ✅ Database queries work with new timeframe
- ✅ Dashboard loads without errors
- ✅ Filter correctly excludes older contracts

### System Cleanup (Previous)
- Removed 11+ redundant dashboard files
- Organized structure into core/, scripts/, archive/
- Updated documentation and created visual architecture diagram
- Fixed all import paths and dependencies
