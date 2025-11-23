# Pre-Commit Security Checklist

Run this checklist BEFORE every `git commit` and `git push`:

## ✅ Required Checks

### 1. Verify Sensitive Files Are Ignored

```bash
git status
```

**Should NOT see:**
- [ ] `.env`
- [ ] `credentials.json`
- [ ] `desktop.credentials.json`
- [ ] `web.credentials.json`
- [ ] `token.json`

### 2. Confirm .gitignore Is Working

```bash
git check-ignore .env credentials.json token.json
```

**Should output:**
```
.env
credentials.json
token.json
```

### 3. Search Staged Files for Secrets

```bash
git diff --cached | grep -i "sk-ant-\|client_secret\|api.*key"
```

**Should output:** Nothing (empty)

### 4. Review What Will Be Committed

```bash
git diff --cached --name-only
```

**Verify:** No sensitive files in the list

### 5. Check for Hardcoded Secrets

```bash
git grep -i "sk-ant-\|GOCSPX-\|client_secret" -- '*.py' '*.md' '*.json'
```

**Should only match:** Example files (*.example)

## 🚨 If You Find Issues

### Found credentials in staged files:

```bash
# Unstage the file
git reset HEAD <file>

# Add to .gitignore if needed
echo "<file>" >> .gitignore
```

### Found hardcoded secrets in code:

1. **Remove the secret immediately**
2. **Replace with environment variable**
3. **Regenerate the credential**
4. **Check git history:**
```bash
git log --all -- <file>
```

## ✅ Safe to Commit When:

- [ ] `git status` shows no sensitive files
- [ ] `git diff --cached` has no API keys/secrets
- [ ] All credentials use environment variables
- [ ] Example files end with `.example`
- [ ] README/docs don't contain real credentials

## 🔐 Final Verification

```bash
# One-liner security check
git status && \
git check-ignore .env credentials.json token.json && \
git diff --cached | grep -i "sk-ant-\|client_secret" || \
echo "✅ Safe to commit!"
```

## 📋 Quick Reference

**Safe to commit:**
- Source code (*.py)
- Documentation (*.md)
- Example configs (*.example)
- Templates (templates/*)
- Requirements (requirements.txt)
- .gitignore

**NEVER commit:**
- .env
- credentials.json
- token.json
- *.key, *.pem
- Any file with "secret" in name
- Backup files with real credentials

---

**When in doubt, don't commit!**

Ask yourself: "Would I be okay with this being public on GitHub?"
