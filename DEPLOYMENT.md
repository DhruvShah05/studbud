# AWS Deployment Guide

Complete guide to deploy StudBud to AWS with auto-deployment CI/CD pipeline.

## Architecture Overview

- **Backend**: AWS Elastic Beanstalk (Python/Flask)
- **Frontend**: Vercel (Next.js)
- **Database**: AWS RDS PostgreSQL
- **Storage**: AWS S3
- **CI/CD**: GitHub Actions (Backend) + Vercel (Frontend)

---

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **GitHub Account** and repository
3. **Vercel Account** (free tier works)
4. **AWS CLI** installed locally
5. **EB CLI** (Elastic Beanstalk CLI) installed

### Install Required CLIs

```bash
# Install AWS CLI
brew install awscli

# Install EB CLI
pip install awsebcli

# Verify installations
aws --version
eb --version
```

---

## Part 1: AWS RDS PostgreSQL Setup

### 1.1 Create RDS Database (if not already created)

```bash
# Login to AWS Console
# Navigate to RDS > Create database

# Settings:
- Engine: PostgreSQL 15.x
- Template: Free tier (for testing) or Production
- DB Instance: db.t3.micro (free tier) or larger
- DB name: studbud
- Master username: postgres
- Master password: [create secure password]
- Public access: Yes (for now - restrict later)
- VPC security group: Create new (allow port 5432 from your IP)
```

### 1.2 Initialize Database Schema

```bash
# Connect to RDS database
psql -h your-rds-endpoint.region.rds.amazonaws.com -U postgres -d studbud

# Run the schema files
\i backend/schema.sql
\i backend/aws_migration.sql
```

---

## Part 2: AWS S3 Setup

### 2.1 Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://studbud-sources-prod --region us-east-1

# Enable CORS
aws s3api put-bucket-cors --bucket studbud-sources-prod --cors-configuration file://s3-cors.json
```

Create `s3-cors.json`:
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
      "AllowedHeaders": ["*"],
      "MaxAgeSeconds": 3000
    }
  ]
}
```

### 2.2 Create IAM User for S3 Access

```bash
# Create IAM user
aws iam create-user --user-name studbud-s3-user

# Attach S3 policy
aws iam attach-user-policy --user-name studbud-s3-user --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Create access keys
aws iam create-access-key --user-name studbud-s3-user
# Save the AccessKeyId and SecretAccessKey
```

---

## Part 3: Backend Deployment (AWS Elastic Beanstalk)

### 3.1 Initialize Elastic Beanstalk Application

```bash
# Navigate to backend directory
cd backend

# Initialize EB application
eb init -p python-3.11 studbud-backend --region us-east-1

# Create environment
eb create studbud-backend-prod --instance-type t3.small --single
```

### 3.2 Configure Environment Variables

```bash
# Set environment variables in Elastic Beanstalk
eb setenv \
  GEMINI_API_KEY=your_gemini_api_key \
  DEEPGRAM_API_KEY=your_deepgram_api_key \
  FLASK_SECRET_KEY=your_secret_key \
  DB_HOST=your-rds-endpoint.region.rds.amazonaws.com \
  DB_PORT=5432 \
  DB_NAME=studbud \
  DB_USER=postgres \
  DB_PASSWORD=your_database_password \
  AWS_ACCESS_KEY_ID=your_aws_access_key \
  AWS_SECRET_ACCESS_KEY=your_aws_secret_key \
  AWS_REGION=us-east-1 \
  S3_BUCKET_NAME=studbud-sources-prod \
  FLASK_ENV=production \
  ALLOWED_ORIGINS=https://your-frontend.vercel.app \
  PORT=8000
```

### 3.3 Deploy Backend

```bash
# Deploy to Elastic Beanstalk
eb deploy

# Check status
eb status

# View logs if needed
eb logs

# Get application URL
eb open
```

### 3.4 Configure Security Group

```bash
# Update RDS security group to allow Elastic Beanstalk
# In AWS Console:
# 1. Go to RDS > Your Database > Security Groups
# 2. Add inbound rule: PostgreSQL (5432) from EB security group
```

---

## Part 4: Frontend Deployment (Vercel)

### 4.1 Connect GitHub to Vercel

1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "Add New Project"
3. Import your GitHub repository
4. Select the `frontend` directory as root

### 4.2 Configure Build Settings

```
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### 4.3 Set Environment Variables in Vercel

```bash
# In Vercel Dashboard > Settings > Environment Variables

