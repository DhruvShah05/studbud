# Linting Guide

This project includes comprehensive linting for both frontend and backend code.

## Quick Start

### Run All Linters
```bash
npm run lint
# or
./lint-all.sh
```

### Run Specific Linters

**Frontend only:**
```bash
npm run lint:frontend
# or
cd frontend && npm run lint
```

**Backend only:**
```bash
npm run lint:backend
```

## What Gets Checked

### Frontend (TypeScript/Next.js)
- ✅ **ESLint** - Code quality and style
- ✅ **TypeScript** - Type checking
- ✅ **Next.js** - Framework-specific rules

### Backend (Python/Flask)
- ✅ **Black** - Code formatting (PEP8)
- ✅ **Flake8** - Style guide enforcement
- ✅ **Pylint** - Comprehensive code analysis

## Auto-Fix Issues

### Frontend
```bash
cd frontend
npm run lint
# Note: ESLint 9 auto-fix is not fully supported with current config
# Manually fix the warnings shown in the output
```

### Backend
```bash
npm run format:backend
# or
cd backend
source venv/bin/activate
black .
```

## Configuration Files

- **Frontend**: `frontend/.eslintrc.json`, `frontend/tsconfig.json`
- **Backend**: `.pylintrc` (root level)
- **Full Linter**: `lint-all.sh`

## CI/CD Integration

Linting runs automatically on:
- Every push to `main` branch
- Every pull request
- See `.github/workflows/test-frontend.yml`

## Linting Rules

### Frontend ESLint Rules
- React hooks rules
- Next.js best practices
- TypeScript strict mode
- Import order

### Backend Python Rules
- Max line length: 100 characters
- PEP8 compliance
- Type hints recommended
- Docstrings for public functions

## Troubleshooting

**Issue**: `venv not found` in backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install flake8 black pylint
```

**Issue**: `node_modules not found` in frontend
```bash
cd frontend
npm install
```

**Issue**: Permission denied on `lint-all.sh`
```bash
chmod +x lint-all.sh
```

## Pre-commit Hook (Optional)

To run linting before every commit:

```bash
# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
npm run lint
EOF

chmod +x .git/hooks/pre-commit
```
