import sqlite3
import pandas as pd
import os
import shutil
from datetime import datetime

# 1. تحديد المسار المطلق لجذر المشروع المباشر لضمان حفظ مجلد backups بجوار app.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "financial_system.db")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")

def get_connection():
    return sqlite3.connect(DB_PATH)

def auto_backup_database():
    """حفظ نسخة احتياطية فورية داخل مجلد backups بجذر المشروع عند أي تعديل مع تدوير 30 يوماً"""
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"financial_backup_{timestamp}.db")
        
        if os.path.exists(DB_PATH):
            shutil.copy2(DB_PATH, backup_path)
            
        # حذف النسخ التي تجاوزت 30 يوماً تلقائياً
        now = datetime.now()
        for filename in os.listdir(BACKUP_DIR):
            file_path = os.path.join(BACKUP_DIR, filename)
            if os.path.isfile(file_path):
                file_age_days = (now - datetime.fromtimestamp(os.path.getmtime(file_path))).days
                if file_age_days > 30:
                    os.remove(file_path)
    except Exception:
        pass

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
    
    # زرع الفروع الافتراضية عند التشغيل الأول
    seed_default_branches()

def seed_default_branches():
    """زرع الفروع الأساسية تلقائياً لمنع تصفير النظام عند إعادة التشغيل"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM branches")
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_branches = [
                ('100', 'الإدارة العامة', 'المملكة العربية السعودية', 'نجران', 0.0, 'نشط'),
                ('101', 'فرع حفر الباطن - 1', 'المملكة العربية السعودية', 'حفر الباطن', 145000.0, 'نشط'),
                ('102', 'فرع الموسى', 'المملكة العربية السعودية', 'تبوك', 80000.0, 'نشط')
            ]
            cursor.executemany("""
                INSERT OR IGNORE INTO branches (branch_code, branch_name, country, city, target, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, default_branches)
            conn.commit()
        conn.close()
    except Exception:
        pass

def execute_query(query, params=()):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()
    
    # تفعيل النسخ الاحتياطي التلقائي فور تنفيذ أي استعلام تعديل/إضافة
    auto_backup_database()

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