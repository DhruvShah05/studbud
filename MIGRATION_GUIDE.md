# Supabase to AWS Migration Guide

## Prerequisites Checklist

- [ ] AWS Account created
- [ ] AWS CLI installed (optional but helpful)
- [ ] PostgreSQL client installed (`psql`)
- [ ] Backup of Supabase data

---

## Step-by-Step Migration Process

### 1. Set Up AWS RDS Database

1. Log into AWS Console → RDS
2. Create PostgreSQL database:
   - Engine: PostgreSQL 14+
   - Instance: `studbud-db`
   - Username: `postgres`
   - Password: (create strong password)
   - Public access: Yes (temporary, for migration)
   - Security group: Allow port 5432 from your IP
3. Wait for database to be available (~10 minutes)
4. Note the endpoint URL

### 2. Set Up AWS S3 Buckets

1. Navigate to S3 → Create bucket
2. Bucket name: `studbud-sources-prod` (must be globally unique)
3. Region: Same as RDS
4. Uncheck "Block all public access"
5. Add bucket policy (see setup guide)
6. Configure CORS (see setup guide)

### 3. Create IAM User

1. IAM → Users → Create user: `studbud-backend`
2. Attach policy: `AmazonS3FullAccess`
3. Create access key → Save credentials

### 4. Export Data from Supabase

```bash
# Export database
pg_dump -h db.YOUR_PROJECT.supabase.co \
  -U postgres \
  -d postgres \
  --no-owner \
  --no-acl \
  --clean \
  --if-exists \
  -f supabase_backup.sql

# Enter your Supabase password when prompted
```

### 5. Import Data to AWS RDS

```bash
# Import to RDS
psql -h YOUR_RDS_ENDPOINT.rds.amazonaws.com \
  -U postgres \
  -d studbud \
  -f supabase_backup.sql

# Verify import
psql -h YOUR_RDS_ENDPOINT.rds.amazonaws.com -U postgres -d studbud

# Check tables
\dt

# Check row counts
SELECT 'workspaces' as table_name, COUNT(*) FROM workspaces
UNION ALL SELECT 'sources', COUNT(*) FROM sources
UNION ALL SELECT 'users', COUNT(*) FROM users;

\q
```

### 6. Update Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cd backend
cp .env.example .env
```

2. Fill in your AWS credentials in `.env`:
```env
# AWS RDS
DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
DB_PORT=5432
DB_NAME=studbud
DB_USER=postgres
DB_PASSWORD=your_password

# AWS S3
AWS_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=studbud-sources-prod

# Keep Supabase credentials temporarily for file migration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### 7. Install New Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 8. Migrate Files from Supabase Storage to S3

```bash
# Run migration script
python migrate_storage.py
```

This will:
- Download all files from Supabase Storage
- Upload them to S3
- Update file URLs in database

### 9. Test the Migration

```bash
# Start backend
python app.py
```

Visit `http://localhost:5000/api/health` - should show:
```json
{
  "status": "healthy",
  "gemini_configured": true,
  "database_configured": true,
  "s3_configured": true,
  "s3_connection": true
}
```

### 10. Test Frontend Integration

```bash
# In another terminal
cd frontend
npm run dev
```

Test:
- [ ] User login/signup
- [ ] Create workspace
- [ ] Upload file
- [ ] Chat with sources
- [ ] Generate outputs (mindmap, flashcards, etc.)

### 11. Clean Up (After Successful Migration)

1. Remove Supabase credentials from `.env`
2. Delete `migrate_storage.py` (no longer needed)
3. Remove Supabase imports from code (if any remain)
4. Update RDS security group to restrict access
5. Consider enabling RDS Multi-AZ for production

---

## Troubleshooting

### Database Connection Issues

**Error:** `could not connect to server`
- Check RDS security group allows your IP on port 5432
- Verify endpoint URL is correct
- Ensure RDS instance is "Available"

**Error:** `password authentication failed`
- Double-check DB_PASSWORD in .env
- Ensure no extra spaces in credentials

### S3 Upload Issues

**Error:** `Access Denied`
- Verify IAM user has S3 permissions
- Check bucket policy allows public read
- Ensure AWS credentials are correct

**Error:** `Bucket does not exist`
- Verify S3_BUCKET_NAME matches actual bucket name
- Check bucket is in correct region

### Migration Script Issues

**Error:** `No module named 'boto3'`
```bash
pip install boto3
```

**Error:** `No module named 'supabase'`
```bash
pip install supabase
```

---

## Rollback Plan

If migration fails:

1. Keep Supabase running (don't delete data)
2. Revert code changes:
```bash
git checkout HEAD -- backend/
```
3. Restore original `.env` with Supabase credentials
4. Restart backend with Supabase

---

## Cost Monitoring

After migration, monitor AWS costs:

1. AWS Console → Billing Dashboard
2. Set up billing alerts:
   - Threshold: $50/month (adjust as needed)
3. Monitor RDS and S3 usage in CloudWatch

---

## Next Steps After Migration

1. **Security Hardening:**
   - Restrict RDS security group to backend server IP only
   - Enable RDS encryption at rest
   - Use AWS Secrets Manager for credentials

2. **Performance Optimization:**
   - Set up RDS read replicas if needed
   - Enable S3 CloudFront CDN
   - Configure RDS connection pooling

3. **Backup Strategy:**
   - Enable RDS automated backups (7-30 days)
   - Set up S3 versioning
   - Test restore procedures

4. **Monitoring:**
   - Set up CloudWatch alarms
   - Monitor RDS performance metrics
   - Track S3 storage costs

---

## Support

If you encounter issues:
1. Check AWS service health dashboard
2. Review CloudWatch logs
3. Verify all environment variables are set correctly
4. Ensure security groups and IAM permissions are configured properly
