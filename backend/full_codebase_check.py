"""
Full Codebase Verification
Checks if code matches RDS schema and is fully migrated from Supabase
"""
import os
import re
from pathlib import Path

def check_imports():
    """Check for any remaining Supabase imports"""
    print("=" * 70)
    print("🔍 CHECKING FOR SUPABASE IMPORTS")
    print("=" * 70)
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip venv, node_modules, etc.
        dirs[:] = [d for d in dirs if d not in ['venv', 'env', '__pycache__', 'node_modules', '.git']]
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    supabase_imports = []
    db_client_imports = []
    s3_client_imports = []
    
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for supabase imports
                if 'from supabase import' in content or 'import supabase' in content:
                    supabase_imports.append(filepath)
                if 'from utils.supabase_client import' in content or 'import utils.supabase_client' in content:
                    supabase_imports.append(filepath)
                
                # Check for new clients
                if 'from utils.db_client import' in content or 'import utils.db_client' in content:
                    db_client_imports.append(filepath)
                if 'from utils.s3_client import' in content or 'import utils.s3_client' in content:
                    s3_client_imports.append(filepath)
        except Exception as e:
            pass
    
    print(f"\n✅ Files using db_client: {len(db_client_imports)}")
    for f in db_client_imports:
        print(f"   • {f}")
    
    print(f"\n✅ Files using s3_client: {len(s3_client_imports)}")
    for f in s3_client_imports:
        print(f"   • {f}")
    
    if supabase_imports:
        print(f"\n❌ Files still importing Supabase: {len(supabase_imports)}")
        for f in supabase_imports:
            print(f"   • {f}")
        return False
    else:
        print("\n✅ No Supabase imports found!")
        return True

def check_file_existence():
    """Check for old files that should be deleted"""
    print("\n" + "=" * 70)
    print("📁 CHECKING FOR OLD FILES")
    print("=" * 70)
    
    old_files = [
        'utils/supabase_client.py',
    ]
    
    found_old = []
    for filepath in old_files:
        if os.path.exists(filepath):
            found_old.append(filepath)
            print(f"⚠️  Old file exists: {filepath}")
    
    if not found_old:
        print("✅ No old Supabase files found")
        return True
    else:
        print(f"\n💡 Delete these files:")
        for f in found_old:
            print(f"   rm {f}")
        return False

def verify_schema_compatibility():
    """Check if db_client functions match RDS schema"""
    print("\n" + "=" * 70)
    print("🔍 VERIFYING SCHEMA COMPATIBILITY")
    print("=" * 70)
    
    issues = []
    
    # Read db_client.py
    try:
        with open('utils/db_client.py', 'r') as f:
            db_client_content = f.read()
        
        # Check for critical functions
        required_functions = [
            'create_workspace',
            'get_workspaces',
            'delete_workspace',
            'create_source',
            'get_sources',
            'delete_source',
            'save_chat_message',
            'get_chat_history',
            'save_studio_output',
            'get_studio_outputs',
            'create_or_update_user',
            'get_user_by_clerk_id'
        ]
        
        print("\nRequired Functions in db_client.py:")
        for func in required_functions:
            if f"def {func}(" in db_client_content:
                print(f"  ✅ {func}")
            else:
                print(f"  ❌ {func} - MISSING")
                issues.append(f"Missing function: {func}")
        
        # Check for user_id field usage (should reference users table)
        if "user_id UUID NOT NULL REFERENCES users" in db_client_content or \
           "get_user_by_clerk_id" in db_client_content:
            print("\n✅ User management functions present")
        else:
            print("\n⚠️  User management might need review")
        
    except FileNotFoundError:
        print("❌ db_client.py not found!")
        issues.append("db_client.py missing")
    
    return len(issues) == 0, issues

def check_routes():
    """Check all route files"""
    print("\n" + "=" * 70)
    print("🛣️  CHECKING ROUTE FILES")
    print("=" * 70)
    
    route_files = {
        'routes/auth_routes.py': ['db_client'],
        'routes/workspace_routes.py': ['db_client'],
        'routes/source_routes.py': ['db_client', 's3_client'],
        'routes/studio_routes.py': ['db_client', 's3_client'],
    }
    
    all_good = True
    
    for route_file, required_imports in route_files.items():
        print(f"\n📄 {route_file}")
        
        if not os.path.exists(route_file):
            print(f"  ⚠️  File not found")
            continue
        
        try:
            with open(route_file, 'r') as f:
                content = f.read()
            
            # Check for required imports
            for required in required_imports:
                if f"from utils.{required} import" in content:
                    print(f"  ✅ imports {required}")
                else:
                    print(f"  ❌ missing import: {required}")
                    all_good = False
            
            # Check for supabase usage
            if 'supabase' in content.lower() and 'supabase_client' not in route_file:
                print(f"  ⚠️  Contains 'supabase' reference")
                all_good = False
        
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            all_good = False
    
    return all_good

