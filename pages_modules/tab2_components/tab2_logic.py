import pandas as pd
import re
from utils.db_manager import execute_query

def clean_float(val):
    """تنظيف واستخراج الأرقام بدقة متناهية"""
    if pd.isna(val): return 0.0
    if isinstance(val, (int, float)): return float(val)
    cleaned = re.sub(r'[^\d.-]', '', str(val))
    try: return float(cleaned) if cleaned else 0.0
    except: return 0.0

def process_excel_preview(df_excel, col_acc, col_debit, col_credit, doc_type="income"):
    """معالجة الملف ومطابقتها فورياً واستبعاد حسابات المركز المالي إذا كان ميزان مراجعة"""
    rows_valid, total_rev, total_exp = 0, 0.0, 0.0
    records = []
    
    # الكلمات التي تعبر عن حسابات الميزانية العمومية لاستبعادها في حالة اختيار ميزان المراجعة
    balance_sheet_keywords = ["بنك", "صندوق", "عملاء", "موردين", "أصول", "التزامات", "رأس المال", "نقدية", "مخزون", "عهد"]

    for _, row in df_excel.iterrows():
        acc_val = row[col_acc]
        if pd.isna(acc_val): continue
        acc_name = str(acc_val).strip()
        
        # استبعاد العناوين والتكيف مع ميزان المراجعة
        if acc_name in ["None", "nan", ""] or any(k == acc_name for k in ["الاسم", "اسم الحساب", "رقم الحساب"]):
            continue
            
        if doc_type == "trial_balance" and any(k in acc_name for k in balance_sheet_keywords):
            continue

        val_debit = clean_float(row[col_debit])
        val_credit = clean_float(row[col_credit])

        if val_debit > 0:
            total_exp += val_debit
            records.append((acc_name, val_debit, "مصروفات"))
            rows_valid += 1
        if val_credit > 0:
            total_rev += val_credit
            records.append((acc_name, val_credit, "إيرادات"))
            rows_valid += 1

    net_profit = total_rev - total_exp
    margin_pct = (net_profit / total_rev * 100) if total_rev > 0 else 0.0
    
    return rows_valid, total_rev, total_exp, net_profit, margin_pct, records

def delete_import_data(del_branches, del_months):
    if not del_months: return False
    selected_codes = [b.split(" - ")[0] for b in del_branches if "جميع الفروع" not in b]
    for m in del_months:
        if "جميع الفروع" in del_branches or not selected_codes:
            execute_query("DELETE FROM income_statement WHERE month = ?", (m,))
        else:
            for code in selected_codes:
                execute_query("DELETE FROM income_statement WHERE month = ? AND branch_code = ?", (m, code))
    return True