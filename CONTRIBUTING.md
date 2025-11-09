# Contributing to Government Contract Cronyism Monitor

This tool enables independent monitoring and verification of government contracting. If you have improvements that enhance watchdog capabilities, bug fixes, or additional data sources, contributions are welcome.

## 🌟 How You Can Contribute

### 1. **Report Issues**
- Found a bug? [Open an issue](../../issues)
- Have a feature idea? [Start a discussion](../../discussions)
- Data source not working? Let us know!

### 2. **Add New Data Sources**
We're always looking to expand coverage. Consider adding:
- State/local government contract databases
- International government procurement systems
- Additional federal agency APIs
- Lobbying and campaign finance data for correlation

### 3. **Improve Pattern Detection**
- Enhance cronyism detection algorithms
- Add new corruption pattern scenarios
- Improve risk scoring models
- Reduce false positives

### 4. **Enhance Documentation**
- Improve setup instructions
- Add tutorials and examples
- Translate documentation
- Create video guides

### 5. **Fix Bugs**
- Check the [issues page](../../issues)
- Look for `good first issue` labels
- Test fixes thoroughly before submitting

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git
- SAM.gov API token (free)

### Development Setup

1. **Fork and Clone**
```bash
git clone https://github.com/YOUR_USERNAME/GSA.git
cd GSA
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Token**
```bash
cp token.txt.example token.txt
# Edit token.txt with your SAM.gov API token
```

5. **Test the System**
```bash
python3 monitor.py
# Choose option 4 for Quick Status Check
```

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Comment complex logic

### Testing
- Test your changes with real data collection
- Verify dashboard displays data correctly
- Check for API rate limit compliance
- Test on multiple platforms if possible

### Git Workflow

1. **Create a Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make Your Changes**
- Write clean, documented code
- Test thoroughly
- Commit with clear messages

3. **Commit Messages**
```bash
git commit -m "Add: Brief description of what you added"
git commit -m "Fix: Brief description of what you fixed"
git commit -m "Update: Brief description of what you updated"
```

4. **Push and Create PR**
```bash
git push origin feature/your-feature-name
```
Then open a Pull Request on GitHub

## 🎯 Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style
- [ ] All tests pass
- [ ] Documentation updated (if needed)
- [ ] No sensitive data (tokens, emails) in commits
- [ ] Clear description of changes

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How you tested your changes

## Screenshots (if applicable)
Add screenshots for UI changes
```

## 🔍 Adding New Data Sources

If you're adding a new government data source:

1. **Create a collector class** in `core/` or `archive/`
2. **Follow existing patterns** (see `comprehensive_collector.py`)
3. **Respect rate limits** - add delays between requests
4. **Handle errors gracefully** - APIs can be unreliable
5. **Document the source** - add to README with setup instructions
6. **Test thoroughly** - ensure data quality

### Example Collector Structure
```python
class NewSourceCollector:
    def __init__(self):
        self.base_url = "https://api.example.gov"
        
    def collect_contracts(self, days_back=7):
        """Collect contracts from new source"""
        contracts = []
        # Implementation
        return contracts
```

## 🐛 Bug Report Template

When reporting bugs, please include:
- **Description**: What happened?
- **Expected behavior**: What should happen?
- **Steps to reproduce**: How to recreate the bug?
- **Environment**: OS, Python version, etc.
- **Error messages**: Full error text if applicable
- **Screenshots**: If relevant

## 💡 Feature Request Template

When requesting features:
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives**: Other ways to solve this?
- **Impact**: Who benefits from this feature?

## 🤝 Standards

### Responsible Development
- Focus on accuracy and verification
- Document limitations clearly
- Prioritize monitoring capability improvements
- Test changes thoroughly
- Verify data collection methods

### Unacceptable Practices
- Spreading misinformation
- Misrepresenting monitoring capabilities
- Violating API terms of service
- Committing sensitive data (tokens, credentials)

## 📜 Legal and Ethical Guidelines

### Data Usage
- All data collected is already public
- Respect government API terms of service
- Do not attempt to circumvent rate limits
- Do not scrape aggressively

### Responsible Use
- **Verify findings** through multiple independent sources
- **Context matters** - pattern detection requires proper analysis
- **Correlation ≠ causation** - patterns indicate areas for scrutiny
- **Multiple sources** - cross-verify all information

### Privacy & Security
- This tool monitors organizational patterns, not individuals
- Maintain security of your monitoring data
- Respect API terms of service and rate limits

## 🏆 Recognition

Contributors will be credited in release notes for improvements that enhance monitoring capabilities.

## 📞 Questions?

- Open an issue on GitHub for bugs or feature requests
- Check existing documentation first

## 📚 Resources

- [USASpending API Documentation](https://api.usaspending.gov/)
- [SAM.gov API Documentation](https://open.gsa.gov/api/entity-api/)
- [Federal Register API](https://www.federalregister.gov/developers/api/v1)
- [Project Architecture](SYSTEM_ARCHITECTURE.md)

---

Thank you for helping improve independent monitoring capabilities! 🔍

