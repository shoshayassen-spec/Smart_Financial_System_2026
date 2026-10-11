import streamlit as st

def apply_tab4_styles():
    """تنسيقات شاشات بطاقات FinTech الكروت العصرية"""
    st.markdown("""
        <style>
            .fintech-kpi-card {
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 14px;
                padding: 18px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(0,0,0,0.25);
            }
            .fintech-kpi-title {
                font-size: 12px;
                color: #CBD5E1;
                font-weight: 700;
                margin-bottom: 6px;
            }
            .fintech-kpi-val {
                font-size: 22px;
                font-weight: 900;
                margin: 4px 0;
            }
            .fintech-kpi-sub {
                color: #94A3B8;
                font-size: 11px;
            }

            /* تصميم شبكة الكروت Grid Cards */
            .fintech-grid-card {
                background: linear-gradient(145deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
                border: 1px solid rgba(56, 189, 248, 0.25);
                border-radius: 16px;
                padding: 18px;
                margin-bottom: 18px;
                box-shadow: 0 10px 22px rgba(0, 0, 0, 0.35);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }
            .fintech-grid-card:hover {
                border-color: rgba(56, 189, 248, 0.6);
                transform: translateY(-2px);
            }
            .card-metric-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 6px 0;
                border-bottom: 1px dashed rgba(255, 255, 255, 0.05);
            }

            /* البادجات الملونة */
            .badge-green {
                background: rgba(16, 185, 129, 0.18);
                color: #10B981;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 8px;
                border-radius: 12px;
                border: 1px solid rgba(16, 185, 129, 0.3);
            }
            .badge-yellow {
                background: rgba(245, 158, 11, 0.18);
                color: #F59E0B;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 8px;
                border-radius: 12px;
                border: 1px solid rgba(245, 158, 11, 0.3);
            }
            .badge-red {
                background: rgba(239, 68, 68, 0.18);
                color: #EF4444;
                font-size: 10px;
                font-weight: 700;
                padding: 3px 8px;
                border-radius: 12px;
                border: 1px solid rgba(239, 68, 68, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)