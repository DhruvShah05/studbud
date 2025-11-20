"""
PostgreSQL database client for AWS RDS
Replaces Supabase client for database operations
"""
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from psycopg2.pool import SimpleConnectionPool
from config import Config
from typing import Optional, List, Dict
import uuid
from datetime import datetime
from contextlib import contextmanager

# Initialize connection pool
pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=Config.DB_HOST,
    port=Config.DB_PORT,
    database=Config.DB_NAME,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    sslmode='require'
)

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        pool.putconn(conn)


# ==================== WORKSPACE OPERATIONS ====================

def create_workspace(user_id: str, name: str, description: str = "") -> dict:
    """Create a new workspace"""
    workspace_id = str(uuid.uuid4())
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO workspaces (id, user_id, name, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (workspace_id, user_id, name, description, datetime.utcnow(), datetime.utcnow()))
            
            return dict(cur.fetchone())


def get_workspaces(user_id: str) -> List[dict]:
    """Get all workspaces for a user"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM workspaces
                WHERE user_id = %s
                ORDER BY updated_at DESC
            """, (user_id,))
            
            return [dict(row) for row in cur.fetchall()]


def get_workspace(workspace_id: str) -> Optional[dict]:
    """Get a specific workspace"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM workspaces WHERE id = %s
            """, (workspace_id,))
            
            row = cur.fetchone()
            return dict(row) if row else None


def update_workspace(workspace_id: str, name: str = None, description: str = None) -> dict:
    """Update workspace details"""
    updates = ["updated_at = %s"]
    params = [datetime.utcnow()]
    
    if name:
        updates.append("name = %s")
        params.append(name)
    if description is not None:
        updates.append("description = %s")
        params.append(description)
    
    params.append(workspace_id)
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(f"""
                UPDATE workspaces
                SET {', '.join(updates)}
                WHERE id = %s
                RETURNING *
            """, params)
            
            return dict(cur.fetchone())


def delete_workspace(workspace_id: str) -> bool:
    """Delete a workspace and all associated data"""
    try:
        # First, get all source file URLs to delete from S3
        sources = get_sources(workspace_id)
        
        # Delete from database
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Delete associated data (CASCADE handles this, but explicit for clarity)
                cur.execute("DELETE FROM sources WHERE workspace_id = %s", (workspace_id,))
                cur.execute("DELETE FROM chat_history WHERE workspace_id = %s", (workspace_id,))
                cur.execute("DELETE FROM studio_outputs WHERE workspace_id = %s", (workspace_id,))
                cur.execute("DELETE FROM workspaces WHERE id = %s", (workspace_id,))
        
        # Delete files from S3 (after DB deletion to avoid orphans if DB fails)
        from utils.s3_client import delete_file_from_storage
        for source in sources:
            try:
                delete_file_from_storage(source['file_url'])
            except Exception as e:
                print(f"Warning: Failed to delete S3 file {source['file_url']}: {e}")
        
        return True
    except Exception as e:
        print(f"Error deleting workspace: {e}")
        return False


# ==================== SOURCE OPERATIONS ====================

def create_source(workspace_id: str, filename: str, file_type: str, file_url: str, extracted_text: str) -> dict:
    """Create a new source document"""
    source_id = str(uuid.uuid4())
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO sources (id, workspace_id, filename, file_type, file_url, extracted_text, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (source_id, workspace_id, filename, file_type, file_url, extracted_text, datetime.utcnow()))
            
            return dict(cur.fetchone())


def get_sources(workspace_id: str) -> List[dict]:
    """Get all sources for a workspace"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM sources
                WHERE workspace_id = %s
                ORDER BY created_at DESC
            """, (workspace_id,))
            
            return [dict(row) for row in cur.fetchall()]


def get_source(source_id: str) -> Optional[dict]:
    """Get a specific source"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM sources WHERE id = %s
            """, (source_id,))
            
            row = cur.fetchone()
            return dict(row) if row else None


