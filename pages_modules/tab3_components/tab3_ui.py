import streamlit as st
import pandas as pd
from utils.db_manager import get_dataframe

def render_control_bar(branches_df, months_list):
    # 1. جلب السنوات المتاحة ديناميكياً من قاعدة البيانات
    df_years = get_dataframe("SELECT DISTINCT year FROM income_statement WHERE year IS NOT NULL AND year != '' ORDER BY year DESC")
    available_years = df_years['year'].tolist() if not df_years.empty else ["2026", "2025"]

    # إعداد قائمة الفروع للعرض
    branch_options = branches_df["branch_code"].astype(str) + " - " + branches_df["branch_name"]

    # --- الجزء العلوي (وسط الصفحة): أزرار التحكم واختيار القالب الشامل ---
    st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
    top_c1, top_c2, top_c3 = st.columns([1.5, 2.5, 1.5])
    
    with top_c1:
        if st.button("🔄 تحديث القوالب", use_container_width=True, key="btn_refresh_ui"):
            st.rerun()

    with top_c2:
        template_options = st.session_state.get('template_list', [
            "🌐 [قالب 1]: لوحة القيادة التنفيذية الشاملة (Dashboard)",
            "📊 [قالب 2]: التقرير المالي التفصيلي (P&L Standard)",
            "📈 [قالب 3]: التحليل العامودي والأفقي (Vertical & Horizontal)",
            "⚖️ [قالب 4]: تقرير نقطة التعادل والهوامش (BEP & Margins)",
            "🔍 [قالب 5]: الفحص والتدقيق المالي المحاسبي",
            "🎯 [قالب 6]: تقرير مقارنة الأهداف والأداء (Target Vs Actual)",
            "📅 [قالب 7]: التقرير الشهري المقارن (Monthly Trend)"
        ])
        selected_template = st.selectbox("🎯 نمط العرض والقالب:", template_options, key="selected_template_ui")

    with top_c3:
        if st.button("🖨️ طباعة / PDF", type="primary", use_container_width=True, key="btn_print_ui"):
            st.js("window.print()")
    st.markdown("</div>", unsafe_allow_html=True)

    # --- الجزء السفلي: الفلاتر المترتبة من اليمين إلى اليسار (الفرع - السنة - الشهر) ---
    st.markdown("<div style='background-color: rgba(255, 255, 255, 0.03); padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)

    with f_col1:
        selected_branch_str = st.selectbox("🏬 1. اختيار الفرع:", branch_options, key="filter_branch_ui")

    with f_col2:
        selected_year = st.selectbox("📅 2. اختيار العام:", available_years, key="filter_year_ui")

    with f_col3:
        clean_months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]
        selected_month_clean = st.selectbox("🗓️ 3. اختيار الشهر (مع إمكانية البحث):", clean_months, key="filter_month_ui")
    
    show_math = st.checkbox("⚠️ إظهار قسم معادلات المراجعة المدرسية في أسفل الصفحة", value=False, key="chk_show_math")
    st.markdown("</div>", unsafe_allow_html=True)

    # استخراج بيانات الفرع المختارة
    selected_b_code = selected_branch_str.split(" - ")[0].strip()
    branch_row = branches_df[branches_df["branch_code"].astype(str).str.strip() == selected_b_code].iloc[0]
    
    b_name = branch_row["branch_name"]
    b_city = branch_row.get("city", "")
    b_target = float(branch_row.get("target", 100000.0))

    selected_month_full = f"{selected_month_clean} {selected_year}"

    return selected_b_code, b_name, b_city, b_target, selected_month_full, selected_month_clean, selected_template, show_math


def render_executive_cards(total_revenue, cogs_amount, cogs_ratio, total_expense, opex_ratio, net_profit, profit_margin, target_achieved, b_target, bep_val, bep_coverage):
    st.markdown("### 📌 المؤشرات المالية الرئيسية")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        st.metric("💰 إجمالي الإيرادات", f"{total_revenue:,.2f}", "النسبة: 100.0%")
    with kpi2:
        st.metric("📦 تكلفة المبيعات", f"{cogs_amount:,.2f}", f"النسبة: {cogs_ratio:.1f}%")
    with kpi3:
        st.metric("💸 إجمالي المصروفات", f"{total_expense:,.2f}", f"النسبة للإيراد: {opex_ratio:.1f}%")
    with kpi4:
        st.metric("📈 صافي الربح / الخسارة", f"{net_profit:,.2f}", f"الهامش: {profit_margin:.1f}%")
    with kpi5:
        st.metric("🎯 نسبة تحقيق الهدف", f"{target_achieved:.1f}%", f"الهدف: {b_target:,.0f}")