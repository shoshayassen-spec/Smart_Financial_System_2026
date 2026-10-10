import streamlit as st

def apply_tab3_styles():
    """
    تنسيقات الواجهة عالية التباين والطباعة الخاصة بالتبويب الثالث
    مع دعم التباين التلقائي للوضع الداكن والفاتح والكروت المحدثة
    """
    st.markdown("""
        <style>
            /* التباين العام للتطبيق */
            .stApp { 
                background-color: #0F172A !important; 
                color: #F8FAFC !important; 
            }
            
            /* العنوان الرئيسي للتطبيقات */
            .main-page-title {
                text-align: center; 
                font-size: 24px; 
                font-weight: 900; 
                color: #FFFFFF !important;
                background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 50%, #1D4ED8 100%);
                padding: 14px; 
                border-radius: 12px; 
                box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
                margin-bottom: 20px; 
                border: 1px solid #60A5FA;
            }

            /* شريط اسم القالب النشط المحدث */
            .active-template-banner {
                text-align: center;
                font-size: 16px;
                font-weight: 800;
                color: #38BDF8 !important;
                background: rgba(30, 58, 138, 0.4);
                padding: 10px;
                border-radius: 8px;
                border: 1px solid rgba(96, 165, 250, 0.3);
                margin-top: 10px;
                margin-bottom: 20px;
            }

            /* كروت المؤشرات العلوية المتكيفة عالية التباين */
            .metric-card-container {
                background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
                border: 1px solid #334155; 
                border-radius: 12px;
                padding: 14px 10px; 
                text-align: center; 
                box-shadow: 0 4px 12px rgba(0,0,0,0.4);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .metric-card-container:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(59, 130, 246, 0.25);
                border-color: #60A5FA;
            }
            .metric-title { 
                font-size: 13px; 
                color: #CBD5E1 !important; 
                font-weight: 700; 
                margin-bottom: 6px; 
            }
            .metric-value { 
                font-size: 20px; 
                font-weight: 900; 
                color: #FFFFFF !important;
                text-shadow: 0 1px 2px rgba(0,0,0,0.5);
            }
            .metric-sub { 
                font-size: 11px; 
                color: #38BDF8 !important; 
                margin-top: 5px; 
                font-weight: bold; 
            }
            
            /* ألوان مخصصة لمؤشرات الأداء */
            .text-success-bright { color: #4ADE80 !important; }
            .text-warning-bright { color: #FBBF24 !important; }
            .text-danger-bright { color: #F87171 !important; }

            /* صناديق تشخيص الذكاء الاصطناعي والاستشارات */
            .ai-box-success {
                background-color: #064E3B !important; 
                border: 1px solid #10B981 !important;
                color: #ECFDF5 !important; 
                padding: 15px; 
                border-radius: 10px; 
                margin-bottom: 15px;
                box-shadow: 0 4px 10px rgba(16, 185, 129, 0.15);
            }
            .ai-box-warning {
                background-color: #78350F !important; 
                border: 1px solid #F59E0B !important;
                color: #FEF3C7 !important; 
                padding: 15px; 
                border-radius: 10px; 
                margin-bottom: 15px;
                box-shadow: 0 4px 10px rgba(245, 158, 11, 0.15);
            }
            .ai-box-error {
                background-color: #7F1D1D !important; 
                border: 1px solid #EF4444 !important;
                color: #FEF2F2 !important; 
                padding: 15px; 
                border-radius: 10px; 
                margin-bottom: 15px;
                box-shadow: 0 4px 10px rgba(239, 68, 68, 0.15);
            }
            .ai-box-info {
                background-color: #1E3A8A !important; 
                border: 1px solid #3B82F6 !important;
                color: #EFF6FF !important; 
                padding: 15px; 
                border-radius: 10px; 
                margin-bottom: 15px;
                box-shadow: 0 4px 10px rgba(59, 130, 246, 0.15);
            }

            /* قسم معادلات المراجعة المدرسية */
            .math-review-section {
                background-color: #020617; 
                border: 1px dashed #3B82F6; 
                border-radius: 10px;
                padding: 20px; 
                margin-top: 40px; 
                color: #F8FAFC !important; 
                font-family: monospace;
            }

            /* الجداول المنسقة والتحليلات العمودية */
            .styled-table {
                width: 100%; 
                border-collapse: collapse; 
                margin: 15px 0; 
                font-size: 15px; 
                text-align: right; 
                color: #FFFFFF !important;
            }
            .styled-table th { 
                background-color: #1E3A8A; 
                color: #FFFFFF !important; 
                padding: 12px; 
                font-weight: bold; 
                border-bottom: 2px solid #3B82F6;
            }
            .styled-table td { 
                padding: 12px; 
                border-bottom: 1px solid #334155; 
                color: #FFFFFF !important; 
            }
            .styled-table tr:hover {
                background-color: rgba(51, 65, 85, 0.4);
            }

            .stDataFrame, .stTable { color: #FFFFFF !important; }
            
            /* إعدادات الطباعة المتقدمة */
            @media print {
                body, .stApp { 
                    background-color: #FFFFFF !important; 
                    color: #000000 !important; 
                }
                header, footer, .stButton, [data-testid="stSidebar"], .no-print, .math-review-section, .stSelectbox { 
                    display: none !important; 
                }
                .metric-card-container {
                    border: 1px solid #000000 !important;
                    background: #FFFFFF !important;
                    color: #000000 !important;
                }
                .metric-title, .metric-value, .metric-sub {
                    color: #000000 !important;
                }
                .styled-table th {
                    background-color: #F1F5F9 !important;
                    color: #000000 !important;
                }
                .styled-table td {
                    color: #000000 !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)