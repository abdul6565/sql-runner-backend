import sqlite3
from typing import List, Dict, Any, Optional
from config import settings


def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(settings.database_url)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def close_db_connection(conn):
    """Close database connection."""
    if conn:
        conn.close()


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Execute a SQL query and return results as list of dictionaries.

    Args:
        query: SQL query string
        params: Query parameters

    Returns:
        List of dictionaries representing query results
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.commit()  # For INSERT, UPDATE, DELETE operations
        return [dict(row) for row in results]
    except sqlite3.Error as e:
        raise Exception(f"Database error: {str(e)}")
    finally:
        close_db_connection(conn)


def get_table_names() -> List[str]:
    """Get list of all table names in the database."""
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    results = execute_query(query)
    return [row['name'] for row in results]


def get_table_info(table_name: str) -> Dict[str, Any]:
    """
    Get schema and sample data for a specific table.

    Args:
        table_name: Name of the table

    Returns:
        Dictionary with columns and sample data
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get column information
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [{"name": row[1], "type": row[2]} for row in cursor.fetchall()]

        # Get sample data (first 5 rows)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
        sample_data = [dict(row) for row in cursor.fetchall()]

        return {
            "columns": columns,
            "sample_data": sample_data
        }
    except sqlite3.Error as e:
        raise Exception(f"Error getting table info: {str(e)}")
    finally:
        close_db_connection(conn)


def create_user(username: str, hashed_password: str) -> bool:
    """Create a new user in the database."""
    query = """
    INSERT INTO users (username, password, created_at, last_login)
    VALUES (?, ?, datetime('now'), datetime('now'))
    """
    try:
        execute_query(query, (username, hashed_password))
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get user by username."""
    query = "SELECT * FROM users WHERE username = ?"
    results = execute_query(query, (username,))
    return results[0] if results else None


def update_user_last_login(username: str):
    """Update user's last login timestamp."""
    query = "UPDATE users SET last_login = datetime('now') WHERE username = ?"
    execute_query(query, (username,))


def save_query_history(username: str, query: str, result: List[Dict[str, Any]]):
    """Save query execution history."""
    query_insert = """
    INSERT INTO recent_queries (username, query, result, created_at)
    VALUES (?, ?, ?, datetime('now'))
    """
    execute_query(query_insert, (username, query, str(result)))


def get_recent_queries(username: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get recent queries for a user."""
    query = """
    SELECT query, result, created_at as timestamp
    FROM recent_queries
    WHERE username = ?
    ORDER BY created_at DESC
    LIMIT ?
    """
    return execute_query(query, (username, limit))


def get_user_profile(username: str) -> Optional[Dict[str, Any]]:
    """Get user profile information."""
    query = """
    SELECT username, created_at, last_login,
           (SELECT COUNT(*) FROM recent_queries WHERE username = u.username) as total_queries
    FROM users u
    WHERE username = ?
    """
    results = execute_query(query, (username,))
    return results[0] if results else None
