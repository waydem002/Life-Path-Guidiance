import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "profiles.db")

def init_db():
    """Initializes the SQLite database with the standard profile_cache schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profile_cache (
            name TEXT,
            dob TEXT,
            language TEXT,
            focus_area TEXT,
            interpretation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (name, dob, language, focus_area)
        )
    """)
    conn.commit()
    conn.close()


def get_cached_profile(name: str, dob: str, language: str, focus_area: str = "General Life Path & Guidance"):
    """Fetches cached profile text based on user parameters."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Ensure table structure exists before query
    init_db()
    
    cursor.execute(
        "SELECT interpretation FROM profile_cache WHERE name=? AND dob=? AND language=? AND focus_area=?", 
        (name, dob, language, focus_area)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def save_profile_to_cache(name: str, dob: str, language: str, focus_area: str, interpretation: str):
    """Saves or updates a profile interpretation entry in the SQLite cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    init_db()
    
    cursor.execute("""
        INSERT OR REPLACE INTO profile_cache (name, dob, language, focus_area, interpretation)
        VALUES (?, ?, ?, ?, ?)
    """, (name, dob, language, focus_area, interpretation))
    
    conn.commit()
    conn.close()


def fetch_profiles_history():
    """Fetches recent profiles for the sidebar history component."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        init_db()
        cursor.execute("""
            SELECT name, dob, language, focus_area 
            FROM profile_cache 
            ORDER BY rowid DESC 
            LIMIT 10
        """)
        rows = cursor.fetchall()
        conn.close()
        return [
            {"name": row[0], "dob": row[1], "language": row[2], "focus_area": row[3]} 
            for row in rows
        ]
    except Exception:
        conn.close()
        return []