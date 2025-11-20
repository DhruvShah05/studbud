# Complete Vercel Setup Guide for StudBud

## Prerequisites

1. Vercel account (free tier works)
2. GitHub repository connected to Vercel
3. Backend deployed (AWS Elastic Beanstalk or similar)
4. Clerk account for authentication

## Step-by-Step Vercel Configuration

### 1. Import Project to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository: `ItzMeh679/StudBud`
4. Vercel will detect it as a monorepo

### 2. Configure Project Settings

#### **Root Directory** (CRITICAL)
```
Root Directory: frontend
```
- ✅ Enable: "Include files outside the root directory in the Build Step"
- ❌ Disable: "Skip deployments when there are no changes to the root directory"

#### **Framework Settings**
```
Framework Preset: Next.js
Build Command: npm run build
Output Directory: .next (Next.js default)
Install Command: npm install
Development Command: next dev --port $PORT
```

All overrides should be **enabled** (blue toggle).

#### **Node.js Version**
```
Node.js Version: 22.x
```

#### **Build Optimization**
- ✅ Enable: "Prioritize Production Builds"
- ❌ Disable: "On-Demand Concurrent Builds" (Pro plan only)
- ❌ Disable: "Rolling Releases" (Pro plan only)

### 3. Environment Variables

Navigate to: **Project Settings** → **Environment Variables**

Add the following variables for **Production**, **Preview**, and **Development**:

#### Required Variables:

| Variable Name | Value | Environments |
|--------------|-------|--------------|
| `NEXT_PUBLIC_API_URL` | `https://your-backend.elasticbeanstalk.com` | Production, Preview |
| `NEXT_PUBLIC_API_URL` | `http://localhost:5000` | Development |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | `pk_live_...` or `pk_test_...` | All |
| `CLERK_SECRET_KEY` | `sk_live_...` or `sk_test_...` | All |

#### How to Add:
1. Click **"Add New"** → **"Environment Variable"**
2. Enter **Key** and **Value**
3. Select environments: ✓ Production, ✓ Preview, ✓ Development
4. Click **"Save"**

**Important Notes:**
- Use production Clerk keys for Production environment
- Use test Clerk keys for Preview/Development
- Never commit `.env.local` to git
- Backend URL should be your deployed backend (AWS EB, Railway, etc.)

### 4. Deploy

#### First Deployment:
1. After configuring settings, click **"Deploy"**
2. Vercel will:
   - Install dependencies from `frontend/package.json`
   - Build the Next.js app
   - Deploy to a production URL

#### Subsequent Deployments:
- **Automatic**: Push to `main` branch → Production deployment
- **Preview**: Push to any other branch → Preview deployment
- **Manual**: Click **"Redeploy"** in Vercel dashboard

### 5. Custom Domain (Optional)

1. Go to **Project Settings** → **Domains**
2. Add your custom domain
3. Configure DNS records as instructed by Vercel
4. Wait for SSL certificate provisioning (automatic)

## Project Structure

```
StudBud/
├── frontend/              # ← Root directory for Vercel
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── package.json      # ← Dependencies installed from here
│   ├── next.config.js
│   └── .env.example
├── backend/              # Not deployed to Vercel
├── vercel.json           # Vercel configuration
└── package.json          # Workspace root (not used by Vercel)
```

## Configuration Files

### `vercel.json` (Root)
```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

### `frontend/next.config.js`
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
}

module.exports = nextConfig
```

### `frontend/.env.local` (Local Development Only)
```bash
# DO NOT COMMIT THIS FILE
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

## Troubleshooting

### Build Fails: "Cannot find module"
**Solution**: Ensure `Root Directory` is set to `frontend`

### Environment Variables Not Working
**Solution**: 
1. Check variable names start with `NEXT_PUBLIC_` for client-side access
2. Redeploy after adding new variables
3. Clear build cache: Settings → General → Clear Build Cache

### API Calls Failing (CORS)
**Solution**: Configure CORS in your backend to allow Vercel domain:
```python
# backend/app.py
CORS(app, origins=[
    "http://localhost:3000",
    "https://your-app.vercel.app",
    "https://your-custom-domain.com"
])
```

### Build Command Not Found
**Solution**: Verify `package.json` in `frontend/` has:
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }
}
```

### Deployment Stuck on "Building"
**Solution**:
1. Check build logs in Vercel dashboard
2. Ensure Node.js version matches (22.x)
3. Try manual redeploy

## Verification Checklist

After deployment, verify:

- [ ] Frontend loads at Vercel URL
- [ ] Sign in/Sign up works (Clerk)
- [ ] API calls reach backend
- [ ] File uploads work
- [ ] Chat functionality works
- [ ] No console errors in browser
- [ ] Environment variables are set correctly
- [ ] Custom domain configured (if applicable)

## Monitoring & Logs

### View Deployment Logs:
1. Go to **Deployments** tab
2. Click on a deployment
3. View **Build Logs** and **Function Logs**

### Analytics:
- **Project** → **Analytics** (available on Pro plan)
- Monitor page views, performance, and errors

## CI/CD Integration

Your GitHub Actions workflow (`.github/workflows/test-frontend.yml`) can be enhanced:

```yaml
name: Test Frontend
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '22'
      - name: Install dependencies
        run: cd frontend && npm install
      - name: Lint
        run: cd frontend && npm run lint
      - name: Build
        run: cd frontend && npm run build
```

## Production Checklist

Before going live:

- [ ] Set production Clerk keys
- [ ] Configure production backend URL
- [ ] Enable HTTPS only
- [ ] Set up custom domain
- [ ] Configure error tracking (Sentry, etc.)
- [ ] Test all features in production
- [ ] Set up monitoring/alerts
- [ ] Review security headers
- [ ] Enable Vercel Analytics (optional)

## Support & Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Clerk + Vercel Guide](https://clerk.com/docs/deployments/deploy-to-vercel)

## Quick Commands

```bash
# Local development
cd frontend
npm install
npm run dev

# Build locally (test before deploy)
npm run build
npm start

# Lint
npm run lint
```

## Summary

Your Vercel configuration is now optimized for:
- ✅ Next.js 16 with React 19
- ✅ Monorepo structure (frontend only)
- ✅ Clerk authentication
- ✅ Backend API integration
- ✅ Automatic deployments from GitHub
- ✅ Environment-specific configurations

**Production URL**: `https://your-project.vercel.app`
**Backend URL**: Configure in environment variables
