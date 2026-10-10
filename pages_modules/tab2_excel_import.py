import streamlit as st
import pandas as pd
import re
from utils.db_manager import execute_query, get_dataframe
from pages_modules.tab2_components.tab2_ui import render_month_selector, render_summary_cards, MONTHS

def clean_float(val):
    """تنظيف وتنقية القيم الرقمية بدقة عالية"""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    cleaned_str = re.sub(r'[^\d.-]', '', str(val))
    try:
        return float(cleaned_str) if cleaned_str else 0.0
    except:
        return 0.0

def process_excel_preview(df_excel, col_acc, col_debit, col_credit):
    """معالجة وحساب الأرقام ومطابقتها قبل الاعتماد"""
    rows_valid = 0
    total_rev = 0.0
    total_exp = 0.0
    records_to_insert = []

    for row_idx, row in df_excel.iterrows():
        acc_val = row[col_acc]
        if pd.isna(acc_val):
            continue

        acc_name = str(acc_val).strip()
        if acc_name in ["None", "nan", ""] or any(k == acc_name for k in ["الاسم", "اسم الحساب", "رقم الحساب"]):
            continue

        val_debit = clean_float(row[col_debit])
        val_credit = clean_float(row[col_credit])

        if val_debit > 0:
            total_exp += val_debit
            records_to_insert.append((acc_name, val_debit, "مصروفات"))
            rows_valid += 1

        if val_credit > 0:
            total_rev += val_credit
            records_to_insert.append((acc_name, val_credit, "إيرادات"))
            rows_valid += 1

    net_profit = total_rev - total_exp
    return rows_valid, total_rev, total_exp, net_profit, records_to_insert

