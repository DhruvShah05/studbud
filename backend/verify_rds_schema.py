"""
RDS Schema Verification Script
Checks if your RDS database has the correct schema
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def test_connection():
    """Test basic RDS connection"""
    print("=" * 70)
    print("🔍 TESTING RDS CONNECTION")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            sslmode='require',
            connect_timeout=10
        )
        
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"✅ Connection Successful!")
            print(f"📊 Database: {Config.DB_NAME}")
            print(f"🖥️  Host: {Config.DB_HOST}")
            print(f"📝 Version: {version[:50]}...")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection Failed!")
        print(f"Error: {e}")
        return False

def check_tables():
    """Check which tables exist"""
    print("\n" + "=" * 70)
    print("📋 CHECKING TABLES")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            sslmode='require'
        )
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get all tables in public schema
            cur.execute("""
                SELECT table_name, 
                       (SELECT COUNT(*) FROM information_schema.columns 
                        WHERE table_schema = 'public' AND table_name = t.table_name) as column_count
                FROM information_schema.tables t
                WHERE table_schema = 'public'
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name;
            """)
            
            tables = cur.fetchall()
            
            expected_tables = ['users', 'workspaces', 'sources', 'chat_history', 'studio_outputs', 'user_sessions']
            
            print(f"\n📊 Tables Found: {len(tables)}")
            print("-" * 70)
            
            found_tables = []
            for table in tables:
                found_tables.append(table['table_name'])
                print(f"  ✅ {table['table_name']:30} ({table['column_count']} columns)")
            
            # Check for missing tables
            missing = [t for t in expected_tables if t not in found_tables]
            if missing:
                print("\n⚠️  Missing Tables:")
                for table in missing:
                    print(f"  ❌ {table}")
            else:
                print(f"\n✅ All {len(expected_tables)} expected tables exist!")
            
            # Check for extra tables
            extra = [t for t in found_tables if t not in expected_tables]
            if extra:
                print("\n📌 Additional Tables:")
                for table in extra:
                    print(f"  ℹ️  {table}")
        
        conn.close()
        return found_tables, missing
        
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return [], []

def check_table_schema(table_name):
    """Check detailed schema for a specific table"""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            sslmode='require'
        )
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Get columns
            cur.execute("""
                SELECT 
                    column_name,
                    data_type,
                    character_maximum_length,
                    is_nullable,
                    column_default
                FROM information_schema.columns
                WHERE table_schema = 'public' 
                  AND table_name = %s
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cur.fetchall()
            
            # Get constraints
            cur.execute("""
                SELECT
                    con.conname as constraint_name,
                    con.contype as constraint_type,
                    CASE con.contype
                        WHEN 'p' THEN 'PRIMARY KEY'
                        WHEN 'f' THEN 'FOREIGN KEY'
                        WHEN 'u' THEN 'UNIQUE'
                        WHEN 'c' THEN 'CHECK'
                    END as constraint_description
                FROM pg_constraint con
                JOIN pg_class rel ON rel.oid = con.conrelid
                JOIN pg_namespace nsp ON nsp.oid = rel.relnamespace
                WHERE nsp.nspname = 'public'
                  AND rel.relname = %s;
            """, (table_name,))
            
            constraints = cur.fetchall()
            
            return columns, constraints
        
    except Exception as e:
        print(f"Error checking schema for {table_name}: {e}")
        return [], []
    finally:
        if conn:
            conn.close()

