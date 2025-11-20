# Vercel Settings Quick Reference

## Exact Settings from Screenshots

### Framework Settings
```
Framework Preset: Next.js
Build Command: npm run build (or next build) - Override: ON
Output Directory: Next.js default - Override: ON
Install Command: yarn install, pnpm install, npm install, or bun install - Override: ON
Development Command: next dev --port $PORT - Override: ON
```

### Root Directory
```
Root Directory: frontend
Include files outside the root directory in the Build Step: Enabled ✓
Skip deployments when there are no changes: Disabled
```

### Node.js Version
```
Node.js Version: 22.x
```

### Build Features
```
On-Demand Concurrent Builds: Disabled (Pro plan feature)
Rolling Releases: Disabled (Pro plan feature)
Prioritize Production Builds: Enabled ✓
```

## Environment Variables to Add

| Key | Example Value | Environment |
|-----|---------------|-------------|
| `NEXT_PUBLIC_API_URL` | `https://studbud-backend.elasticbeanstalk.com` | Production, Preview |
| `NEXT_PUBLIC_API_URL` | `http://localhost:5000` | Development |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | `pk_test_...` or `pk_live_...` | All |
| `CLERK_SECRET_KEY` | `sk_test_...` or `sk_live_...` | All |

## Files Updated

### ✅ `vercel.json` (Updated)
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

**Note**: Commands no longer need `cd frontend` because Root Directory is set to `frontend`.

### ✅ `frontend/package.json` (Already Correct)
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx"
  }
}
```

### ✅ `frontend/next.config.js` (Already Correct)
```javascript
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
}
```

## Deployment Steps

1. **Import to Vercel**: Connect GitHub repo
2. **Set Root Directory**: `frontend`
3. **Configure Framework**: Use settings above
4. **Add Environment Variables**: All required variables
5. **Deploy**: Click deploy button
6. **Verify**: Test all functionality

## Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| Build fails | Check Root Directory = `frontend` |
| Env vars not working | Redeploy after adding variables |
| CORS errors | Add Vercel domain to backend CORS |
| Module not found | Verify `frontend/package.json` has all deps |

## Post-Deployment Checklist

- [ ] Frontend loads at Vercel URL
- [ ] Authentication works (Clerk)
- [ ] API calls succeed
- [ ] No console errors
- [ ] All pages accessible
- [ ] File uploads functional
- [ ] Chat works correctly