def render():
    st.markdown("<div class='main-page-title no-print'>📥 التبويب الثاني: سحب واستيراد ملفات الإكسل الشهري</div>", unsafe_allow_html=True)
    st.info("💡 قم برفع ملفات القوائم المالية الشهرية وسجلات الحسابات المعتمدة بصيغة XLSX أو CSV.")

    branches_df = get_dataframe("SELECT branch_code, branch_name FROM branches")

    if not branches_df.empty:
        b_list = (branches_df['branch_code'].astype(str) + " - " + branches_df['branch_name'].astype(str)).tolist()

        st.markdown("### 1️⃣ اختر الفرع المراد سحب البيانات له:")
        selected_b_select = st.selectbox("🎯 اختر الفرع:", b_list)
        selected_b_code = selected_b_select.split(" - ")[0]

        df_branch_months = get_dataframe("SELECT DISTINCT month FROM income_statement WHERE branch_code = ?", (selected_b_code,))
        locked_months_for_branch = df_branch_months['month'].tolist() if not df_branch_months.empty else []

        render_month_selector(selected_b_code, locked_months_for_branch)

        active_m = st.session_state.get('active_import_month', None)
        active_b = st.session_state.get('active_import_branch', None)

        if active_m and active_b == selected_b_code:
            st.markdown("---")
            st.success(f"✨ تم اختيار **شهر {active_m}** للفرع **[{selected_b_select}]**.")
            
            uploaded_file = st.file_uploader(f"اختر ملف الإكسل الشهري الخاص بشهر {active_m}", type=["xlsx", "xls", "csv"])

            if uploaded_file:
                if uploaded_file.name.endswith('.csv'):
                    df_excel = pd.read_csv(uploaded_file, header=None)
                else:
                    xls = pd.ExcelFile(uploaded_file)
                    sheet_names = xls.sheet_names
                    sheet_name = st.selectbox("📑 اختر الشيت المراد سحبه:", sheet_names)
                    df_excel = pd.read_excel(uploaded_file, sheet_name=sheet_name, header=None)

                col_names = [f"Unnamed: {i}" for i in range(df_excel.shape[1])]
                df_excel.columns = col_names

                st.markdown("<div class='glass-panel-3d'>", unsafe_allow_html=True)
                st.markdown("#### 🛠️ تحديد أعمدة الحركة ومعاينة الحساب الفوري:")
                c1, c2, c3 = st.columns(3)

                idx_acc = 1 if len(col_names) > 1 else 0
                idx_debit = 6 if len(col_names) > 6 else 0
                idx_credit = 7 if len(col_names) > 7 else 0

                with c1:
                    col_acc = st.selectbox("عمود اسم الحساب (العمود B):", col_names, index=idx_acc)
                with c2:
                    col_debit = st.selectbox("عمود الحركة - مدين (العمود G):", col_names, index=idx_debit)
                with c3:
                    col_credit = st.selectbox("عمود الحركة - دائن (العمود H):", col_names, index=idx_credit)

                # حساب وتجميع أرقام المعاينة فورياً
                rows_valid, total_rev, total_exp, net_profit, records_to_insert = process_excel_preview(df_excel, col_acc, col_debit, col_credit)

                # عرض كروت المطابقة الفورية للأرقام وسجل عدد السطور
                st.markdown("---")
                st.markdown("#### 📊 نتائج المطابقة الفورية للأرقام وسجل السطور المكتشفة:")
                render_summary_cards(selected_b_select, active_m, rows_valid, total_rev, total_exp, net_profit)

                st.markdown("<br>", unsafe_allow_html=True)
                
                # زر الاعتماد النهائي بعد المطابقة
                if st.button("✅ تأكيد دقة الأرقام واعتمد الترحيل النهائي للقاعدة", use_container_width=True, type="primary"):
                    execute_query("DELETE FROM income_statement WHERE branch_code = ? AND month = ?", (selected_b_code, active_m))

                    for acc_name, amount, category in records_to_insert:
                        execute_query("""
                            INSERT INTO income_statement (branch_code, month, account_name, amount, category)
                            VALUES (?, ?, ?, ?, ?)
                        """, (selected_b_code, active_m, acc_name, amount, category))

                    st.session_state['last_summary_data'] = {
                        'b_select': selected_b_select,
                        'm': active_m,
                        'rows': rows_valid,
                        'rev': total_rev,
                        'exp': total_exp,
                        'profit': net_profit
                    }

                    st.session_state['active_import_month'] = None
                    st.session_state['active_import_branch'] = None
                    st.success("🎉 تم حفظ وترحيل البيانات بنجاح وتجميد الشهر!")
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

        elif 'last_summary_data' in st.session_state and st.session_state['last_summary_data']:
            s = st.session_state['last_summary_data']
            render_summary_cards(s['b_select'], s['m'], s['rows'], s['rev'], s['exp'], s['profit'])

    else:
        st.error("⚠️ لا توجد فروع مسجلة! يرجى إضافة فروع أولاً من التبويب الأول.")

    # قسم إدارة المسح
    st.markdown("---")
    st.markdown("### 🗑️ مسح وإعادة تنشيط سحب الشهور والفروع")
    with st.expander("⚙️ إدارة مسح البيانات وإعادة فتح الشهور للسحب"):
        branches_data = get_dataframe("SELECT branch_code, branch_name FROM branches")
        b_options = ["جميع الفروع"] + (branches_data['branch_code'].astype(str) + " - " + branches_data['branch_name'].astype(str)).tolist() if not branches_data.empty else ["جميع الفروع"]

        del_branches = st.multiselect("🎯 اختر الفرع / الفروع لمسح بياناتها (اختيار متعدد):", b_options, default=["جميع الفروع"])
        del_months = st.multiselect("📅 اختر الشهر / الشهور المراد مسحها (اختيار متعدد):", MONTHS)

        if st.button("⚠️ تأكيد مسح البيانات وإعادة فتح زر السحب", use_container_width=True):
            if del_months:
                selected_codes = [b.split(" - ")[0] for b in del_branches if "جميع الفروع" not in b]
                for m in del_months:
                    if "جميع الفروع" in del_branches or not selected_codes:
                        execute_query("DELETE FROM income_statement WHERE month = ?", (m,))
                    else:
                        for code in selected_codes:
                            execute_query("DELETE FROM income_statement WHERE month = ? AND branch_code = ?", (m, code))
                
                if 'last_summary_data' in st.session_state:
                    st.session_state['last_summary_data'] = None

                st.success("✨ تم مسح البيانات المحددة بنجاح وأُعيد فتح إمكانية السحب!")
                st.rerun()
            else:
                st.warning("يرجى تحديد شهر واحد على الأقل للمسح.")