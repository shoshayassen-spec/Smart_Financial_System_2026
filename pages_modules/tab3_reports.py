import streamlit as st
import pandas as pd
from utils.db_manager import get_dataframe, execute_query

from pages_modules.tab3_components.tab3_styles import apply_tab3_styles
from pages_modules.tab3_components.tab3_ui import render_control_bar, render_executive_cards
from pages_modules.tab3_components.tab3_templates import render_templates, get_available_templates

MONTHS = ["يناير 2026", "فبراير 2026", "مارس 2026", "أبريل 2026", "مايو 2026", "يونيو 2026", 
          "يوليو 2026", "أغسطس 2026", "سبتمبر 2026", "أكتوبر 2026", "نوفمبر 2026", "ديسمبر 2026"]

def categorize_expense(acc_name):
    """تصنيف المصروفات تلقائياً حسب طبيعة الحساب"""
    acc = str(acc_name).lower()
    if any(k in acc for k in ['تكلفة المبيعات', 'المشتريات', 'تكلفة البضاعة', 'مواد خام']):
        return 'تكلفة المبيعات (COGS)', 'متغيرة'
    elif any(k in acc for k in ['تسويق', 'دعاية', 'إعلان', 'ترويج', 'حملة']):
        return 'دعاية وإعلان وتطبيق', 'متغيرة'
    elif any(k in acc for k in ['رواتب', 'إيجار', 'تأمين', 'استهلاك', 'إهلاك']):
        return 'عمومية وإدارية', 'ثابتة'
    else:
        return 'مصروفات تشغيلية أخرى', 'ثابتة'

def render():
    # ضمان وجود عمود year بدون أن يحدث خطأ
    try:
        execute_query("ALTER TABLE income_statement ADD COLUMN year TEXT DEFAULT '2026'")
    except Exception:
        pass

    available = get_available_templates()
    st.session_state['template_list'] = list(available.keys()) if available else []

    apply_tab3_styles()

    st.markdown("<div class='main-page-title no-print'>📊 منصة التحليل المالي المتقدم واستعلام تقارير الفروع</div>", unsafe_allow_html=True)

    branches_df = get_dataframe("SELECT branch_code, branch_name, city, target FROM branches")
    if branches_df.empty:
        st.warning("⚠️ لا توجد فروع مسجلة! يرجى إضافة الفروع أولاً.")
        return

    # 2. عرض شريط التحكم
    selected_b_code, b_name, b_city, b_target, selected_month_full, selected_month, selected_template, show_math = render_control_bar(branches_df, MONTHS)

    clean_month = selected_month_full.split(" ")[0].strip()
    clean_code = str(selected_b_code).strip()

    # 3. جلب بيانات الفرع والشهر بمرونة كاملة تتوافق مع جميع البنيات
    df_data = get_dataframe("""
        SELECT account_name, amount, category, branch_code, month
        FROM income_statement 
        WHERE TRIM(branch_code) = ? AND (TRIM(month) = ? OR TRIM(month) = ?)
    """, (clean_code, clean_month, selected_month_full))

    if df_data.empty:
        df_all = get_dataframe("SELECT account_name, amount, category, branch_code, month FROM income_statement")
        if not df_all.empty:
            df_data = df_all[
                (df_all['branch_code'].astype(str).str.contains(clean_code)) & 
                (df_all['month'].astype(str).str.contains(clean_month))
            ].copy()

    if df_data.empty:
        st.warning(f"🚨 لا توجد بيانات مالية مسحوبة لـ **[{b_name}]** عن **{selected_month_full}**.")
        return

    rev_df = df_data[df_data['category'] == 'إيرادات'].copy()
    exp_df = df_data[df_data['category'] == 'مصروفات'].copy()

    exp_df[['تصنيف_الميزانية', 'طبيعة_التكلفة']] = exp_df['account_name'].apply(lambda x: pd.Series(categorize_expense(x)))

    total_revenue = float(rev_df['amount'].sum())
    total_expense = float(exp_df['amount'].sum())
    net_profit = total_revenue - total_expense

    variable_costs = float(exp_df[exp_df['طبيعة_التكلفة'] == 'متغيرة']['amount'].sum())
    fixed_costs = float(exp_df[exp_df['طبيعة_التكلفة'] == 'ثابتة']['amount'].sum())

    cogs_row = exp_df[exp_df['تصنيف_الميزانية'] == 'تكلفة المبيعات (COGS)']
    cogs_amount = float(cogs_row['amount'].sum()) if not cogs_row.empty else (total_expense * 0.45)
    cogs_ratio = (cogs_amount / total_revenue * 100) if total_revenue > 0 else 0.0

    target_achieved = (total_revenue / b_target * 100) if b_target > 0 else 0.0
    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    opex_ratio = (total_expense / total_revenue * 100) if total_revenue > 0 else 0.0
    
    cost_per_sales_riyal = (total_expense / total_revenue) if total_revenue > 0 else 0.0
    return_per_expense_riyal = (total_revenue / total_expense) if total_expense > 0 else 0.0

    ebitda = net_profit + (total_expense * 0.05)
    ebitda_margin = (ebitda / total_revenue * 100) if total_revenue > 0 else 0.0
    ebit = net_profit
    ebit_margin = (ebit / total_revenue * 100) if total_revenue > 0 else 0.0

    contribution_margin = total_revenue - variable_costs
    contribution_margin_ratio = (contribution_margin / total_revenue) if total_revenue > 0 else 0.55
    bep_val = fixed_costs / contribution_margin_ratio if contribution_margin_ratio > 0 else total_expense
    bep_coverage = (total_revenue / bep_val * 100) if bep_val > 0 else 0.0

    dol = (contribution_margin / ebit) if ebit > 0 else 1.0

    st.markdown("---")

    render_executive_cards(total_revenue, cogs_amount, cogs_ratio, total_expense, opex_ratio, net_profit, profit_margin, target_achieved, b_target, bep_val, bep_coverage)

    render_templates(
        selected_template,
        total_revenue=total_revenue, b_target=b_target, exp_df=exp_df, rev_df=rev_df,
        total_expense=total_expense, net_profit=net_profit, profit_margin=profit_margin,
        cost_per_sales_riyal=cost_per_sales_riyal, return_per_expense_riyal=return_per_expense_riyal,
        fixed_costs=fixed_costs, variable_costs=variable_costs, cogs_amount=cogs_amount,
        cogs_ratio=cogs_ratio, target_achieved=target_achieved, opex_ratio=opex_ratio,
        ebitda=ebitda, ebitda_margin=ebitda_margin, ebit=ebit, ebit_margin=ebit_margin,
        contribution_margin=contribution_margin, contribution_margin_ratio=contribution_margin_ratio,
        bep_val=bep_val, bep_coverage=bep_coverage, dol=dol, df_data=df_data, show_math=show_math
    )