def delete_source(source_id: str) -> bool:
    """Delete a source"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM sources WHERE id = %s", (source_id,))
        return True
    except Exception as e:
        print(f"Error deleting source: {e}")
        return False


def get_sources_text(source_ids: List[str]) -> str:
    """Get combined text from multiple sources"""
    if not source_ids:
        return ""
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT filename, extracted_text
                FROM sources
                WHERE id = ANY(%s::uuid[])
            """, (source_ids,))
            
            combined_text = ""
            for row in cur.fetchall():
                combined_text += f"\n\n=== SOURCE: {row['filename']} ===\n\n"
                combined_text += row['extracted_text']
            
            return combined_text


# ==================== CHAT HISTORY OPERATIONS ====================

def save_chat_message(workspace_id: str, role: str, content: str, source_ids: List[str] = None) -> dict:
    """Save a chat message"""
    message_id = str(uuid.uuid4())
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Cast source_ids to UUID array for PostgreSQL
            cur.execute("""
                INSERT INTO chat_history (id, workspace_id, role, content, source_ids, created_at)
                VALUES (%s, %s, %s, %s, %s::uuid[], %s)
                RETURNING *
            """, (message_id, workspace_id, role, content, source_ids or [], datetime.utcnow()))
            
            return dict(cur.fetchone())


def get_chat_history(workspace_id: str, limit: int = 50) -> List[dict]:
    """Get chat history for a workspace"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM chat_history
                WHERE workspace_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            """, (workspace_id, limit))
            
            return [dict(row) for row in cur.fetchall()]


def clear_chat_history(workspace_id: str) -> bool:
    """Clear chat history for a workspace"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM chat_history WHERE workspace_id = %s", (workspace_id,))
        return True
    except Exception as e:
        print(f"Error clearing chat history: {e}")
        return False


# ==================== STUDIO OUTPUTS OPERATIONS ====================

def save_studio_output(workspace_id: str, output_type: str, content: dict, source_ids: List[str] = None) -> dict:
    """Save a studio output (mindmap, flashcards, quiz, report)"""
    output_id = str(uuid.uuid4())
    
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Cast source_ids to UUID array for PostgreSQL
            cur.execute("""
                INSERT INTO studio_outputs (id, workspace_id, output_type, content, source_ids, created_at)
                VALUES (%s, %s, %s, %s, %s::uuid[], %s)
                RETURNING *
            """, (output_id, workspace_id, output_type, Json(content), source_ids or [], datetime.utcnow()))
            
            return dict(cur.fetchone())


def get_studio_outputs(workspace_id: str, output_type: str = None) -> List[dict]:
    """Get studio outputs for a workspace"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            if output_type:
                cur.execute("""
                    SELECT * FROM studio_outputs
                    WHERE workspace_id = %s AND output_type = %s
                    ORDER BY created_at DESC
                """, (workspace_id, output_type))
            else:
                cur.execute("""
                    SELECT * FROM studio_outputs
                    WHERE workspace_id = %s
                    ORDER BY created_at DESC
                """, (workspace_id,))
            
            return [dict(row) for row in cur.fetchall()]


def delete_studio_output(output_id: str) -> bool:
    """Delete a studio output"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM studio_outputs WHERE id = %s", (output_id,))
        return True
    except Exception as e:
        print(f"Error deleting studio output: {e}")
        return False


# ==================== USER OPERATIONS (for Clerk integration) ====================

def get_user_by_clerk_id(clerk_user_id: str) -> Optional[dict]:
    """Get user by Clerk user ID"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT * FROM users WHERE clerk_user_id = %s
            """, (clerk_user_id,))
            
            row = cur.fetchone()
            return dict(row) if row else None


def create_or_update_user(clerk_user_id: str, email: str, first_name: str = None, last_name: str = None) -> dict:
    """Create or update user from Clerk data"""
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO users (clerk_user_id, email, first_name, last_name, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (clerk_user_id) 
                DO UPDATE SET 
                    email = EXCLUDED.email,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    updated_at = EXCLUDED.updated_at
                RETURNING *
            """, (clerk_user_id, email, first_name, last_name, datetime.utcnow(), datetime.utcnow()))
            
            return dict(cur.fetchone())
