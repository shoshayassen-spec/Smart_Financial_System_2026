import streamlit as st
import pandas as pd
import numpy as np
from utils.db_manager import get_dataframe

# استدعاء مكونات مجلد tab4_components
from pages_modules.tab4_components.tab4_styles import apply_tab4_styles
from pages_modules.tab4_components.tab4_ui import (
    render_city_header,
    render_city_selector,
    render_city_kpi_cards,
    render_top_bottom_branches,
    render_city_analytics_tabs,
    render_city_branches_table
)

def render():
    # 1. تطبيق الجماليات الهيكلية والأنماط الزجاجية 3D
    apply_tab4_styles()

    # 2. الهيدر الرئيسي للتبويب
    render_city_header()

    # 3. جلب قائمة المدن المسجلة من قاعدة البيانات
    cities_df = get_dataframe("SELECT DISTINCT city FROM branches WHERE city IS NOT NULL AND city != ''")
    
    if cities_df.empty:
        st.warning("⚠️ لا توجد مدن مسجلة أو مرتبطة بالفروع حالياً في قاعدة البيانات.")
        return

    city_list = [" جميع المدن (عرض موحد)"] + sorted(cities_df['city'].tolist())
    
    # 4. شريط اختيار المدينة
    selected_city = render_city_selector(city_list)

    # 5. جلب بيانات الفروع والأداء المالي للمدينة المختارة
    if selected_city.startswith(" جميع المدن"):
        query = "SELECT * FROM branches"
        branches_data = get_dataframe(query)
    else:
        query = "SELECT * FROM branches WHERE city = ?"
        branches_data = get_dataframe(query, (selected_city,))

    if branches_data.empty:
        st.info("ℹ️ لا توجد بيانات مالية مسجلة للفروع التابعة لهذه المدينة.")
        return

    # 6. تجهيز وحساب المعاملات المالية الحقيقية للفروع
    branches_data['actual_sales'] = branches_data['actual_sales'].fillna(0.0) if 'actual_sales' in branches_data.columns else 0.0
    branches_data['target'] = branches_data['target'].fillna(0.0) if 'target' in branches_data.columns else 0.0
    branches_data['fixed_costs'] = branches_data['fixed_costs'].fillna(0.0) if 'fixed_costs' in branches_data.columns else 0.0
    branches_data['variable_costs'] = branches_data['variable_costs'].fillna(0.0) if 'variable_costs' in branches_data.columns else 0.0
    
    branches_data['total_expenses'] = branches_data['fixed_costs'] + branches_data['variable_costs']
    branches_data['net_profit'] = branches_data['actual_sales'] - branches_data['total_expenses']
    
    # نسبة تحقيق المستهدف لكل فرع
    branches_data['target_achieved'] = np.where(
        branches_data['target'] > 0,
        (branches_data['actual_sales'] / branches_data['target']) * 100.0,
        0.0
    )

    # 7. عرض كروت KPIs التشغيلية والمالية المجمعة
    render_city_kpi_cards(branches_data, selected_city)

    st.markdown("---")

    # 8. عرض مقارنة أعلى وأدنى الفروع أداءً داخل المدينة
    render_top_bottom_branches(branches_data, selected_city)

    st.markdown("<br>", unsafe_allow_html=True)

    # 9. تحليلات القوالب المالية المتقدمة على مستوى المدينة (BEP & EBITDA & Benchmarking)
    render_city_analytics_tabs(branches_data, selected_city)

    st.markdown("<br>", unsafe_allow_html=True)

    # 10. جدول البيانات التفصيلي للفروع
    render_city_branches_table(branches_data, selected_city)