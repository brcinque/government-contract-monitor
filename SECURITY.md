# Security Policy

## 🔒 Security Considerations

This project collects data from public government APIs and stores it locally. While the data itself is public, there are important security considerations for running this tool.

## ⚠️ Important Security Warnings

### API Token Security

**🔴 CRITICAL: Never commit your `token.txt` file to version control**

Your SAM.gov API token should be treated as a secret:
- ✅ Use `token.txt` (gitignored by default)
- ✅ Store in environment variables
- ❌ Never commit tokens to git
- ❌ Never share tokens publicly
- ❌ Never include in screenshots or logs

If your token is exposed:
1. Immediately revoke it at https://sam.gov/
2. Generate a new token
3. Update your local `token.txt`
4. If committed to git, remove from history using `git filter-branch` or BFG Repo-Cleaner

### Database Security

The `government_monitor.db` file contains:
- Contract data (all public information)
- Generated alerts and analysis
- Company tracking information

**Best Practices:**
- ✅ Database is gitignored by default
- ✅ Store database locally, not in cloud without encryption
- ✅ Backup database regularly if you want to preserve historical data
- ❌ Don't share database files publicly (they may contain your analysis patterns)

### Email Configuration

If using email alerts (optional):
- ✅ Use app-specific passwords (not your main email password)
- ✅ Store credentials in environment variables or `.env` file (gitignored)
- ❌ Never hardcode email credentials in Python files
- ❌ Never commit email configuration to version control

### Rate Limiting and API Respect

**Ethical Usage:**
- This tool respects API rate limits
- Don't modify delays to scrape faster
- Aggressive scraping may get your IP blocked
- Follow government API terms of service

## 🛡️ Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | ✅ Yes             |
| < 1.0   | ⚠️ Best effort     |

## 🐛 Reporting a Vulnerability

### Security Vulnerabilities

If you discover a security vulnerability in this project:

1. **DO NOT** open a public issue
2. **DO NOT** disclose publicly until patched
3. **DO** report privately via:
   - Open a [Security Advisory](../../security/advisories/new) on GitHub
   - Or email maintainers (if email is provided in profile)

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

We will:
- Acknowledge receipt within 48 hours
- Provide a timeline for fix
- Credit you in the fix (if desired)
- Coordinate public disclosure after patch

### Data Collection Issues

If you find issues with data collection that could:
- Violate API terms of service
- Cause excessive load on government servers
- Bypass rate limiting
- Access unauthorized data

Please report these as security issues.

## 🔍 Security Best Practices for Users

### Local Development
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate

# Install from requirements.txt (once we create it)
pip install -r requirements.txt

# Set up token securely
cp token.txt.example token.txt
# Edit token.txt, never commit it
```

### Production Deployment

If running this tool on a server:

1. **Use environment variables for secrets**
```bash
export SAM_API_TOKEN="your-token-here"
```

2. **Restrict file permissions**
```bash
chmod 600 token.txt
chmod 600 government_monitor.db
chmod 700 .  # Restrict directory access
```

3. **Run with limited privileges**
- Don't run as root
- Use dedicated user account
- Apply principle of least privilege

4. **Secure the database**
- Regular backups
- Encrypt backups
- Secure backup storage

5. **Monitor logs**
- Check for unusual API access patterns
- Monitor for failed authentication attempts
- Watch for rate limit warnings

### Network Security

This tool makes HTTPS requests to:
- `api.usaspending.gov`
- `sam.gov`
- `www.federalregister.gov`
- `www.defense.gov`
- Various agency websites

**Firewall considerations:**
- Outbound HTTPS (443) access required
- No inbound connections needed
- Tool runs entirely locally

### SSL/TLS Certificate Verification

The tool uses SSL verification by default. If you encounter certificate issues:
- ⚠️ Don't disable SSL verification without understanding risks
- Update your Python `certifi` package
- Check system CA certificates

## 📋 Security Checklist for Contributors

Before submitting code:
- [ ] No hardcoded tokens, passwords, or secrets
- [ ] Sensitive files added to `.gitignore`
- [ ] API calls use rate limiting
- [ ] Error messages don't leak sensitive info
- [ ] Input validation for user-provided data
- [ ] SQL queries use parameterization (avoid injection)
- [ ] No arbitrary code execution vulnerabilities

## 🔐 Dependencies

This project uses third-party Python packages. Security considerations:
- Keep dependencies updated
- Review security advisories
- Use virtual environments
- Pin versions in production

Run security checks:
```bash
pip install safety
safety check
```

## 📊 Data Privacy

### What Data is Collected?
- Government contract information (public)
- Company names and contract amounts (public)
- Agency names and dates (public)
- Your generated alerts and analysis (local only)

### What Data is NOT Collected?
- Personal information about individuals
- Private/classified contracts
- Non-public government data
- Your personal information or usage patterns

### Data Retention
- All data stored locally on your machine
- No telemetry or tracking
- No data sent to third parties
- You control retention (can delete database anytime)

## 🚨 Incident Response

If a security incident occurs:

1. **Assessment**: Determine scope and impact
2. **Containment**: Revoke compromised credentials
3. **Notification**: Inform affected users if needed
4. **Remediation**: Apply fixes and patches
5. **Review**: Update security practices

## 📝 Audit Trail

For transparency and accountability:
- All code changes tracked in git
- Security-related commits clearly labeled
- Security advisories publicly disclosed (after fix)

## 🔗 Security Resources

- [SAM.gov API Documentation](https://open.gsa.gov/api/entity-api/)
- [USASpending API Terms](https://api.usaspending.gov/)
- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## 📞 Questions?

Security questions can be raised via GitHub Issues.

---

**Remember: Protect your monitoring data and API credentials. This tool enables independent verification - keep your watchdog capabilities secure.**

