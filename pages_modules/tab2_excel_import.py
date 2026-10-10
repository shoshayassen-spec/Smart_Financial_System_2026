import streamlit as st
import pandas as pd
from utils.db_manager import execute_query, get_dataframe
from pages_modules.tab2_components.tab2_ui import render_month_selector, render_summary_cards, MONTHS
from pages_modules.tab2_components.tab2_logic import process_excel_preview, delete_import_data

def render():
    st.markdown("<div class='main-page-title no-print'>📥 التبويب الثاني: سحب واستيراد ملفات الإكسل الشهري</div>", unsafe_allow_html=True)
    st.info("💡 قم برفع ملفات القوائم المالية الشهرية وسجلات الحسابات المعتمدة بصيغة XLSX أو CSV.")

    branches_df = get_dataframe("SELECT branch_code, branch_name FROM branches")
    if branches_df.empty:
        st.error("⚠️ لا توجد فروع مسجلة! يرجى إضافة فروع أولاً من التبويب الأول.")
        return

    b_list = (branches_df['branch_code'].astype(str) + " - " + branches_df['branch_name'].astype(str)).tolist()
    st.markdown("### 1️⃣ اختر الفرع المراد سحب البيانات له:")
    selected_b_select = st.selectbox("🎯 اختر الفرع:", b_list)
    selected_b_code = selected_b_select.split(" - ")[0]

    df_branch_months = get_dataframe("SELECT DISTINCT month FROM income_statement WHERE branch_code = ?", (selected_b_code,))
    locked_months = df_branch_months['month'].tolist() if not df_branch_months.empty else []

    render_month_selector(selected_b_code, locked_months)

    active_m, active_b = st.session_state.get('active_import_month'), st.session_state.get('active_import_branch')

    if active_m and active_b == selected_b_code:
        st.markdown("---")
        uploaded_file = st.file_uploader(f"اختر ملف الإكسل الشهري لشهر {active_m}", type=["xlsx", "xls", "csv"])

        if uploaded_file:
            df_excel = pd.read_csv(uploaded_file, header=None) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file, sheet_name=st.selectbox("📑 اختر الشيت:", pd.ExcelFile(uploaded_file).sheet_names), header=None)
            col_names = [f"Unnamed: {i}" for i in range(df_excel.shape[1])]
            df_excel.columns = col_names

            c1, c2, c3 = st.columns(3)
            col_acc = c1.selectbox("عمود الحساب:", col_names, index=1 if len(col_names)>1 else 0)
            col_debit = c2.selectbox("عمود المدين:", col_names, index=6 if len(col_names)>6 else 0)
            col_credit = c3.selectbox("عمود الدائن:", col_names, index=7 if len(col_names)>7 else 0)

            rows_valid, total_rev, total_exp, net_profit, records = process_excel_preview(df_excel, col_acc, col_debit, col_credit)

            render_summary_cards(selected_b_select, active_m, rows_valid, total_rev, total_exp, net_profit)

            if st.button("✅ تأكيد دقة الأرقام واعتمد الترحيل النهائي للقاعدة", use_container_width=True, type="primary"):
                execute_query("DELETE FROM income_statement WHERE branch_code = ? AND month = ?", (selected_b_code, active_m))
                for acc, amt, cat in records:
                    execute_query("INSERT INTO income_statement (branch_code, month, account_name, amount, category) VALUES (?, ?, ?, ?, ?)", (selected_b_code, active_m, acc, amt, cat))

                st.session_state['last_summary_data'] = {'b_select': selected_b_select, 'm': active_m, 'rows': rows_valid, 'rev': total_rev, 'exp': total_exp, 'profit': net_profit}
                st.session_state['active_import_month'] = None
                st.session_state['active_import_branch'] = None
                st.success("🎉 تم حفظ وترحيل البيانات بنجاح وتجميد الشهر!")
                st.rerun()

    elif 'last_summary_data' in st.session_state and st.session_state['last_summary_data']:
        s = st.session_state['last_summary_data']
        render_summary_cards(s['b_select'], s['m'], s['rows'], s['rev'], s['exp'], s['profit'])

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
            else:
                st.warning("يرجى تحديد شهر واحد على الأقل.")