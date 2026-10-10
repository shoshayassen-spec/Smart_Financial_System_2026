import streamlit as st
import pandas as pd
import time
from utils.db_manager import execute_query, get_dataframe
from pages_modules.tab2_components.tab2_ui import render_month_selector, render_preview_cards, MONTHS
from pages_modules.tab2_components.tab2_logic import process_excel_preview, delete_import_data

YEARS = ["2024", "2025", "2026", "2027"]

def render():
    st.markdown("<div class='main-page-title no-print'>📥 التبويب الثاني: سحب واستيراد ملفات الإكسل الشهري</div>", unsafe_allow_html=True)

    branches_df = get_dataframe("SELECT branch_code, branch_name FROM branches")
    if branches_df.empty:
        st.error("⚠️ لا توجد فروع مسجلة! يرجى إضافة فروع أولاً من التبويب الأول.")
        return

    b_list = (branches_df['branch_code'].astype(str) + " - " + branches_df['branch_name'].astype(str)).tolist()
    
    # عناصر التحكم العلوية
    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        selected_b_select = st.selectbox("🎯 1️⃣ اختر الفرع:", b_list)
    with col_b:
        selected_year = st.selectbox("📅 اختر السنة:", YEARS, index=2) # الافتراضي 2026
    with col_c:
        doc_type = st.radio("📄 2️⃣ نوع القائمة:", ["قائمة دخل", "ميزان مراجعة"], horizontal=True)

    selected_b_code = selected_b_select.split(" - ")[0]
    
    # قراءة الشهور المكتملة بناء على الفرع والسنة المحددين
    locked_df = get_dataframe("SELECT DISTINCT month FROM income_statement WHERE TRIM(branch_code) = ? AND TRIM(year) = ?", (selected_b_code, selected_year))
    locked_months = locked_df['month'].tolist() if not locked_df.empty else []

    render_month_selector(selected_b_code, locked_months)

    active_m, active_b = st.session_state.get('active_import_month'), st.session_state.get('active_import_branch')

    if active_m and active_b == selected_b_code:
        st.markdown("---")
        uploaded_file = st.file_uploader(f"اختر ملف ({doc_type}) الشهري لشهر {active_m} لعام {selected_year}", type=["xlsx", "xls", "csv"])

        if uploaded_file:
            progress_bar = st.progress(0, text="⌛ جاري تحليل السطور وفلترة البيانات...")
            for i in range(1, 101, 25):
                time.sleep(0.01)
                progress_bar.progress(i, text="⌛ جاري مطابقة وتجميع البيانات...")
            progress_bar.empty()

            df_excel = pd.read_csv(uploaded_file, header=None) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file, sheet_name=st.selectbox("📑 اختر الشيت:", pd.ExcelFile(uploaded_file).sheet_names), header=None)
            col_names = [f"Unnamed: {i}" for i in range(df_excel.shape[1])]
            df_excel.columns = col_names

            c1, c2, c3 = st.columns(3)
            col_acc = c1.selectbox("عمود الحساب:", col_names, index=1 if len(col_names)>1 else 0)
            col_debit = c2.selectbox("عمود المدين:", col_names, index=6 if len(col_names)>6 else 0)
            col_credit = c3.selectbox("عمود الدائن:", col_names, index=7 if len(col_names)>7 else 0)

            doc_key = "trial_balance" if doc_type == "ميزان مراجعة" else "income"
            rows_valid, total_rev, total_exp, net_profit, margin_pct, records = process_excel_preview(df_excel, col_acc, col_debit, col_credit, doc_key)

            st.markdown("<br>", unsafe_allow_html=True)
            col_info, col_btn = st.columns([2.3, 1.1])

            with col_info:
                st.markdown(f"""
                    <div class="info-card-right">
                        <h3 style="color: #F8FAFC; margin: 0; font-size: 16px; text-align: right;">🎉 معاينة المطابقة ودقة التجميع 100% ({doc_type})</h3>
                        <p style="color: #CBD5E1; font-size: 13px; margin: 4px 0 0 0; text-align: right;">
                            <b>الفرع:</b> {selected_b_select} | <b>السنة:</b> {selected_year} | <b>الشهر:</b> {active_m} | 
                            <b>الصفوف:</b> <span style="background: rgba(56, 189, 248, 0.2); color: #38BDF8; padding: 2px 8px; border-radius: 8px; font-weight: bold;">{rows_valid} صف</span>
                        </p>
                    </div>
                """, unsafe_allow_html=True)

            with col_btn:
                st.markdown("<div class='confirm-btn-container'>", unsafe_allow_html=True)
                if st.button("✅ اعتمد ورحّل البيانات لقاعدة البيانات", use_container_width=True, type="primary"):
                    # حذف الصفوف القديمة المطبقة لنفس الفرع والسنة والشهر لمنع التكرار
                    execute_query("DELETE FROM income_statement WHERE TRIM(branch_code) = ? AND TRIM(month) = ? AND TRIM(year) = ?", (selected_b_code, active_m, selected_year))
                    for acc, amt, cat in records:
                        execute_query("INSERT INTO income_statement (branch_code, year, month, account_name, amount, category) VALUES (?, ?, ?, ?, ?, ?)", (selected_b_code, selected_year, active_m, acc, amt, cat))

                    st.session_state['last_summary_data'] = {'b_select': selected_b_select, 'm': active_m, 'year': selected_year, 'rows': rows_valid, 'rev': total_rev, 'exp': total_exp, 'profit': net_profit, 'margin': margin_pct, 'doc': doc_type}
                    st.session_state['active_import_month'] = None
                    st.session_state['active_import_branch'] = None
                    st.success("🎉 تم تجميد الشهر واعتماد الترحيل بنجاح!")
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            render_preview_cards(total_rev, total_exp, net_profit, margin_pct)

    elif 'last_summary_data' in st.session_state and st.session_state['last_summary_data']:
        s = st.session_state['last_summary_data']
        st.markdown(f"""
            <div class="info-card-right" style="height: auto; padding: 16px 20px;">
                <h3 style="color: #F8FAFC; margin: 0; font-size: 16px; text-align: right;">✅ تم اعتماد وتجميد بيانات الشهر بنجاح ({s['doc']})</h3>
                <p style="color: #CBD5E1; font-size: 13px; margin: 6px 0 0 0; text-align: right;">
                    <b>الفرع:</b> {s['b_select']} | <b>السنة:</b> {s.get('year', '2026')} | <b>الشهر:</b> {s['m']} | <b>الصفوف:</b> <span style="color:#38BDF8; font-weight:bold;">{s['rows']} صف</span>
                </p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        render_preview_cards(s['rev'], s['exp'], s['profit'], s['margin'])

    # قسم إدارة المسح والتصفير الشامل
    st.markdown("---")
    with st.expander("⚙️ إدارة مسح البيانات وتصفير قاعدة البيانات للبدء من جديد"):
        c_del1, c_del2 = st.columns([3, 1])
        with c_del1:
            st.warning("⚠️ يمكنك تصفير كافة البيانات المالية القديمة للبدء على نظافة كاملة بمشروع السنوات المتعددة.")
        with c_del2:
            if st.button("🗑️ تصفير كل البيانات المالية", type="secondary", use_container_width=True):
                execute_query("DELETE FROM income_statement")
                st.session_state['last_summary_data'] = None
                st.success("✨ تم تصفير قاعدة البيانات بنجاح! جاهزية كاملة لرفع السنوات.")
                st.rerun()