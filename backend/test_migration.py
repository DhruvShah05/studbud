"""
Test script to verify Supabase to RDS/S3 migration
Run: python test_migration.py
"""
import os
from config import Config
from utils.db_client import get_db_connection
from utils.s3_client import check_s3_connection

def test_rds_connection():
    """Test RDS PostgreSQL connection"""
    print("🔍 Testing RDS connection...")
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"✅ RDS Connected: {version}")
                
                # Check tables exist
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name;
                """)
                tables = [row[0] for row in cur.fetchall()]
                print(f"✅ Tables found: {', '.join(tables)}")
                
                expected_tables = ['users', 'workspaces', 'sources', 'chat_history', 'studio_outputs']
                missing = [t for t in expected_tables if t not in tables]
                if missing:
                    print(f"⚠️  Missing tables: {', '.join(missing)}")
                    print("   Run: psql -h <host> -U <user> -d studbud -f backend/rds_schema.sql")
                else:
                    print("✅ All required tables exist")
                    
        return True
    except Exception as e:
        print(f"❌ RDS Connection Failed: {e}")
        return False

def test_s3_connection():
    """Test S3 bucket connection"""
    print("\n🔍 Testing S3 connection...")
    try:
        if check_s3_connection():
            print(f"✅ S3 Connected: {Config.S3_BUCKET_NAME}")
            return True
        else:
            print(f"❌ S3 Connection Failed")
            return False
    except Exception as e:
        print(f"❌ S3 Error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n🔍 Checking configuration...")
    
    checks = {
        "DB_HOST": Config.DB_HOST,
        "DB_NAME": Config.DB_NAME,
        "DB_USER": Config.DB_USER,
        "DB_PASSWORD": bool(Config.DB_PASSWORD),
        "AWS_ACCESS_KEY_ID": bool(Config.AWS_ACCESS_KEY_ID),
        "AWS_SECRET_ACCESS_KEY": bool(Config.AWS_SECRET_ACCESS_KEY),
        "S3_BUCKET_NAME": Config.S3_BUCKET_NAME,
        "GEMINI_API_KEY": bool(Config.GEMINI_API_KEY),
    }
    
    all_good = True
    for key, value in checks.items():
        if value:
            print(f"✅ {key}: {'***' if 'PASSWORD' in key or 'KEY' in key else value}")
        else:
            print(f"❌ {key}: NOT SET")
            all_good = False
    
    return all_good

def check_old_supabase():
    """Check for old Supabase references"""
    print("\n🔍 Checking for old Supabase code...")
    
    supabase_file = "utils/supabase_client.py"
    if os.path.exists(supabase_file):
        print(f"⚠️  Old file exists: {supabase_file}")
        print("   Delete with: rm backend/utils/supabase_client.py")
    else:
        print("✅ No old Supabase client file")
    
    if Config.SUPABASE_URL or Config.SUPABASE_KEY:
        print("⚠️  Supabase config still in config.py (lines 26-28)")
        print("   Remove after verifying everything works")
    else:
        print("✅ No Supabase config found")

def main():
    print("=" * 60)
    print("🧪 StudBud Migration Test Suite")
    print("=" * 60)
    
    config_ok = test_config()
    rds_ok = test_rds_connection()
    s3_ok = test_s3_connection()
    check_old_supabase()
    
    print("\n" + "=" * 60)
    if config_ok and rds_ok and s3_ok:
        print("✅ Migration Complete! All systems operational.")
    else:
        print("⚠️  Migration incomplete. Fix issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
