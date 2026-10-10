import streamlit as st

def apply_tab3_styles():
    """
    تنسيقات الواجهة عالية التباين والطباعة الخاصة بالتبويب الثالث
    """
    st.markdown("""
        <style>
            .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
            .main-page-title {
                text-align: center; font-size: 24px; font-weight: 900; color: #FFFFFF;
                background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 50%, #1D4ED8 100%);
                padding: 14px; border-radius: 12px; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
                margin-bottom: 20px; border: 1px solid #60A5FA;
            }
            .metric-card-container {
                background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
                border: 1px solid #334155; border-radius: 12px;
                padding: 12px 8px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            }
            .metric-title { font-size: 12px; color: #CBD5E1; font-weight: bold; margin-bottom: 5px; }
            .metric-value { font-size: 18px; font-weight: 900; }
            .metric-sub { font-size: 11px; color: #38BDF8; margin-top: 4px; font-weight: bold; }
            
            .ai-box-success {
                background-color: #064E3B !important; border: 1px solid #10B981 !important;
                color: #ECFDF5 !important; padding: 15px; border-radius: 10px; margin-bottom: 15px;
            }
            .ai-box-warning {
                background-color: #78350F !important; border: 1px solid #F59E0B !important;
                color: #FEF3C7 !important; padding: 15px; border-radius: 10px; margin-bottom: 15px;
            }
            .ai-box-error {
                background-color: #7F1D1D !important; border: 1px solid #EF4444 !important;
                color: #FEF2F2 !important; padding: 15px; border-radius: 10px; margin-bottom: 15px;
            }

            .math-review-section {
                background-color: #020617; border: 1px dashed #3B82F6; border-radius: 10px;
                padding: 20px; margin-top: 40px; color: #F8FAFC !important; font-family: monospace;
            }

            .styled-table {
                width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 15px; text-align: right; color: #FFFFFF !important;
            }
            .styled-table th { background-color: #1E3A8A; color: #FFFFFF !important; padding: 12px; font-weight: bold; }
            .styled-table td { padding: 12px; border-bottom: 1px solid #334155; color: #FFFFFF !important; }

            .stDataFrame, .stTable { color: #FFFFFF !important; }
            
            @media print {
                body, .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
                header, footer, .stButton, [data-testid="stSidebar"], .no-print, .math-review-section { 
                    display: none !important; 
                }
            }
        </style>
    """, unsafe_allow_html=True)