# 📋 Deployment Checklist

Use this checklist to ensure you have everything ready for AWS deployment.

---

## ✅ Pre-Deployment Checklist

### AWS Account Setup
- [ ] AWS account created with admin access
- [ ] AWS CLI installed (`aws --version`)
- [ ] EB CLI installed (`eb --version`)
- [ ] AWS credentials configured (`aws configure`)

### Database Setup
- [ ] RDS PostgreSQL instance created
- [ ] Database endpoint saved
- [ ] Database password saved
- [ ] Database schema imported (`backend/schema.sql`)
- [ ] RDS security group allows connections

### Storage Setup
- [ ] S3 bucket created (e.g., `studbud-sources-prod`)
- [ ] S3 CORS configured
- [ ] IAM user created for S3 access
- [ ] AWS Access Key and Secret Key saved

### API Keys
- [ ] Gemini API key obtained
- [ ] Deepgram API key obtained (optional but recommended)
- [ ] Flask secret key generated

### Code Repository
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] GitHub Actions enabled

### Vercel Account
- [ ] Vercel account created
- [ ] GitHub connected to Vercel

---

## 📝 Information Gathering

Copy this template and fill in your values:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Database
DB_HOST=
DB_PORT=5432
DB_NAME=studbud
DB_USER=postgres
DB_PASSWORD=

# Storage
S3_BUCKET_NAME=

# API Keys
GEMINI_API_KEY=
DEEPGRAM_API_KEY=
FLASK_SECRET_KEY=

# Application
APP_NAME=studbud-backend
ENV_NAME=studbud-backend-prod
INSTANCE_TYPE=t3.small
```

---

## 🚀 Deployment Steps

### Step 1: Backend Deployment
- [ ] Navigate to backend directory
- [ ] Initialize EB (`eb init`)
- [ ] Create environment (`eb create`)
- [ ] Set environment variables (`eb setenv`)
- [ ] Deploy backend (`eb deploy`)
- [ ] Verify health check (`eb status`)
- [ ] Save backend URL

### Step 2: Frontend Deployment
- [ ] Go to vercel.com/new
- [ ] Import GitHub repository
- [ ] Set root directory to `frontend`
- [ ] Add environment variable `NEXT_PUBLIC_API_URL`
- [ ] Deploy
- [ ] Save frontend URL

### Step 3: CORS Configuration
- [ ] Update backend `ALLOWED_ORIGINS` with frontend URL
- [ ] Redeploy backend (`eb deploy`)
- [ ] Test frontend can call backend

### Step 4: GitHub Actions Setup
- [ ] Add `AWS_ACCESS_KEY_ID` to GitHub Secrets
- [ ] Add `AWS_SECRET_ACCESS_KEY` to GitHub Secrets
- [ ] Push to main branch
- [ ] Verify GitHub Actions runs successfully

### Step 5: Verification
- [ ] Backend health check works
- [ ] Frontend loads correctly
- [ ] Can upload documents
- [ ] Can generate outputs
- [ ] Audio generation works (if Deepgram configured)
- [ ] Auto-deployment works on push

---

## 🔍 Testing Checklist

### Backend Tests
```bash
# Health check
curl https://your-backend-url/api/health

# Should return:
{
  "status": "healthy",
  "gemini_configured": true,
  "database_configured": true,
  "s3_configured": true
}
```

### Frontend Tests
- [ ] Home page loads
- [ ] Can create workspace
- [ ] Can upload file
- [ ] Can chat with AI
- [ ] Can generate mind map
- [ ] Can generate flashcards
- [ ] Downloads work

### CI/CD Tests
- [ ] Make small code change
- [ ] Commit and push
- [ ] GitHub Actions triggers
- [ ] Backend auto-deploys
- [ ] Frontend auto-deploys
- [ ] Changes reflected in production

---

## 🔐 Security Checklist

### AWS Security
- [ ] RDS security group restricts to EB only
- [ ] S3 bucket has proper CORS configuration
- [ ] IAM user has minimal required permissions
- [ ] No AWS credentials in code
- [ ] Environment variables encrypted

### Application Security
- [ ] HTTPS enabled on both frontend and backend
- [ ] CORS configured properly
- [ ] Secret keys are strong and random
- [ ] No sensitive data in logs
- [ ] Database connections use SSL

### GitHub Security
- [ ] Secrets stored in GitHub Secrets, not code
- [ ] `.env` files gitignored
- [ ] No API keys in repository
- [ ] Branch protection enabled (optional)

---

## 📊 Monitoring Setup

### AWS CloudWatch
- [ ] EB environment health monitoring enabled
- [ ] RDS monitoring enabled
- [ ] Set up alarms for high CPU/memory
- [ ] Configure log retention

### Vercel
- [ ] Analytics enabled
- [ ] Error tracking configured
- [ ] Performance monitoring active

### GitHub
- [ ] Email notifications for failed Actions
- [ ] Dependabot enabled for security updates

---

## 💰 Cost Optimization

### Review Monthly
- [ ] Check AWS billing dashboard
- [ ] Monitor RDS usage
- [ ] Review S3 storage size
- [ ] Check data transfer costs

### Optimization Tips
- [ ] Use RDS free tier if eligible
- [ ] Enable S3 lifecycle policies for old files
- [ ] Configure auto-scaling for EB
- [ ] Delete unused resources

---

## 🔄 Maintenance Checklist

### Weekly
- [ ] Check application health
- [ ] Review error logs
- [ ] Monitor costs

### Monthly
- [ ] Update dependencies
- [ ] Review security updates
- [ ] Check database backups
- [ ] Optimize database queries

### Quarterly
- [ ] Review architecture
- [ ] Update documentation
- [ ] Load testing
- [ ] Security audit

---

## 🆘 Emergency Contacts

Keep these handy:

```
AWS Support: https://console.aws.amazon.com/support
Vercel Support: https://vercel.com/help
GitHub Support: https://support.github.com

Backend URL: https://_____________.elasticbeanstalk.com
Frontend URL: https://_____________.vercel.app
Database URL: _____________.rds.amazonaws.com
S3 Bucket: s3://____________

Emergency Rollback:
Backend: eb deploy --version [previous-version]
Frontend: Vercel dashboard → Previous deployment → Promote
```

---

## 📚 Quick Reference

### Useful Commands

```bash
# Backend
eb status                  # Check status
eb logs                    # View logs
eb deploy                  # Deploy
eb setenv KEY=value        # Set env var
eb printenv                # List env vars
eb ssh                     # SSH into instance

# Frontend
vercel --prod             # Deploy to production
vercel logs               # View logs
vercel env ls             # List env vars

# AWS
aws s3 ls s3://bucket-name              # List S3 files
aws rds describe-db-instances           # List RDS instances
aws logs tail /aws/elasticbeanstalk/... # Tail logs

# Git
git push origin main      # Triggers auto-deploy
git revert HEAD           # Rollback last commit
```

---

## ✅ Post-Deployment Success

If you've checked all boxes:

- ✅ Application is live in production
- ✅ Auto-deployment is working
- ✅ Monitoring is active
- ✅ Security is configured
- ✅ You're ready to scale!

**Congratulations! 🎉**

---

## 📞 Getting Help

If you're stuck:

1. Check `DEPLOYMENT.md` for detailed instructions
2. Review error logs (`eb logs` or Vercel dashboard)
3. Verify all environment variables are set
4. Check security groups and CORS settings
5. Review GitHub Actions logs

**Remember**: The auto-deploy setup takes ~30 minutes once, but saves hours every week!

---

**Happy Deploying! 🚀**
