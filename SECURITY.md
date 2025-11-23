# Security Guide

## 🔒 Protecting Your Credentials

This project uses sensitive credentials that should **NEVER** be committed to version control or shared publicly.

### Files to Keep Private

These files contain sensitive information and are already in `.gitignore`:

1. **`.env`** - Contains your Anthropic API key
2. **`credentials.json`** - Google OAuth credentials
3. **`desktop.credentials.json`** - Desktop OAuth credentials (if used)
4. **`web.credentials.json`** - Web OAuth credentials (if used)
5. **`token.json`** - Gmail access token (auto-generated)

### ⚠️ Important Security Checks

Before pushing to GitHub:

```bash
# 1. Verify .gitignore is working
git status

# 2. Check what will be committed
git diff --cached

# 3. Search for accidentally staged secrets
git grep -i "api.*key\|secret\|password" $(git diff --cached --name-only)
```

### 🛡️ If You Accidentally Commit Credentials

If you've already committed sensitive files:

1. **Immediately revoke/regenerate the credentials:**
   - Anthropic API Key: https://console.anthropic.com/
   - Google OAuth: https://console.cloud.google.com/

2. **Remove from git history:**
```bash
# Remove the file from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch credentials.json" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (WARNING: This rewrites history!)
git push origin --force --all
```

3. **Use BFG Repo-Cleaner (easier method):**
```bash
# Install BFG
brew install bfg

# Remove the file from history
bfg --delete-files credentials.json

# Cleanup
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

### ✅ Setting Up Credentials Securely

1. **Copy the example files:**
```bash
cp .env.example .env
cp credentials.json.example credentials.json
```

2. **Add your actual credentials:**
   - Edit `.env` and add your Anthropic API key
   - Edit `credentials.json` with your Google OAuth credentials

3. **Verify they're ignored:**
```bash
git status
# Should NOT show .env or credentials.json
```

### 🔐 Best Practices

1. **Never hardcode secrets** in Python files
2. **Use environment variables** for API keys
3. **Keep credentials.json local only**
4. **Regenerate tokens** if you suspect compromise
5. **Use different credentials** for dev/prod environments
6. **Enable 2FA** on all accounts (Google, Anthropic, GitHub)

### 📋 Credential Checklist

- [ ] `.env` is in `.gitignore`
- [ ] `credentials.json` is in `.gitignore`
- [ ] `token.json` is in `.gitignore`
- [ ] No API keys in source code
- [ ] Example files are provided for setup
- [ ] Secrets are not in commit history

### 🚨 What to Do If Exposed

If credentials are exposed on GitHub:

1. **Delete the repository immediately** (if public)
2. **Revoke ALL credentials:**
   - Anthropic: Generate new API key
   - Google: Delete OAuth client, create new one
3. **Check for unauthorized usage:**
   - Anthropic dashboard: Usage statistics
   - Google Cloud: API activity logs
4. **Set up monitoring/alerts** for unusual activity
5. **Consider using git-secrets:**
```bash
# Install git-secrets
brew install git-secrets

# Set up for this repo
git secrets --install
git secrets --register-aws  # Or custom patterns
```

### 🔍 Scanning for Secrets

Use tools to scan for accidentally committed secrets:

```bash
# TruffleHog
pip install truffleHog
truffleHog --regex --entropy=False https://github.com/yourusername/AgentSmith

# GitLeaks
brew install gitleaks
gitleaks detect --source . --verbose
```

### 📝 Example .env Template

```bash
# Anthropic API Key
# Get yours at: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXX

# Optional: Set a different model
# MODEL=claude-sonnet-4-5-20250929
```

### 🎯 Quick Security Audit

Run this before every commit:

```bash
# Check for secrets in staged files
git diff --cached | grep -i "api.*key\|secret\|password\|token"

# Verify gitignore is working
git check-ignore .env credentials.json token.json
```

---

**Remember:** It's always better to be safe than sorry. When in doubt, regenerate your credentials!
