import streamlit as st

def apply_tab4_styles():
    """تنسيقات الواجهة عالية التباين والجماليات الزجاجية 3D الخاصة بالتبويب الرابع"""
    st.markdown("""
        <style>
            .city-card-container {
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                border: 1px solid rgba(56, 189, 248, 0.35);
                border-radius: 14px;
                padding: 16px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            }
            .city-card-title {
                font-size: 12px;
                color: #CBD5E1;
                font-weight: 700;
                margin-bottom: 6px;
            }
            .city-card-value {
                font-size: 20px;
                font-weight: 800;
                margin: 6px 0;
            }
        </style>
    """, unsafe_allow_html=True)