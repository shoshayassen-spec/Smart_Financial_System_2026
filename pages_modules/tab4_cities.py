import streamlit as st
import pandas as pd
import numpy as np
from utils.db_manager import get_dataframe

from pages_modules.tab4_components.tab4_styles import apply_tab4_styles
from pages_modules.tab4_components.tab4_ui import (
    render_city_control_bar,
    render_city_report_banner,
    render_executive_summary,
    render_income_statement_table,
    render_financial_ratios_table,
    render_cost_structure_and_donut,
    render_bep_section,
    render_target_performance_section,
    render_pareto_analysis,
    render_waterfall_bridge,
    render_sensitivity_analysis,
    render_branch_recommendations,
    render_ai_analysis_panel
)

def render():
    # 1. تطبيق الأنماط والتنسيقات الزجاجية العصرية
    apply_tab4_styles()

    # 2. جلب قائمة المدن المسجلة
    cities_df = get_dataframe("SELECT DISTINCT city FROM branches WHERE city IS NOT NULL AND city != ''")
    if cities_df.empty:
        st.warning("⚠️ لا توجد مدن مسجلة حالياً.")
        return

    city_list = sorted(cities_df['city'].tolist())
    
    # 3. شريط الفلاتر والتحكم والقوالب المثبتة في الأعلى
    selected_city, selected_template, date_from, date_to = render_city_control_bar(city_list)

    # 4. جلب وترشيح البيانات المجمعة للمدينة
    query = "SELECT * FROM branches WHERE city = ?"
    branches_data = get_dataframe(query, (selected_city,))

    if branches_data.empty:
        st.info(f"ℹ️ لا توجد بيانات مالية مسجلة لمدينة {selected_city}.")
        return

    # معالجة وحساب المتغيرات المالية
    branches_data['actual_sales'] = branches_data['actual_sales'].fillna(0.0) if 'actual_sales' in branches_data.columns else 0.0
    branches_data['target'] = branches_data['target'].fillna(0.0) if 'target' in branches_data.columns else 0.0
    branches_data['fixed_costs'] = branches_data['fixed_costs'].fillna(0.0) if 'fixed_costs' in branches_data.columns else 0.0
    branches_data['variable_costs'] = branches_data['variable_costs'].fillna(0.0) if 'variable_costs' in branches_data.columns else 0.0
    
    branches_data['total_expenses'] = branches_data['fixed_costs'] + branches_data['variable_costs']
    branches_data['net_profit'] = branches_data['actual_sales'] - branches_data['total_expenses']
    branches_data['target_achieved'] = np.where(branches_data['target'] > 0, (branches_data['actual_sales'] / branches_data['target']) * 100.0, 0.0)

    # 5. عرض بانر التقرير الشامل للمدينة
    render_city_report_banner(selected_city, date_from, date_to)

    # 6. الملخص التنفيذي وكروت KPIs الستة
    render_executive_summary(branches_data, selected_city)

    # 7. التبديل والعرض حسب القالب المختار
    st.markdown("---")
    
    # عرض الأقسام الرئيسية للتقرير الشامل
    render_income_statement_table(branches_data, selected_city)
    st.markdown("<br>", unsafe_allow_html=True)

    render_financial_ratios_table(branches_data)
    st.markdown("<br>", unsafe_allow_html=True)

    render_cost_structure_and_donut(branches_data)
    st.markdown("<br>", unsafe_allow_html=True)

    render_bep_section(branches_data)
    st.markdown("<br>", unsafe_allow_html=True)

    render_target_performance_section(branches_data)
    st.markdown("<br>", unsafe_allow_html=True)

    render_pareto_analysis(branches_data)
    st.markdown("<br>", unsafe_allow_html=True)

    render_waterfall_bridge(branches_data)
    st.markdown("<br>", unsafe_allow_html=True)

    render_sensitivity_analysis(branches_data)
    st.markdown("<br>", unsafe_allow_html=True)

    render_branch_recommendations(branches_data, selected_city)
    st.markdown("<br>", unsafe_allow_html=True)

    render_ai_analysis_panel(selected_city)