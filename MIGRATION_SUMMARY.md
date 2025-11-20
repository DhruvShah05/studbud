# Migration Summary: Supabase → AWS

## What Changed

### Database
- **Before:** Supabase PostgreSQL
- **After:** AWS RDS PostgreSQL
- **Client:** `supabase` Python SDK → `psycopg2-binary`

### Storage
- **Before:** Supabase Storage buckets
- **After:** AWS S3 buckets
- **Client:** `supabase.storage` → `boto3` (AWS SDK)

### Code Changes
- ✅ New file: `backend/utils/db_client.py` - PostgreSQL database operations
- ✅ New file: `backend/utils/s3_client.py` - S3 storage operations
- ✅ Updated: `backend/config.py` - AWS credentials
- ✅ Updated: `backend/requirements.txt` - New dependencies
- ✅ Updated: All route files to use new clients
- ✅ Created: `backend/migrate_storage.py` - One-time migration script
- ✅ Created: `backend/.env.example` - Environment template

---

## Files Modified

1. **backend/requirements.txt**
   - Removed: `supabase==2.9.0`
   - Added: `psycopg2-binary==2.9.9`, `boto3==1.34.34`, `requests==2.31.0`

2. **backend/config.py**
   - Added AWS RDS configuration
   - Added AWS S3 configuration
   - Kept Supabase config for migration only

3. **backend/app.py**
   - Updated health check to verify AWS services

4. **backend/routes/workspace_routes.py**
   - Changed imports from `supabase_client` to `db_client`
   - Updated helper functions

5. **backend/routes/source_routes.py**
   - Changed imports to use `db_client` and `s3_client`
   - Updated file upload to use S3

6. **backend/routes/auth_routes.py**
   - Simplified using new `db_client` functions
   - Removed session management (not needed)

7. **backend/routes/studio_routes.py**
   - Changed imports from `supabase_client` to `db_client`
   - Updated audio upload to use S3

---

## Migration Checklist

### AWS Setup
- [ ] Create RDS PostgreSQL instance
- [ ] Create S3 bucket(s)
- [ ] Create IAM user with S3 access
- [ ] Configure security groups
- [ ] Note all credentials

### Data Migration
- [ ] Export Supabase database using `pg_dump`
- [ ] Import to RDS using `psql`
- [ ] Verify data integrity
- [ ] Run `migrate_storage.py` to move files to S3
- [ ] Verify file URLs updated in database

### Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Fill in all AWS credentials
- [ ] Update `DB_HOST`, `DB_PASSWORD`
- [ ] Update `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- [ ] Update `S3_BUCKET_NAME`

### Testing
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Start backend: `python app.py`
- [ ] Check health endpoint: `/api/health`
- [ ] Test user authentication
- [ ] Test workspace creation
- [ ] Test file upload
- [ ] Test chat functionality
- [ ] Test all studio features

### Cleanup
- [ ] Remove Supabase credentials from `.env`
- [ ] Delete `migrate_storage.py`
- [ ] Update RDS security group (restrict access)
- [ ] Set up CloudWatch monitoring
- [ ] Configure automated backups

---

## Environment Variables Required

```env
# Required for AWS
DB_HOST=your-rds-endpoint.region.rds.amazonaws.com
DB_PASSWORD=your_db_password
AWS_ACCESS_KEY_ID=AKIAXXXXXXXX
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=studbud-sources-prod

# Optional (with defaults)
DB_PORT=5432
DB_NAME=studbud
DB_USER=postgres
AWS_REGION=us-east-1

# Keep temporarily for migration
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
```

---

## Key Differences

### Database Queries
**Before (Supabase):**
```python
result = supabase.table('workspaces').select('*').eq('user_id', user_id).execute()
workspaces = result.data
```

**After (PostgreSQL):**
```python
with get_db_connection() as conn:
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM workspaces WHERE user_id = %s", (user_id,))
        workspaces = [dict(row) for row in cur.fetchall()]
```

### File Storage
**Before (Supabase):**
```python
result = supabase.storage.from_("sources").upload(file_path, file_bytes)
public_url = supabase.storage.from_("sources").get_public_url(file_path)
```

**After (S3):**
```python
s3_client.put_object(Bucket=S3_BUCKET, Key=s3_key, Body=file_bytes)
public_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
```

---

## Benefits of AWS Migration

1. **Scalability:** Auto-scaling, larger instance types available
2. **Reliability:** 99.99% SLA, Multi-AZ support
3. **Performance:** Global CDN with CloudFront
4. **Control:** Full database access, custom configurations
5. **Ecosystem:** Integration with 200+ AWS services
6. **Cost:** Potentially lower at scale with reserved instances

---

## Estimated Costs (Monthly)

**Development:**
- RDS (db.t3.micro): ~$15-20
- S3 (10GB): ~$0.50
- Data transfer: ~$1
- **Total: ~$20-25/month**

**Production:**
- RDS (db.t3.medium, Multi-AZ): ~$120-150
- S3 (100GB): ~$2.50
- CloudFront: ~$10-20
- **Total: ~$150-200/month**

---

## Timeline

- **AWS Setup:** 1-2 hours
- **Data Migration:** 1-2 hours
- **Code Testing:** 2-3 hours
- **Deployment:** 1 hour
- **Total:** ~1 day for complete migration

---

## Support Resources

- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

## Next Steps

1. Follow `MIGRATION_GUIDE.md` for detailed instructions
2. Set up AWS services
3. Run migration scripts
4. Test thoroughly
5. Deploy to production
6. Monitor and optimize
