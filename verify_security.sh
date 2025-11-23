#!/bin/bash
# Security Verification Script

echo "🔒 AgentSmith Security Verification"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASS=0
FAIL=0

# Check 1: Sensitive files are ignored
echo "1. Checking if sensitive files are ignored..."
if git check-ignore .env credentials.json token.json > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Sensitive files are properly ignored"
    ((PASS++))
else
    echo -e "${RED}✗${NC} WARNING: Sensitive files are NOT ignored!"
    ((FAIL++))
fi

# Check 2: Sensitive files not in git status
echo ""
echo "2. Checking git status..."
if git status --short | grep -E "\.env$|credentials\.json$|token\.json$" > /dev/null; then
    echo -e "${RED}✗${NC} WARNING: Sensitive files in git status!"
    git status --short | grep -E "\.env$|credentials\.json$|token\.json$"
    ((FAIL++))
else
    echo -e "${GREEN}✓${NC} No sensitive files in git status"
    ((PASS++))
fi

# Check 3: No secrets in staged files
echo ""
echo "3. Checking staged files for secrets..."
if git diff --cached | grep -i "sk-ant-\|GOCSPX-\|client_secret" > /dev/null; then
    echo -e "${RED}✗${NC} WARNING: Found secrets in staged files!"
    ((FAIL++))
else
    echo -e "${GREEN}✓${NC} No secrets in staged files"
    ((PASS++))
fi

# Check 4: No secrets in tracked files
echo ""
echo "4. Checking tracked files for hardcoded secrets..."
if git ls-files | xargs grep -i "sk-ant-.*api03\|GOCSPX-" 2>/dev/null | grep -v ".example" > /dev/null; then
    echo -e "${RED}✗${NC} WARNING: Found hardcoded secrets in tracked files!"
    ((FAIL++))
else
    echo -e "${GREEN}✓${NC} No hardcoded secrets in tracked files"
    ((PASS++))
fi

# Check 5: Example files exist
echo ""
echo "5. Checking for example files..."
if [ -f "credentials.json.example" ] && [ -f ".env.example" ]; then
    echo -e "${GREEN}✓${NC} Example files exist"
    ((PASS++))
else
    echo -e "${YELLOW}!${NC} Missing example files"
    ((FAIL++))
fi

# Check 6: .gitignore exists and has content
echo ""
echo "6. Checking .gitignore..."
if [ -f ".gitignore" ] && grep -q "credentials.json" .gitignore; then
    echo -e "${GREEN}✓${NC} .gitignore properly configured"
    ((PASS++))
else
    echo -e "${RED}✗${NC} .gitignore missing or incomplete"
    ((FAIL++))
fi

# Summary
echo ""
echo "===================================="
echo "Summary: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ All security checks passed!${NC}"
    echo "Safe to commit and push."
    exit 0
else
    echo -e "${RED}❌ Security issues found!${NC}"
    echo "DO NOT commit until issues are resolved."
    exit 1
fi
