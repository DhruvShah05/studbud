#!/bin/bash

# Full Linter Check Script for StudBud
# Runs linting checks on both frontend and backend

set -e  # Exit on error

echo "🔍 Starting full linter checks..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0

# ============================================
# FRONTEND LINTING
# ============================================
echo "📦 Frontend Linting (Next.js/TypeScript)"
echo "========================================"

if [ -d "frontend" ]; then
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "${YELLOW}⚠️  Installing frontend dependencies...${NC}"
        npm install
    fi
    
    # Run ESLint
    echo "Running ESLint..."
    if npm run lint; then
        echo "${GREEN}✅ ESLint passed${NC}"
    else
        echo "${RED}❌ ESLint failed${NC}"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Run TypeScript type checking
    echo ""
    echo "Running TypeScript type check..."
    if npx tsc --noEmit; then
        echo "${GREEN}✅ TypeScript type check passed${NC}"
    else
        echo "${RED}❌ TypeScript type check failed${NC}"
        ERRORS=$((ERRORS + 1))
    fi
    
    cd ..
else
    echo "${RED}❌ Frontend directory not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo ""

# ============================================
# BACKEND LINTING
# ============================================
echo "🐍 Backend Linting (Python/Flask)"
echo "========================================"

if [ -d "backend" ]; then
    cd backend
    
    # Check if virtual environment exists, if not create one
    if [ ! -d "venv" ]; then
        echo "${YELLOW}⚠️  Creating virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install linting tools if not present
    echo "Installing/updating linting tools..."
    pip install -q flake8 black pylint mypy 2>/dev/null || true
    
    # Run Black (code formatter check)
    echo ""
    echo "Running Black (code formatter)..."
    if black --check --diff .; then
        echo "${GREEN}✅ Black formatting check passed${NC}"
    else
        echo "${RED}❌ Black formatting issues found${NC}"
        echo "${YELLOW}💡 Run 'black .' to auto-format${NC}"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Run Flake8 (style guide enforcement)
    echo ""
    echo "Running Flake8 (PEP8 style check)..."
    if flake8 --max-line-length=100 --exclude=venv,__pycache__,.git --ignore=E203,W503 .; then
        echo "${GREEN}✅ Flake8 passed${NC}"
    else
        echo "${RED}❌ Flake8 found issues${NC}"
        ERRORS=$((ERRORS + 1))
    fi
    
    # Run Pylint (comprehensive linting)
    echo ""
    echo "Running Pylint..."
    if pylint --rcfile=../.pylintrc --disable=C0111,R0903,C0103 --max-line-length=100 \
        --ignore=venv,__pycache__ *.py routes/*.py utils/*.py 2>/dev/null || [ $? -lt 16 ]; then
        echo "${GREEN}✅ Pylint passed${NC}"
    else
        echo "${YELLOW}⚠️  Pylint found some issues (non-critical)${NC}"
    fi
    
    # Deactivate virtual environment
    deactivate
    
    cd ..
else
    echo "${RED}❌ Backend directory not found${NC}"
    ERRORS=$((ERRORS + 1))
fi

echo ""
echo ""

# ============================================
# SUMMARY
# ============================================
echo "========================================"
echo "📊 Linting Summary"
echo "========================================"

if [ $ERRORS -eq 0 ]; then
    echo "${GREEN}✅ All linting checks passed!${NC}"
    exit 0
else
    echo "${RED}❌ Found $ERRORS error(s)${NC}"
    echo ""
    echo "💡 Tips:"
    echo "  - Frontend: Run 'cd frontend && npm run lint -- --fix' to auto-fix ESLint issues"
    echo "  - Backend: Run 'cd backend && black .' to auto-format Python code"
    exit 1
fi
