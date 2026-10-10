import sqlite3
import pandas as pd

DB_PATH = "financial_system.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. جدول الفروع المحسّن
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS branches (
            branch_code TEXT PRIMARY KEY,
            branch_name TEXT NOT NULL,
            country TEXT DEFAULT 'المملكة العربية السعودية',
            city TEXT,
            target REAL DEFAULT 0.0,
            status TEXT DEFAULT 'نشط'
        )
    """)
    
    # إضافة الأعمدة الجديدة تلقائياً إذا لم تكن موجودة
    for col, col_type in [("country", "TEXT DEFAULT 'المملكة العربية السعودية'"), 
                          ("city", "TEXT"), 
                          ("target", "REAL DEFAULT 0.0"), 
                          ("status", "TEXT DEFAULT 'نشط'")]:
        try:
            cursor.execute(f"ALTER TABLE branches ADD COLUMN {col} {col_type}")
        except Exception:
            pass

    # 2. جدول المدن
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT UNIQUE NOT NULL
        )
    """)
    
    # 3. جدول قائمة الدخل الموحد
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS income_statement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_code TEXT,
            year TEXT,
            month TEXT,
            account_name TEXT,
            amount REAL,
            category TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_dataframe(query, params=()):
    conn = get_connection()
    try:
        df = pd.read_sql_query(query, conn, params=params)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df

init_db()