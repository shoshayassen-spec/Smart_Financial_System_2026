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
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #1E293B;
        text-align: right;
        padding-bottom: 12px;
        border-bottom: 2px solid #E2E8F0;
        margin-bottom: 20px;
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

    @media print {
        [data-testid="stSidebar"] { display: none !important; }
        .stApp > header { display: none !important; }
        .no-print { display: none !important; }
        .main-header { font-size: 18pt !important; text-align: center; color: #000 !important; }
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