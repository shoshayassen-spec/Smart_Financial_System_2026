import streamlit as st
import pandas as pd

MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

def render_month_selector(selected_b_code, locked_months):
    """
    عرض الشهور على شكل كروت وأزرار 3D تفاعلية
    """
    st.markdown("### 2️⃣ اضغط على الشهر المطلوب لسحب بياناته (الشهور المكتملة تظهر مجمدة 🔒):")
    cols = st.columns(6)
    for idx, m in enumerate(MONTHS):
        col = cols[idx % 6]
        is_disabled = m in locked_months
        label = f"🔒 {m}" if is_disabled else f"📅 {m}"
        if col.button(label, key=f"btn_m_{selected_b_code}_{m}", disabled=is_disabled, use_container_width=True):
            st.session_state['active_import_month'] = m
            st.session_state['active_import_branch'] = selected_b_code

def render_summary_cards(selected_b_select, active_m, rows_imported, total_rev, total_exp, net_profit):
    """
    عرض نتائج السحب والترحيل المالي بكروت إحصائية 3D فاخرة
    """
    status_str = "ربح صافي 🟢" if net_profit >= 0 else "خسارة صافية 🔴"
    card_border = "#10B981" if net_profit >= 0 else "#EF4444"
    card_bg = "rgba(16, 185, 129, 0.1)" if net_profit >= 0 else "rgba(239, 68, 68, 0.1)"

    st.markdown(f"""
        <div style="background: {card_bg}; border: 1px solid {card_border}; border-radius: 16px; padding: 20px; margin-top: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); backdrop-filter: blur(8px);">
            <h3 style="color: #F8FAFC; margin-top:0; font-size:20px;">✅ تم سحب البيانات وتأكيد دقة التجميع 100%!</h3>
            <p style="color: #CBD5E1; font-size:14px;"><b>الفرع:</b> {selected_b_select} | <b>الشهر:</b> {active_m} | <b>عدد الصفوف المرحّلة:</b> <span style="color:#38BDF8; font-weight:bold;">{rows_imported} صف</span></p>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <h4 style="color: #F8FAFC; font-size:16px;">📊 الخلاصة الحقيقية للقائمة المالية:</h4>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border-right: 5px solid #10B981; border-radius: 12px; padding: 15px; margin-top: 10px;">
                <div style="color: #94A3B8; font-size: 13px; font-weight: bold;">إجمالي الإيرادات (الدائن)</div>
                <div style="color: #10B981; font-size: 22px; font-weight: bold; margin-top: 5px;">{total_rev:,.2f} <span style="font-size:12px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border-right: 5px solid #EF4444; border-radius: 12px; padding: 15px; margin-top: 10px;">
                <div style="color: #94A3B8; font-size: 13px; font-weight: bold;">إجمالي المصروفات (المدين)</div>
                <div style="color: #EF4444; font-size: 22px; font-weight: bold; margin-top: 5px;">{total_exp:,.2f} <span style="font-size:12px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        profit_color = "#10B981" if net_profit >= 0 else "#EF4444"
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border-right: 5px solid {profit_color}; border-radius: 12px; padding: 15px; margin-top: 10px;">
                <div style="color: #94A3B8; font-size: 13px; font-weight: bold;">صافي النتيجة ({status_str})</div>
                <div style="color: {profit_color}; font-size: 22px; font-weight: bold; margin-top: 5px;">{net_profit:,.2f} <span style="font-size:12px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)