import streamlit as st

MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

def apply_tab2_styles():
    """تطبيق CSS مخصص لكروت الشهور ومربعات الادخال الزجاجية 3D"""
    st.markdown("""
    <style>
        /* كروت أزرار الشهور 3D */
        div[data-testid="stColumn"] div.stButton > button {
            width: 100% !important;
            background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 12px !important;
            color: #E2E8F0 !important;
            font-weight: 700 !important;
            padding: 12px 10px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        div[data-testid="stColumn"] div.stButton > button:hover {
            transform: translateY(-3px) scale(1.03) !important;
            border-color: #38BDF8 !important;
            color: #38BDF8 !important;
            box-shadow: 0 8px 20px rgba(56, 189, 248, 0.3) !important;
        }
        div[data-testid="stColumn"] div.stButton > button:disabled {
            background: rgba(15, 23, 42, 0.6) !important;
            border-color: rgba(255, 255, 255, 0.05) !important;
            color: #64748B !important;
            box-shadow: none !important;
            opacity: 0.7 !important;
        }

        /* كرت المعاينة وإعدادات الأعمدة */
        .glass-panel-3d {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin: 15px 0 !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
            backdrop-filter: blur(10px) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_month_selector(selected_b_code, locked_months):
    """عرض الشهور على شكل كروت وأزرار 3D تفاعلية"""
    apply_tab2_styles()
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
    """عرض نتائج السحب والترحيل المالي بكروت إحصائية 3D فاخرة"""
    status_str = "ربح صافي 🟢" if net_profit >= 0 else "خسارة صافية 🔴"
    card_border = "#10B981" if net_profit >= 0 else "#EF4444"
    card_bg = "rgba(16, 185, 129, 0.12)" if net_profit >= 0 else "rgba(239, 68, 68, 0.12)"

    st.markdown(f"""
        <div style="background: {card_bg}; border: 1px solid {card_border}; border-radius: 16px; padding: 22px; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); backdrop-filter: blur(10px);">
            <h3 style="color: #F8FAFC; margin-top:0; font-size:20px;">🎉 تم سحب البيانات وتأكيد دقة التجميع 100%!</h3>
            <p style="color: #CBD5E1; font-size:14px;"><b>الفرع:</b> {selected_b_select} | <b>الشهر:</b> {active_m} | <b>عدد الصفوف المرحّلة:</b> <span style="color:#38BDF8; font-weight:bold;">{rows_imported} صف</span></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-right: 5px solid #10B981; border-radius: 14px; padding: 18px; box-shadow: 0 6px 20px rgba(0,0,0,0.3);">
                <div style="color: #94A3B8; font-size: 13px; font-weight: bold;">إجمالي الإيرادات (الدائن الحقيقي)</div>
                <div style="color: #10B981; font-size: 24px; font-weight: 800; margin-top: 6px;">{total_rev:,.2f} <span style="font-size:13px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-right: 5px solid #EF4444; border-radius: 14px; padding: 18px; box-shadow: 0 6px 20px rgba(0,0,0,0.3);">
                <div style="color: #94A3B8; font-size: 13px; font-weight: bold;">إجمالي المصروفات (المدين الحقيقي)</div>
                <div style="color: #EF4444; font-size: 24px; font-weight: 800; margin-top: 6px;">{total_exp:,.2f} <span style="font-size:13px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        profit_color = "#10B981" if net_profit >= 0 else "#EF4444"
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-right: 5px solid {profit_color}; border-radius: 14px; padding: 18px; box-shadow: 0 6px 20px rgba(0,0,0,0.3);">
                <div style="color: #94A3B8; font-size: 13px; font-weight: bold;">صافي النتيجة ({status_str})</div>
                <div style="color: {profit_color}; font-size: 24px; font-weight: 800; margin-top: 6px;">{net_profit:,.2f} <span style="font-size:13px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)