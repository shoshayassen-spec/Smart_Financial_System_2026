import streamlit as st

def render_city_selector(city_list):
    """
    شريط اختيار المدينة للاستعلام
    """
    col_sel, _ = st.columns([2, 1])
    with col_sel:
        selected_city = st.selectbox("🎯 اختر المدينة للاستعلام والتجميع:", city_list)
    return selected_city


def render_city_kpi_cards(branch_count, total_target):
    """
    عرض الكروت الإحصائية السريعة الخاصة بالمدينة
    """
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div class="city-card-container">
                <div class="city-card-title">🏢 عدد الفروع التابعة</div>
                <div class="city-card-value" style="color:#60A5FA;">{branch_count} فروع</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="city-card-container">
                <div class="city-card-title">🎯 إجمالي مستهدف المدينة</div>
                <div class="city-card-value" style="color:#FBBF24;">{total_target:,.0f} ريال</div>
            </div>
        """, unsafe_allow_html=True)


def render_city_branches_table(branches_data, selected_city):
    """
    عرض جدول بيانات الفروع التابعة للمدينة
    """
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"📊 قائمة بيانات الفروع في: {selected_city}")
    
    st.dataframe(
        branches_data,
        column_config={
            "branch_code": "كود الفرع",
            "branch_name": "اسم الفرع",
            "city": "المدينة",
            "manager_name": "مدير الفرع",
            "phone": "رقم التواصل",
            "target": st.column_config.NumberColumn("المستهدف (ريال)", format="%.0f ريال")
        },
        use_container_width=True
    )