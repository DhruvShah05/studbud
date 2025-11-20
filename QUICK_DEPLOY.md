# Quick Deploy Guide (15 Minutes)

Fast-track deployment guide for StudBud on AWS.

## 🚀 Prerequisites

- AWS Account with admin access
- GitHub repository with your code
- Vercel account (free)

---

## Step 1: Install CLIs (2 min)

```bash
pip install awsebcli
brew install awscli  # or: pip install awscli
```

---

## Step 2: Deploy Backend to AWS (5 min)

```bash
cd backend

# Initialize and create Elastic Beanstalk app
eb init -p python-3.11 studbud-backend --region us-east-1
eb create studbud-backend-prod --instance-type t3.small --single

# Set environment variables (update with your values)
eb setenv \
  GEMINI_API_KEY=your_key \
  DEEPGRAM_API_KEY=your_key \
  FLASK_SECRET_KEY=your_secret \
  DB_HOST=your-rds-endpoint.rds.amazonaws.com \
  DB_PASSWORD=your_db_password \
  AWS_ACCESS_KEY_ID=your_aws_key \
  AWS_SECRET_ACCESS_KEY=your_aws_secret \
  S3_BUCKET_NAME=studbud-sources-prod \
  FLASK_ENV=production \
  ALLOWED_ORIGINS=https://your-app.vercel.app \
  PORT=8000

# Deploy
eb deploy

# Get URL
eb status | grep CNAME
```

---

## Step 3: Deploy Frontend to Vercel (3 min)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Set root directory: `frontend`
4. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://[your-eb-url].elasticbeanstalk.com
   ```
5. Click "Deploy"

---

## Step 4: Setup Auto-Deploy (3 min)

1. Add GitHub Secrets (Settings > Secrets > Actions):
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

2. Push to GitHub:
   ```bash
   git add .
   git commit -m "Setup deployment"
   git push origin main
   ```

3. **Done!** GitHub Actions auto-deploys backend, Vercel auto-deploys frontend.

---

## Step 5: Update CORS (2 min)

After getting Vercel URL, update backend:

```bash
cd backend
eb setenv ALLOWED_ORIGINS=https://your-app.vercel.app
```

---

## ✅ Verification

- Backend: `https://[your-eb-url].elasticbeanstalk.com/api/health`
- Frontend: `https://your-app.vercel.app`

---

## 🔄 Future Deployments

Just push to GitHub - everything auto-deploys! ✨

```bash
git add .
git commit -m "Your changes"
git push
```

---

## 📊 Monitor Deployments

- Backend: [GitHub Actions](https://github.com/your-repo/actions)
- Frontend: [Vercel Dashboard](https://vercel.com/dashboard)
- Logs: `eb logs` or Vercel logs

---

## Common Issues

**CORS Error**: Update `ALLOWED_ORIGINS` with your Vercel URL
**DB Connection**: Check RDS security group allows EB access
**Build Fails**: Check `eb logs` for details

For detailed guide, see [DEPLOYMENT.md](./DEPLOYMENT.md)
