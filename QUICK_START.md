# Quick Start: Database & Storage Migration

## Prerequisites
- AWS Account
- PostgreSQL client (`brew install postgresql` on macOS)
- Python 3.8+

---

## Quick Migration Steps

### 1. AWS Setup (30 minutes)

#### Create RDS Database
```bash
# AWS Console → RDS → Create Database
# - Engine: PostgreSQL 14+
# - Instance: db.t3.micro (free tier) or db.t3.small
# - Public access: Yes
# - Security group: Allow 5432 from your IP
# - Note the endpoint URL
```

#### Create S3 Bucket
```bash
# AWS Console → S3 → Create Bucket
# - Name: studbud-sources-prod (must be unique)
# - Uncheck "Block all public access"
# - Add bucket policy and CORS (see MIGRATION_GUIDE.md)
```

#### Create IAM User
```bash
# AWS Console → IAM → Users → Create
# - Name: studbud-backend
# - Attach: AmazonS3FullAccess
# - Create access key → Save credentials
```

---

### 2. Export from Supabase (10 minutes)

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
```

---

### 3. Import to RDS (10 minutes)

```bash
# Import to RDS
psql -h YOUR_RDS_ENDPOINT.rds.amazonaws.com \
  -U postgres \
  -d studbud \
  -f supabase_backup.sql

# Verify
psql -h YOUR_RDS_ENDPOINT.rds.amazonaws.com -U postgres -d studbud
\dt
\q
```

---

### 4. Configure Environment (5 minutes)

```bash
cd backend

# Copy template
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Fill in:
```env
DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
DB_PASSWORD=your_db_password
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=studbud-sources-prod
```

---

### 5. Install Dependencies (2 minutes)

```bash
cd backend
pip install -r requirements.txt
```

---

### 6. Migrate Files to S3 (10-30 minutes)

```bash
# Run migration script
python migrate_storage.py
```

This will:
- ✅ Download files from Supabase
- ✅ Upload to S3
- ✅ Update database URLs

---

### 7. Test Everything (10 minutes)

```bash
# Start backend
python app.py

# In another terminal, check health
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "gemini_configured": true,
  "database_configured": true,
  "s3_configured": true,
  "s3_connection": true
}
```

---

### 8. Test Frontend (5 minutes)

```bash
# In another terminal
cd frontend
npm run dev
```

Test:
- ✅ Login
- ✅ Create workspace
- ✅ Upload file
- ✅ Chat
- ✅ Generate outputs

---

## Troubleshooting

### Can't connect to RDS
```bash
# Check security group allows your IP
# AWS Console → RDS → Your DB → Security Group → Edit Inbound Rules
# Add: PostgreSQL (5432) from your IP
```

### S3 upload fails
```bash
# Verify bucket policy allows public read
# S3 → Your Bucket → Permissions → Bucket Policy
# (See MIGRATION_GUIDE.md for policy)
```

### Migration script errors
```bash
# Install missing packages
pip install boto3 supabase requests psycopg2-binary
```

---

## After Successful Migration

1. ✅ Remove Supabase credentials from `.env`
2. ✅ Delete `migrate_storage.py`
3. ✅ Update RDS security group (restrict to backend IP only)
4. ✅ Set up CloudWatch monitoring
5. ✅ Enable RDS automated backups

---

## Need Help?

- **Detailed Guide:** See `MIGRATION_GUIDE.md`
- **Code Changes:** See `MIGRATION_SUMMARY.md`
- **AWS Issues:** Check AWS service health dashboard
- **Database Issues:** Review RDS logs in CloudWatch

---

## Rollback

If something goes wrong:
1. Keep Supabase running (don't delete)
2. Revert code: `git checkout HEAD -- backend/`
3. Restore original `.env`
4. Restart with Supabase

---

## Total Time: ~1.5-2 hours

Good luck! 🚀