NEXT_PUBLIC_API_URL=https://studbud-backend-prod.us-east-1.elasticbeanstalk.com
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
```

### 4.4 Deploy Frontend

Vercel will automatically deploy when you push to the `main` branch.

For manual deployment:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

---

## Part 5: Setup GitHub Actions CI/CD

### 5.1 Add GitHub Secrets

Go to GitHub Repository > Settings > Secrets and variables > Actions

Add these secrets:
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

### 5.2 Configure Auto-Deployment

The GitHub Actions workflows are already created:
- `.github/workflows/deploy-backend.yml` - Auto-deploys backend on push to main
- `.github/workflows/test-frontend.yml` - Runs frontend tests

```bash
# Push to GitHub to trigger deployment
git add .
git commit -m "Setup AWS deployment"
git push origin main
```

---

## Part 6: Update CORS Settings

### 6.1 Update Backend CORS

After getting your Vercel URL, update the Elastic Beanstalk environment:

```bash
eb setenv ALLOWED_ORIGINS=https://your-app.vercel.app,https://custom-domain.com
```

### 6.2 Update Frontend API URL

In Vercel Dashboard, update:
```
NEXT_PUBLIC_API_URL=https://studbud-backend-prod.us-east-1.elasticbeanstalk.com
```

---

## Part 7: Domain Configuration (Optional)

### 7.1 Custom Domain for Backend

1. Go to Route 53 > Create Hosted Zone
2. Add A record pointing to Elastic Beanstalk
3. Update environment URL in EB console

### 7.2 Custom Domain for Frontend

1. In Vercel Dashboard > Settings > Domains
2. Add your custom domain
3. Update DNS records as instructed

---

## Part 8: Monitoring & Maintenance

### 8.1 Setup CloudWatch Alarms

```bash
# Create alarm for high CPU
aws cloudwatch put-metric-alarm \
  --alarm-name studbud-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ElasticBeanstalk \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### 8.2 View Logs

```bash
# Backend logs
eb logs

# Or in CloudWatch
# AWS Console > CloudWatch > Logs > /aws/elasticbeanstalk/studbud-backend-prod
```

### 8.3 Health Checks

- Backend: `https://your-backend-url.elasticbeanstalk.com/api/health`
- Frontend: Vercel automatically handles health checks

---

## Deployment Workflow

### Auto-Deployment (Recommended ✅)

1. Make code changes locally
2. Commit and push to GitHub
3. GitHub Actions automatically deploys backend
4. Vercel automatically deploys frontend
5. Check deployment status in GitHub Actions tab

### Manual Deployment (Not Recommended)

```bash
# Backend
cd backend
eb deploy

# Frontend
cd frontend
vercel --prod
```

---

## Cost Estimation (Monthly)

- **Elastic Beanstalk**: ~$15-30 (t3.small instance)
- **RDS PostgreSQL**: ~$15-25 (db.t3.micro)
- **S3 Storage**: ~$1-5 (first 50GB free)
- **Data Transfer**: ~$5-10
- **Vercel**: Free (or $20/month for Pro)
- **Total**: ~$40-70/month (excluding Vercel Pro)

---

## Troubleshooting

### Backend won't start

```bash
# Check logs
eb logs

# SSH into instance
eb ssh

# Check environment variables
eb printenv
```

### Database connection issues

```bash
# Test connection from EB instance
eb ssh
python3
>>> import psycopg2
>>> conn = psycopg2.connect(host="your-rds-endpoint", database="studbud", user="postgres", password="password")
```

### CORS errors

1. Verify `ALLOWED_ORIGINS` includes your Vercel URL
2. Check that Vercel environment variable `NEXT_PUBLIC_API_URL` is correct
3. Redeploy both frontend and backend

### S3 upload failures

1. Verify IAM user has S3 permissions
2. Check bucket name and region are correct
3. Verify CORS configuration on S3 bucket

---

## Security Best Practices

1. **Never commit `.env` files** to GitHub
2. **Use AWS Secrets Manager** for sensitive data in production
3. **Enable RDS encryption** at rest
4. **Restrict RDS security group** to only EB security group
5. **Enable CloudTrail** for audit logging
6. **Use HTTPS only** - configure SSL certificates
7. **Regular security updates** - update dependencies monthly

---

## Rollback Procedure

### Backend Rollback

```bash
# List previous versions
eb appversion lifecycle

# Deploy previous version
eb deploy --version [version-label]
```

### Frontend Rollback

1. Go to Vercel Dashboard
2. Select previous deployment
3. Click "Promote to Production"

---

## Next Steps

1. ✅ Setup monitoring alerts
2. ✅ Configure auto-scaling for EB
3. ✅ Setup CloudFront CDN for frontend
4. ✅ Implement backup strategy for RDS
5. ✅ Setup staging environment
6. ✅ Configure custom domains
7. ✅ Enable AWS WAF for security

---

## Support

For issues:
- Check logs: `eb logs` or Vercel logs
- Review GitHub Actions output
- Check AWS CloudWatch for backend metrics
- Verify all environment variables are set correctly

**Happy Deploying! 🚀**
