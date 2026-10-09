import streamlit as st
import pandas as pd

def render():
    st.markdown("<div class='main-header'>🏙️ التبويب الرابع: استعلام وتقارير المدن</div>", unsafe_allow_html=True)
    city_df = pd.DataFrame({
        "المدينة": ["الرياض", "جدة", "الدمام", "مكة المكرمة"],
        "عدد الفروع": [12, 8, 5, 3],
        "المبيعات (ريال)": [1450000.00, 980000.00, 620000.00, 410000.00],
        "نسبة النمو": ["12.5%", "8.2%", "15.0%", "5.4%"]
    })
    st.dataframe(city_df, hide_index=True, use_container_width=True)