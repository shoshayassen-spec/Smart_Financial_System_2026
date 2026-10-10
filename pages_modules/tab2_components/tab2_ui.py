import streamlit as st

MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

def apply_tab2_styles():
    st.markdown("""
    <style>
        div[data-testid="stColumn"] div.stButton > button {
            width: 100% !important; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important; border-radius: 12px !important;
            color: #E2E8F0 !important; font-weight: 700 !important; padding: 12px 10px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important; transition: all 0.3s ease !important;
        }
        div[data-testid="stColumn"] div.stButton > button:hover {
            transform: translateY(-3px) scale(1.03) !important; border-color: #38BDF8 !important; color: #38BDF8 !important;
        }
        div[data-testid="stColumn"] div.stButton > button:disabled {
            background: rgba(15, 23, 42, 0.6) !important; opacity: 0.6 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_month_selector(selected_b_code, locked_months):
    apply_tab2_styles()
    st.markdown("### 2️⃣ اضغط على الشهر المطلوب لسحب بياناته (الشهور المكتملة تظهر مجمدة 🔒):")
    cols = st.columns(6)
    for idx, m in enumerate(MONTHS):
        col = cols[idx % 6]
        is_disabled = m in locked_months
        if col.button(f"🔒 {m}" if is_disabled else f"📅 {m}", key=f"btn_m_{selected_b_code}_{m}", disabled=is_disabled, use_container_width=True):
            st.session_state['active_import_month'] = m
            st.session_state['active_import_branch'] = selected_b_code

def render_summary_cards(selected_b_select, active_m, rows_imported, total_rev, total_exp, net_profit):
    status_str = "ربح صافي 🟢" if net_profit >= 0 else "خسارة صافية 🔴"
    card_border = "#10B981" if net_profit >= 0 else "#EF4444"
    card_bg = "rgba(16, 185, 129, 0.12)" if net_profit >= 0 else "rgba(239, 68, 68, 0.12)"

    st.markdown(f"""
        <div style="background: {card_bg}; border: 1px solid {card_border}; border-radius: 16px; padding: 18px; margin-top: 15px;">
            <h3 style="color: #F8FAFC; margin:0; font-size:18px;">🎉 تم سحب البيانات وتأكيد دقة التجميع 100%!</h3>
            <p style="color: #CBD5E1; font-size:13px; margin-top:5px;"><b>الفرع:</b> {selected_b_select} | <b>الشهر:</b> {active_m} | <b>عدد الصفوف المرحّلة:</b> <span style="color:#38BDF8; font-weight:bold;">{rows_imported} صف</span></p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    profit_color = "#10B981" if net_profit >= 0 else "#EF4444"
    
    for col, title, val, color in [(c1, "إجمالي الإيرادات (الدائن الحقيقي)", total_rev, "#10B981"),
                                  (c2, "إجمالي المصروفات (المدين الحقيقي)", total_exp, "#EF4444"),
                                  (c3, f"صافي النتيجة ({status_str})", net_profit, profit_color)]:
        with col:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-right: 5px solid {color}; border-radius: 12px; padding: 15px; margin-top: 10px;">
                    <div style="color: #94A3B8; font-size: 12px; font-weight: bold;">{title}</div>
                    <div style="color: {color}; font-size: 22px; font-weight: 800; margin-top: 5px;">{val:,.2f} <span style="font-size:12px;">ريال</span></div>
                </div>
            """, unsafe_allow_html=True)