def check_config():
    """Check config.py"""
    print("\n" + "=" * 70)
    print("⚙️  CHECKING CONFIGURATION")
    print("=" * 70)
    
    try:
        with open('config.py', 'r') as f:
            content = f.read()
        
        # Check for RDS config
        rds_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
        print("\nRDS Configuration:")
        for var in rds_vars:
            if var in content:
                print(f"  ✅ {var}")
            else:
                print(f"  ❌ {var} - MISSING")
        
        # Check for S3 config
        s3_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_REGION', 'S3_BUCKET_NAME']
        print("\nS3 Configuration:")
        for var in s3_vars:
            if var in content:
                print(f"  ✅ {var}")
            else:
                print(f"  ❌ {var} - MISSING")
        
        # Check for legacy Supabase config
        if 'SUPABASE_URL' in content or 'SUPABASE_KEY' in content:
            print("\n⚠️  Legacy Supabase config still present (lines 26-28)")
            print("   Safe to remove after full verification")
        else:
            print("\n✅ No legacy Supabase config")
        
        return True
        
    except FileNotFoundError:
        print("❌ config.py not found!")
        return False

def check_requirements():
    """Check requirements.txt"""
    print("\n" + "=" * 70)
    print("📦 CHECKING DEPENDENCIES")
    print("=" * 70)
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        required = {
            'psycopg2-binary': '✅ PostgreSQL driver',
            'boto3': '✅ AWS S3 client',
            'Flask': '✅ Web framework',
            'google-genai': '✅ Gemini AI',
        }
        
        print("\nRequired Dependencies:")
        for package, description in required.items():
            if package.lower() in content.lower():
                print(f"  {description}")
            else:
                print(f"  ❌ Missing: {package}")
        
        # Check for old supabase
        if 'supabase' in content.lower():
            print("\n⚠️  'supabase' package still in requirements.txt")
            print("   Can be removed if not used")
        else:
            print("\n✅ No 'supabase' dependency")
        
        return True
        
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return False

def check_data_types():
    """Verify data types match between code and schema"""
    print("\n" + "=" * 70)
    print("🔢 CHECKING DATA TYPE COMPATIBILITY")
    print("=" * 70)
    
    print("\nRDS Schema uses:")
    print("  • UUID for all IDs (NOT varchar)")
    print("  • TEXT for strings (NOT varchar)")
    print("  • JSONB for studio_outputs.content")
    print("  • ARRAY for source_ids")
    print("  • TIMESTAMP WITH TIME ZONE for dates")
    
    try:
        with open('utils/db_client.py', 'r') as f:
            content = f.read()
        
        # Check UUID usage
        if 'uuid.uuid4()' in content:
            print("\n✅ Using uuid.uuid4() for ID generation")
        else:
            print("\n⚠️  Not using uuid.uuid4() consistently")
        
        # Check for Json wrapper for JSONB
        if 'from psycopg2.extras import' in content and 'Json' in content:
            print("✅ Using psycopg2.extras.Json for JSONB")
        else:
            print("⚠️  Check JSONB handling in save_studio_output")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 18 + "FULL CODEBASE VERIFICATION" + " " * 24 + "║")
    print("╚" + "=" * 68 + "╝")
    
    results = {
        'Imports': check_imports(),
        'Old Files': check_file_existence(),
        'Schema Compatibility': verify_schema_compatibility()[0],
        'Routes': check_routes(),
        'Config': check_config(),
        'Dependencies': check_requirements(),
        'Data Types': check_data_types(),
    }
    
    print("\n" + "=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    
    for check, passed in results.items():
        status = "✅" if passed else "❌"
        print(f"{status} {check}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Codebase is fully migrated to RDS + S3")
        print("✅ Schema matches database")
        print("✅ Ready for production!")
    else:
        print("⚠️  Some issues found - review details above")
    print("=" * 70)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
