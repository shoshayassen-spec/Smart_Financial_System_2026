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
        
        /* تنسيق زر الاعتماد الخاص المدمج */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
            border: 1px solid #34D399 !important;
            color: #FFFFFF !important;
            font-size: 15px !important;
            font-weight: 800 !important;
            padding: 14px 10px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
        }
        div.stButton > button[kind="primary"]:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.6) !important;
        }

        .unified-banner-box {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; padding: 16px 20px;
            margin-bottom: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }
    </style>
    """, unsafe_allow_html=True)

def render_month_selector(selected_b_code, locked_months):
    apply_tab2_styles()
    st.markdown("### 3️⃣ اضغط على الشهر المطلوب لسحب بياناته (الشهور المكتملة تظهر مجمدة 🔒):")
    cols = st.columns(6)
    for idx, m in enumerate(MONTHS):
        col = cols[idx % 6]
        is_disabled = m in locked_months
        if col.button(f"🔒 {m}" if is_disabled else f"📅 {m}", key=f"btn_m_{selected_b_code}_{m}", disabled=is_disabled, use_container_width=True):
            st.session_state['active_import_month'] = m
            st.session_state['active_import_branch'] = selected_b_code

def render_preview_cards(total_rev, total_exp, net_profit, margin_pct):
    """عرض كروت المؤشرات المالية الثلاثية"""
    status_str = "ربح صافي 🟢" if net_profit >= 0 else "خسارة صافية 🔴"
    profit_color = "#10B981" if net_profit >= 0 else "#EF4444"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-right: 5px solid #10B981; border-radius: 12px; padding: 15px;">
                <div style="color: #94A3B8; font-size: 12px; font-weight: bold;">إجمالي الإيرادات (الدائن الحقيقي)</div>
                <div style="color: #10B981; font-size: 22px; font-weight: 800; margin-top: 5px;">{total_rev:,.2f} <span style="font-size:12px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-right: 5px solid #EF4444; border-radius: 12px; padding: 15px;">
                <div style="color: #94A3B8; font-size: 12px; font-weight: bold;">إجمالي المصروفات (المدين الحقيقي)</div>
                <div style="color: #EF4444; font-size: 22px; font-weight: 800; margin-top: 5px;">{total_exp:,.2f} <span style="font-size:12px;">ريال</span></div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); border-right: 5px solid {profit_color}; border-radius: 12px; padding: 15px;">
                <div style="color: #94A3B8; font-size: 12px; font-weight: bold;">صافي النتيجة ({status_str})</div>
                <div style="color: {profit_color}; font-size: 22px; font-weight: 800; margin-top: 5px;">{net_profit:,.2f} <span style="font-size:12px;">ريال</span> <span style="font-size:11px; color:#94A3B8;">(هامش الربح: {margin_pct:.1f}%)</span></div>
            </div>
        """, unsafe_allow_html=True)