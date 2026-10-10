import streamlit as st

def apply_tab4_styles():
    """
    تنسيقات الواجهة عالية التباين والجماليات الخاصة بالتبويب الرابع (المدن)
    """
    st.markdown("""
        <style>
            .city-card-container {
                background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 15px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            }
            .city-card-title {
                font-size: 13px;
                color: #CBD5E1;
                font-weight: bold;
                margin-bottom: 6px;
            }
            .city-card-value {
                font-size: 20px;
                font-weight: 900;
            }
        </style>
    """, unsafe_allow_html=True)