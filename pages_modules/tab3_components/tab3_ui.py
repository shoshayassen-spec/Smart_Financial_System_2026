import streamlit as st
import streamlit.components.v1 as components

def render_control_bar(branches_df, months_list):
    """
    شريط التحكم والأزرار الرئيسية في أعلى التبويب الثالث
    """
    col_online, col_print, col_template, col_m, col_b = st.columns([1, 0.9, 2.2, 1, 1.2])

    with col_b:
        b_options = (branches_df['branch_code'].astype(str) + " - " + branches_df['branch_name'].astype(str)).tolist()
        selected_b_str = st.selectbox("🏢 الفرع المستهدف:", b_options)
        selected_b_code = selected_b_str.split(" - ")[0]
        branch_info = branches_df[branches_df['branch_code'].astype(str) == selected_b_code].iloc[0]
        b_name = branch_info['branch_name']
        b_city = branch_info['city']
        b_target = float(branch_info.get('target', 0.0))

    with col_m:
        selected_month_full = st.selectbox("📅 الفترة المالية:", months_list)
        selected_month = selected_month_full.split(" ")[0]

    with col_template:
        selected_template = st.selectbox("🎯 نمط العرض والقالب:", st.session_state['template_list'], index=0)

    with col_online:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌐 تحديث القوالب", use_container_width=True):
            st.toast("🌐 تم تحديث كافة القوالب والمؤشرات المالية المتقدمة بنجاح.", icon="✨")

    with col_print:
        st.markdown("<br>", unsafe_allow_html=True)
        components.html("""
            <button onclick="window.parent.print()" style="
                background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
                color: white; border: none; padding: 8px 16px; border-radius: 8px;
                font-weight: bold; cursor: pointer; width: 100%; height: 38px;
                font-family: sans-serif; font-size: 14px;">
                🖨️ طباعة / PDF
            </button>
        """, height=45)

    show_math = st.checkbox("📐 إظهار قسم معادلات المراجعة المدرسية في أسفل الصفحة", value=False)

    return selected_b_code, b_name, b_city, b_target, selected_month_full, selected_month, selected_template, show_math


def render_executive_cards(total_revenue, cogs_amount, cogs_ratio, total_expense, opex_ratio, net_profit, profit_margin, target_achieved, b_target, bep_val, bep_coverage):
    """
    عرض الكروت التنفيذية الستة الرئيسية
    """
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">💰 إجمالي الإيرادات</div>
                <div class="metric-value" style="color:#34D399;">{total_revenue:,.2f}</div>
                <div class="metric-sub">النسبة: 100.0%</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">📦 تكلفة المبيعات</div>
                <div class="metric-value" style="color:#FB923C;">{cogs_amount:,.2f}</div>
                <div class="metric-sub">النسبة: {cogs_ratio:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">💸 إجمالي المصروفات</div>
                <div class="metric-value" style="color:#F87171;">{total_expense:,.2f}</div>
                <div class="metric-sub">النسبة للإيراد: {opex_ratio:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        p_color = "#34D399" if net_profit >= 0 else "#F87171"
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">📈 صافي الربح / الخسارة</div>
                <div class="metric-value" style="color:{p_color};">{net_profit:,.2f}</div>
                <div class="metric-sub">الهامش: {profit_margin:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">🎯 نسبة تحقيق الهدف</div>
                <div class="metric-value" style="color:#FBBF24;">{target_achieved:.1f}%</div>
                <div class="metric-sub">الهدف: {b_target:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">⚖️ نقطة التعادل (BEP)</div>
                <div class="metric-value" style="color:#60A5FA;">{bep_val:,.2f}</div>
                <div class="metric-sub">التغطية: {bep_coverage:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)