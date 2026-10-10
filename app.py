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

    /* 1. تصميم عنوان الصفحة بالوسط (3D Card) */
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
        margin-bottom: 25px;
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

    /* 3. تحويل خيارات st.radio إلى كروت 3D زجاجية تفاعلية */
    div[data-testid="stSidebar"] [data-testid="stRadio"] > div {
        gap: 12px !important;
    }

    div[data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        font-size: 15px !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }

    /* استهداف كبسولة الخيار بالكامل */
    div[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        padding: 14px 18px !important;
        color: #CBD5E1 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin-bottom: 2px !important;
    }

    /* إخفاء دائرة الراديو الافتراضية لجعل الكرت أنيقاً ومسطحاً */
    div[data-testid="stSidebar"] [data-testid="stRadio"] label [data-testid="stRadioButtonCustomIcon"] {
        display: none !important;
    }

    /* تأثير المرور فوق الكروت Hover */
    div[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        transform: translateY(-3px) scale(1.02) !important;
        border-color: #38BDF8 !important;
        color: #38BDF8 !important;
        box-shadow: 0 8px 22px rgba(56, 189, 248, 0.3) !important;
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
    }

    /* الكرت المختار والنشط حالياً Active */
    div[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked),
    div[data-testid="stSidebar"] [data-testid="stRadio"] label[data-checked="true"] {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        border: 1px solid #60A5FA !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 25px rgba(37, 99, 235, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.4) !important;
        transform: scale(1.03) !important;
    }

    div[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
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
# [3] الهيدر والتنقل في القائمة الجانبية (Sidebar Routing)
# -----------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand-box">
            <div class="sidebar-brand-title">🌐 النظام المالي الذكي</div>
            <div class="sidebar-brand-sub">إصدار التحليل الشامل 2026</div>
        </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        "اختر التبويب للتنقل:",
        [
            "🏢  1. تكويد وبيانات الفروع",
            "📥  2. سحب واستيراد الإكسل الشهري",
            "📊  3. استعلام وتقارير الفروع (متعدد)",
            "🏙️  4. استعلام وتقارير المدن",
            "📈  5. التجميع المالي والمؤشرات الشاملة",
            "🌐  6. استجلاء القوالب الذكية (Online)",
            "⚙️  7. إعدادات النظام وتفريغ الذاكرة"
        ],
        label_visibility="collapsed"
    )

# -----------------------------------------------------------------------------------
# [4] توجيه الصفحة المحددة
# -----------------------------------------------------------------------------------
if "1. تكويد وبيانات الفروع" in menu:
    tab1_branches.render()

elif "2. سحب واستيراد الإكسل الشهري" in menu:
    tab2_excel_import.render()

elif "3. استعلام وتقارير الفروع" in menu:
    tab3_reports.render()

elif "4. استعلام وتقارير المدن" in menu:
    tab4_cities.render()

elif "5. التجميع المالي والمؤشرات الشاملة" in menu:
    tab5_consolidation.render()

elif "6. استجلاء القوالب الذكية" in menu:
    tab6_online.render()

elif "7. إعدادات النظام وتفريغ الذاكرة" in menu:
    tab7_settings.render()