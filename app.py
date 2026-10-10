import streamlit as st

# -----------------------------------------------------------------------------------
# [1] إعدادات الصفحة والتصميم العام (RTL & 3D Glassmorphic Styles)
# -----------------------------------------------------------------------------------
st.set_page_config(
    page_title="النظام المالي الذكي المتقدم 2026",
    page_icon="🌐",
    layout="wide"
)

# إدارة حالة التبويب الحالي
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = "tab1"

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }

    /* 1. هيدر عنوان الصفحة بالوسط (Centralized 3D Card Header) */
    .main-header, .main-page-title {
        text-align: center !important;
        margin: 10px auto 25px auto !important;
        padding: 18px 25px !important;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.35) !important;
        border-radius: 18px !important;
        color: #F8FAFC !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        max-width: 900px !important;
    }

    /* 2. تحسين خلفية القائمة الجانبية */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B132B 0%, #1C2541 100%) !important;
        border-left: 1px solid #3A506B !important;
    }

    /* هيدر القائمة الجانبية */
    .sidebar-brand-box {
        text-align: center;
        padding: 18px 12px;
        background: rgba(28, 37, 65, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }
    .sidebar-brand-title {
        font-size: 20px;
        font-weight: 800;
        color: #38BDF8;
        margin: 0;
    }
    .sidebar-brand-sub {
        font-size: 12px;
        color: #94A3B8;
        margin-top: 4px;
    }

    /* 3. تحويل كافة أزرار القائمة الجانبية إلى كروت زجاجية 3D فاخرة */
    [data-testid="stSidebar"] div.stButton > button {
        width: 100% !important;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        color: #CBD5E1 !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 14px 16px !important;
        text-align: right !important;
        justify-content: flex-start !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 4px !important;
    }

    /* تأثير المرور فوق الكرت Hover */
    [data-testid="stSidebar"] div.stButton > button:hover {
        transform: translateX(-5px) translateY(-2px) !important;
        border-color: #38BDF8 !important;
        color: #38BDF8 !important;
        box-shadow: 0 8px 22px rgba(56, 189, 248, 0.3) !important;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
    }

    /* الكرت المختار والنشط حالياً Active Card */
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        border: 1px solid #60A5FA !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
        transform: scale(1.02) !important;
    }

    @media print {
        [data-testid="stSidebar"] { display: none !important; }
        .stApp > header { display: none !important; }
        .no-print { display: none !important; }
        .main-header, .main-page-title { font-size: 18pt !important; text-align: center; color: #000 !important; background: none !important; box-shadow: none !important; border: none !important; }
        body { font-size: 10pt; color: #000; background: #fff !important; direction: rtl; }
        @page { size: A4 portrait; margin: 10mm; }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------------
# [2] استدعاء وحدات الصفحات من المجلد الفرعي (pages_modules)
# -----------------------------------------------------------------------------------
from pages_modules import (
    tab1_branches,
    tab2_excel_import,
    tab3_reports,
    tab4_cities,
    tab5_consolidation,
    tab6_online,
    tab7_settings
)

# -----------------------------------------------------------------------------------
# [3] الهيدر والتنقل في القائمة الجانبية عبر أزرار الكروت 3D
# -----------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-title">🌐 النظام المالي الذكي</div>
            <div class="sidebar-brand-sub">إصدار التحليل الشامل 2026</div>
        </div>
    """, unsafe_allow_html=True)

    # قائمة الأزرار والكروت
    tabs = [
        ("🏢  1. تكويد وبيانات الفروع", "tab1"),
        ("📥  2. سحب واستيراد الإكسل الشهري", "tab2"),
        ("📊  3. استعلام وتقارير الفروع (متعدد)", "tab3"),
        ("🏙️  4. استعلام وتقارير المدن", "tab4"),
        ("📈  5. التجميع المالي والمؤشرات الشاملة", "tab5"),
        ("🌐  6. استجلاء القوالب الذكية (Online)", "tab6"),
        ("⚙️  7. إعدادات النظام وتفريغ الذاكرة", "tab7"),
    ]

    for label, tab_id in tabs:
        # إذا كان التبويب هو النشط حالياً يأخذ نوع primary ليظهر كرت مضيء بارز
        btn_type = "primary" if st.session_state['active_tab'] == tab_id else "secondary"
        if st.button(label, key=f"btn_{tab_id}", type=btn_type, use_container_width=True):
            st.session_state['active_tab'] = tab_id
            st.rerun()

# -----------------------------------------------------------------------------------
# [4] توجيه الصفحة المحددة حسب Session State
# -----------------------------------------------------------------------------------
active = st.session_state['active_tab']

if active == "tab1":
    tab1_branches.render()
elif active == "tab2":
    tab2_excel_import.render()
elif active == "tab3":
    tab3_reports.render()
elif active == "tab4":
    tab4_cities.render()
elif active == "tab5":
    tab5_consolidation.render()
elif active == "tab6":
    tab6_online.render()
elif active == "tab7":
    tab7_settings.render()