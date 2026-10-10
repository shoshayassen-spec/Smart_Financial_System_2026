import streamlit as st

# -----------------------------------------------------------------------------------
# [1] إعدادات الصفحة والتصميم العام (RTL & Styles)
# -----------------------------------------------------------------------------------
st.set_page_config(
    page_title="النظام المالي الذكي المتقدم 2026",
    page_icon="🌐",
    layout="wide"
)

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
    }

    /* 1. تصميم هيدر عنوان الصفحة بالوسط (Centralized 3D Glassmorphic Card Header) */
    .main-header, .main-page-title {
        text-align: center !important;
        margin: 10px auto 25px auto !important;
        padding: 18px 25px !important;
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 18px !important;
        color: #F8FAFC !important;
        font-size: 24px !important;
        font-weight: 800 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        max-width: 900px !important;
    }

    .kpi-card-3d {
        background: #FFFFFF;
        padding: 16px;
        border-radius: 12px;
        border-right: 5px solid #2563EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 15px;
    }
    .kpi-title { font-size: 14px; color: #64748B; font-weight: bold; }
    .kpi-value { font-size: 22px; color: #0F172A; font-weight: bold; margin: 5px 0; }
    .kpi-sub { font-size: 12px; font-weight: bold; }
    .text-success { color: #10B981; }
    .text-danger { color: #EF4444; }

    /* 2. تصميم أزرار وقائمة التصفح الجانبية بكروت 3D زجاجية أنيقة */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
        border-left: 1px solid #334155;
    }

    div[data-testid="stSidebar"] div.stRadio > div {
        gap: 12px;
    }
    
    div[data-testid="stSidebar"] div.stRadio label {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease-in-out !important;
        cursor: pointer !important;
    }

    /* تأثير المرور فوق التبويب Hover */
    div[data-testid="stSidebar"] div.stRadio label:hover {
        transform: translateY(-3px) scale(1.02) !important;
        border-color: #38BDF8 !important;
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.25) !important;
        color: #38BDF8 !important;
    }

    /* التبويب النشط والمحدد حالياً Active */
    div[data-testid="stSidebar"] div.stRadio label[data-checked="true"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        border-color: #60A5FA !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
        transform: scale(1.03) !important;
    }

    @media print {
        [data-testid="stSidebar"] { display: none !important; }
        .stApp > header { display: none !important; }
        .no-print { display: none !important; }
        .main-header, .main-page-title { font-size: 18pt !important; text-align: center; color: #000 !important; background: none !important; box-shadow: none !important; border: none !important; }
        .kpi-card-3d { border: 1px solid #ccc !important; box-shadow: none !important; page-break-inside: avoid; }
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
# [3] القائمة الجانبية والتنقل (Sidebar Routing)
# -----------------------------------------------------------------------------------
st.sidebar.title("🌐 النظام المالي الذكي")
st.sidebar.caption("إصدار التحليل الشامل 2026")

menu = st.sidebar.radio(
    "التنقل بين الصفحات والتبويبات:",
    [
        "🏢 1. تكويد وبيانات الفروع",
        "📥 2. سحب واستيراد الإكسل الشهري",
        "📊 3. استعلام وتقارير الفروع (متعدد)",
        "🏙️ 4. استعلام وتقارير المدن",
        "📈 5. التجميع المالي والمؤشرات الشاملة",
        "🌐 6. استجلاء القوالب الذكية (Online)",
        "⚙️ 7. إعدادات النظام وتفريغ الذاكرة"
    ]
)

# -----------------------------------------------------------------------------------
# [4] توجيه الصفحة المحددة
# -----------------------------------------------------------------------------------
if menu == "🏢 1. تكويد وبيانات الفروع":
    tab1_branches.render()

elif menu == "📥 2. سحب واستيراد الإكسل الشهري":
    tab2_excel_import.render()

elif menu == "📊 3. استعلام وتقارير الفروع (متعدد)":
    tab3_reports.render()

elif menu == "🏙️ 4. استعلام وتقارير المدن":
    tab4_cities.render()

elif menu == "📈 5. التجميع المالي والمؤشرات الشاملة":
    tab5_consolidation.render()

elif menu == "🌐 6. استجلاء القوالب الذكية (Online)":
    tab6_online.render()

elif menu == "⚙️ 7. إعدادات النظام وتفريغ الذاكرة":
    tab7_settings.render()