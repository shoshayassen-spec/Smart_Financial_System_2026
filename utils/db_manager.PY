import sqlite3
import pandas as pd
import json
import os

DB_PATH = "database/financial_system.db"

def init_db():
    os.makedirs("database", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # جدول تكويد الفروع (البند 12)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS branches (
            branch_code TEXT PRIMARY KEY,
            branch_name TEXT NOT NULL,
            city TEXT NOT NULL,
            target REAL DEFAULT 0.0,
            status TEXT DEFAULT 'نشط'
        )
    ''')
    
    # جدول بيانات قائمة الدخل وحركات الفروع الشهري (البند 3 و 10)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS income_statement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            branch_code TEXT,
            month TEXT,
            account_name TEXT,
            amount REAL,
            category TEXT,
            FOREIGN KEY (branch_code) REFERENCES branches (branch_code)
        )
    ''')
    
    # جدول تتبع حالة سحب الشهور مجمدة/مفتوحة (البند 10)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS month_status (
            month TEXT PRIMARY KEY,
            is_locked INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def get_dataframe(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def clear_system_memory():
    """تفريغ كافة البيانات والذاكرة الخاصة بالنظام (البند 9)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM income_statement")
    cursor.execute("DELETE FROM month_status")
    conn.commit()
    conn.close()