def verify_all_schemas():
    """Verify schema for all tables"""
    print("\n" + "=" * 70)
    print("🔍 DETAILED SCHEMA VERIFICATION")
    print("=" * 70)
    
    expected_schemas = {
        'users': {
            'columns': ['id', 'clerk_user_id', 'email', 'first_name', 'last_name', 
                       'profile_image_url', 'created_at', 'updated_at', 'last_login'],
            'must_have': ['id', 'clerk_user_id', 'email']
        },
        'workspaces': {
            'columns': ['id', 'name', 'description', 'created_at', 'updated_at', 'user_id'],
            'must_have': ['id', 'name', 'user_id']
        },
        'sources': {
            'columns': ['id', 'workspace_id', 'filename', 'file_type', 'file_url', 
                       'extracted_text', 'created_at'],
            'must_have': ['id', 'workspace_id', 'filename', 'file_url']
        },
        'chat_history': {
            'columns': ['id', 'workspace_id', 'role', 'content', 'source_ids', 'created_at'],
            'must_have': ['id', 'workspace_id', 'role', 'content']
        },
        'studio_outputs': {
            'columns': ['id', 'workspace_id', 'output_type', 'content', 'source_ids', 'created_at'],
            'must_have': ['id', 'workspace_id', 'output_type', 'content']
        },
        'user_sessions': {
            'columns': ['id', 'user_id', 'clerk_session_id', 'ip_address', 'user_agent', 
                       'created_at', 'expires_at', 'is_active'],
            'must_have': ['id', 'clerk_session_id']
        }
    }
    
    all_good = True
    
    for table_name, expected in expected_schemas.items():
        print(f"\n📊 Table: {table_name.upper()}")
        print("-" * 70)
        
        columns, constraints = check_table_schema(table_name)
        
        if not columns:
            print(f"  ❌ Table does not exist or is empty")
            all_good = False
            continue
        
        # Check columns
        actual_columns = [col['column_name'] for col in columns]
        
        print(f"  Columns ({len(actual_columns)}):")
        for col in columns:
            nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT {col['column_default']}" if col['column_default'] else ""
            print(f"    • {col['column_name']:20} {col['data_type']:15} {nullable:10}{default}")
        
        # Check for missing required columns
        missing_cols = [c for c in expected['must_have'] if c not in actual_columns]
        if missing_cols:
            print(f"  ❌ Missing required columns: {', '.join(missing_cols)}")
            all_good = False
        
        # Check constraints
        if constraints:
            print(f"\n  Constraints ({len(constraints)}):")
            for con in constraints:
                print(f"    • {con['constraint_description']:15} {con['constraint_name']}")
        
        print(f"  {'✅ Schema OK' if not missing_cols else '❌ Schema Issues'}")
    
    return all_good

def check_extensions():
    """Check if required PostgreSQL extensions are enabled"""
    print("\n" + "=" * 70)
    print("🔌 CHECKING POSTGRESQL EXTENSIONS")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            sslmode='require'
        )
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT extname, extversion FROM pg_extension ORDER BY extname;")
            extensions = cur.fetchall()
            
            print(f"\nInstalled Extensions: {len(extensions)}")
            for ext in extensions:
                print(f"  ✅ {ext['extname']:25} (v{ext['extversion']})")
            
            # Check for uuid-ossp
            ext_names = [e['extname'] for e in extensions]
            if 'uuid-ossp' not in ext_names:
                print("\n⚠️  WARNING: 'uuid-ossp' extension not found")
                print("   This is needed for UUID generation")
                print("   Run: CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        
        conn.close()
        
    except Exception as e:
        print(f"Error checking extensions: {e}")

def get_row_counts():
    """Get row counts for all tables"""
    print("\n" + "=" * 70)
    print("📊 ROW COUNTS")
    print("=" * 70)
    
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            sslmode='require'
        )
        
        tables = ['users', 'workspaces', 'sources', 'chat_history', 'studio_outputs', 'user_sessions']
        
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            print("")
            for table in tables:
                try:
                    cur.execute(f"SELECT COUNT(*) as count FROM {table};")
                    result = cur.fetchone()
                    count = result['count']
                    
                    emoji = "📦" if count == 0 else "📊"
                    print(f"  {emoji} {table:25} {count:>6} rows")
                except Exception as e:
                    print(f"  ❌ {table:25} Error: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting row counts: {e}")

def main():
    """Run all verification checks"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "RDS SCHEMA VERIFICATION TOOL" + " " * 25 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Test connection
    if not test_connection():
        print("\n❌ Cannot proceed - connection failed")
        return
    
    # Check tables
    found_tables, missing_tables = check_tables()
    
    if not found_tables:
        print("\n❌ No tables found in database")
        print("\n💡 You need to run the schema creation SQL:")
        print("   psql -h studbud-db.cofwacuk4ltf.us-east-1.rds.amazonaws.com \\")
        print("        -U postgres -d postgres -f backend/rds_schema.sql")
        return
    
    # Verify schemas
    schema_ok = verify_all_schemas()
    
    # Check extensions
    check_extensions()
    
    # Get row counts
    get_row_counts()
    
    # Final summary
    print("\n" + "=" * 70)
    print("📋 FINAL SUMMARY")
    print("=" * 70)
    
    if missing_tables:
        print(f"❌ Missing {len(missing_tables)} tables")
        print("   Need to create schema")
    elif schema_ok:
        print("✅ Database schema is correct and complete!")
        print("✅ All tables exist with proper structure")
        print("✅ Ready for use!")
    else:
        print("⚠️  Database exists but has schema issues")
        print("   Review the details above")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
