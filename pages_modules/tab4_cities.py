import streamlit as st
import pandas as pd
import numpy as np
from utils.db_manager import get_dataframe

from pages_modules.tab4_components.tab4_styles import apply_tab4_styles
from pages_modules.tab4_components.tab4_ui import (
    render_city_header,
    render_city_selector_and_filter,
    render_city_kpi_cards,
    render_fintech_branch_cards_grid,
    render_city_analytics_tabs
)

def render():
    # 1. تطبيق أنماط الكروت العصرية 3D
    apply_tab4_styles()

    # 2. الهيدر العام
    render_city_header()

    # 3. جلب المدن
    cities_df = get_dataframe("SELECT DISTINCT city FROM branches WHERE city IS NOT NULL AND city != ''")
    if cities_df.empty:
        st.warning("⚠️ لا توجد مدن مسجلة حالياً.")
        return

    city_list = [" جميع المدن (عرض موحد)"] + sorted(cities_df['city'].tolist())
    selected_city, status_filter = render_city_selector_and_filter(city_list)

    # 4. جلب وترشيح البيانات
    if selected_city.startswith(" جميع المدن"):
        branches_data = get_dataframe("SELECT * FROM branches")
    else:
        branches_data = get_dataframe("SELECT * FROM branches WHERE city = ?", (selected_city,))

    if branches_data.empty:
        st.info("ℹ️ لا توجد بيانات مسجلة للفروع.")
        return

    # معالجة القيم
    branches_data['actual_sales'] = branches_data['actual_sales'].fillna(0.0) if 'actual_sales' in branches_data.columns else 0.0
    branches_data['target'] = branches_data['target'].fillna(0.0) if 'target' in branches_data.columns else 0.0
    branches_data['fixed_costs'] = branches_data['fixed_costs'].fillna(0.0) if 'fixed_costs' in branches_data.columns else 0.0
    branches_data['variable_costs'] = branches_data['variable_costs'].fillna(0.0) if 'variable_costs' in branches_data.columns else 0.0
    
    branches_data['total_expenses'] = branches_data['fixed_costs'] + branches_data['variable_costs']
    branches_data['net_profit'] = branches_data['actual_sales'] - branches_data['total_expenses']
    branches_data['target_achieved'] = np.where(branches_data['target'] > 0, (branches_data['actual_sales'] / branches_data['target']) * 100.0, 0.0)

    # تطبيق التصفية
    if status_filter == "🟢 الفروع الرابحة":
        branches_data = branches_data[branches_data['net_profit'] >= 0]
    elif status_filter == "🔴 فروع تحتاج تحسين":
        branches_data = branches_data[branches_data['net_profit'] < 0]

    # 5. عرض الكروت الإحصائية العليا
    render_city_kpi_cards(branches_data, selected_city)

    st.markdown("<br>", unsafe_allow_html=True)

    # 6. عرض شبكة بطاقات الفروع الحديثة (Grid Cards)
    render_fintech_branch_cards_grid(branches_data)

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. عرض التحليلات والقوالب المجمعة
    render_city_analytics_tabs(branches_data, selected_city)