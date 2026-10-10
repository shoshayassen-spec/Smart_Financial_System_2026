import streamlit as st
from utils.db_manager import get_dataframe

# استدعاء مكونات مجلد tab4_components
from pages_modules.tab4_components.tab4_styles import apply_tab4_styles
from pages_modules.tab4_components.tab4_ui import (
    render_city_selector,
    render_city_kpi_cards,
    render_city_branches_table
)

def render():
    # 1. تطبيق الجماليات والتنسيقات
    apply_tab4_styles()

    st.markdown("<div class='main-page-title no-print'>🏙️ التبويب الرابع: استعلام وتحليلات المدن والمناطق</div>", unsafe_allow_html=True)

    # 2. جلب قائمة المدن المسجلة
    cities_df = get_dataframe("SELECT DISTINCT city FROM branches WHERE city IS NOT NULL AND city != ''")
    
    if cities_df.empty:
        st.warning("⚠️ لا توجد مدن مسجلة أو مرتبطة بالفروع حالياً.")
        return

    city_list = ["جميع المدن"] + cities_df['city'].tolist()
    
    if selected_city == "جميع المدن":
        query = "SELECT * FROM branches"
        branches_data = get_dataframe(query)
    else:
        query = "SELECT * FROM branches WHERE city = ?"
        branches_data = get_dataframe(query, (selected_city,))
        query = "SELECT branch_code, branch_name, city, manager_name, phone, target FROM branches WHERE city = ?"
        branches_data = get_dataframe(query, (selected_city,))

    # 4. حساب وعرض الكروت الإحصائية
    branch_count = len(branches_data)
    total_target = branches_data['target'].sum() if 'target' in branches_data.columns else 0.0
    render_city_kpi_cards(branch_count, total_target)

    # 5. عرض جدول البيانات
    render_city_branches_table(branches_data, selected_city)