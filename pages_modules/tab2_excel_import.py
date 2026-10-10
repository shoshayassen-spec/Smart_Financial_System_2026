import streamlit as st
import pandas as pd
import time
from utils.db_manager import execute_query, get_dataframe
from pages_modules.tab2_components.tab2_ui import render_month_selector, render_preview_header_and_cards, MONTHS
from pages_modules.tab2_components.tab2_logic import process_excel_preview, delete_import_data

def render():
    st.markdown("<div class='main-page-title no-print'>📥 التبويب الثاني: سحب واستيراد ملفات الإكسل الشهري</div>", unsafe_allow_html=True)

    branches_df = get_dataframe("SELECT branch_code, branch_name FROM branches")
    if branches_df.empty:
        st.error("⚠️ لا توجد فروع مسجلة! يرجى إضافة فروع أولاً من التبويب الأول.")
        return

    b_list = (branches_df['branch_code'].astype(str) + " - " + branches_df['branch_name'].astype(str)).tolist()
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        selected_b_select = st.selectbox("🎯 1️⃣ اختر الفرع:", b_list)
    with col_b:
        doc_type = st.radio("📄 2️⃣ نوع القائمة المرفوعة:", ["قائمة دخل", "ميزان مراجعة"], horizontal=True)

    selected_b_code = selected_b_select.split(" - ")[0]
    locked_months = (get_dataframe("SELECT DISTINCT month FROM income_statement WHERE branch_code = ?", (selected_b_code,))['month'].tolist()) if not get_dataframe("SELECT DISTINCT month FROM income_statement WHERE branch_code = ?", (selected_b_code,)).empty else []

    render_month_selector(selected_b_code, locked_months)

    active_m, active_b = st.session_state.get('active_import_month'), st.session_state.get('active_import_branch')

    if active_m and active_b == selected_b_code:
        st.markdown("---")
        uploaded_file = st.file_uploader(f"اختر ملف ({doc_type}) الشهري لشهر {active_m}", type=["xlsx", "xls", "csv"])

        if uploaded_file:
            # شريط التقدم الفوري
            progress_bar = st.progress(0, text="⌛ جاري تحليل السطور وفلترة البيانات...")
            for i in range(1, 101, 20):
                time.sleep(0.01)
                progress_bar.progress(i, text="⌛ جاري مطابقة وتجميع الميزان وقائمة الدخل...")
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

            # عرض البانر الموحد والكروت
            render_preview_header_and_cards(selected_b_select, active_m, rows_valid, total_rev, total_exp, net_profit, margin_pct, doc_type)

            st.markdown("<br>", unsafe_allow_html=True)
            # زر الاعتماد الرئيسي ومحاذاته
            if st.button("✅ اعتمد ورحّل البيانات النهائية لقاعدة البيانات", use_container_width=True, type="primary"):
                execute_query("DELETE FROM income_statement WHERE branch_code = ? AND month = ?", (selected_b_code, active_m))
                for acc, amt, cat in records:
                    execute_query("INSERT INTO income_statement (branch_code, month, account_name, amount, category) VALUES (?, ?, ?, ?, ?)", (selected_b_code, active_m, acc, amt, cat))

                st.session_state['last_summary_data'] = {'b_select': selected_b_select, 'm': active_m, 'rows': rows_valid, 'rev': total_rev, 'exp': total_exp, 'profit': net_profit, 'margin': margin_pct, 'doc': doc_type}
                st.session_state['active_import_month'] = None
                st.session_state['active_import_branch'] = None
                st.success("🎉 تم تجميد الشهر واعتماد الترحيل بنجاح!")
                st.rerun()

    elif 'last_summary_data' in st.session_state and st.session_state['last_summary_data']:
        s = st.session_state['last_summary_data']
        render_preview_header_and_cards(s['b_select'], s['m'], s['rows'], s['rev'], s['exp'], s['profit'], s['margin'], s['doc'])

    # قسم إدارة المسح
    st.markdown("---")
    with st.expander("⚙️ إدارة مسح البيانات وإعادة فتح الشهور للسحب"):
        del_branches = st.multiselect("🎯 اختر الفرع:", ["جميع الفروع"] + b_list, default=["جميع الفروع"])
        del_months = st.multiselect("📅 اختر الشهر:", MONTHS)
        if st.button("⚠️ تأكيد مسح البيانات وإعادة فتح زر السحب", use_container_width=True):
            if delete_import_data(del_branches, del_months):
                st.session_state['last_summary_data'] = None
                st.success("✨ تم مسح البيانات المحددة بنجاح!")
                st.rerun()