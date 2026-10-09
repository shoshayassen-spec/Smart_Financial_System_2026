import streamlit as st
import pandas as pd
from utils.db_manager import execute_query, get_dataframe

MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"]

def render():
    st.markdown("<div class='main-header'>📥 التبويب الثاني: سحب واستيراد ملفات الإكسل</div>", unsafe_allow_html=True)
    st.info("💡 قم برفع ملفات القوائم المالية الشهرية وسجلات الحسابات المعتمدة بصيغة XLSX أو CSV.")

    branches_df = get_dataframe("SELECT branch_code, branch_name FROM branches")

    if not branches_df.empty:
        b_list = (branches_df['branch_code'].astype(str) + " - " + branches_df['branch_name'].astype(str)).tolist()

        st.markdown("### 1️⃣ اختر الفرع المراد سحب البيانات له:")
        selected_b_select = st.selectbox("🎯 اختر الفرع:", b_list)
        selected_b_code = selected_b_select.split(" - ")[0]

        df_branch_months = get_dataframe("SELECT DISTINCT month FROM income_statement WHERE branch_code = ?", (selected_b_code,))
        locked_months_for_branch = df_branch_months['month'].tolist() if not df_branch_months.empty else []

        st.markdown("### 2️⃣ اضغط على الشهر المطلوب لسحب بياناته (الشهور المكتملة تظهر بحالة مجمدة 🔒):")

        cols = st.columns(6)
        for idx, m in enumerate(MONTHS):
            col = cols[idx % 6]
            is_disabled = m in locked_months_for_branch
            label = f"🔒 {m}" if is_disabled else f"📅 {m}"
            if col.button(label, key=f"btn_m_{selected_b_code}_{m}", disabled=is_disabled):
                st.session_state['active_import_month'] = m
                st.session_state['active_import_branch'] = selected_b_code

        active_m = st.session_state.get('active_import_month', None)
        active_b = st.session_state.get('active_import_branch', None)

        if active_m and active_b == selected_b_code:
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

                st.write("🔍 **معاينة البيانات الأولية:**")
                st.dataframe(df_excel.head(10), use_container_width=True)

                st.markdown("#### 🛠️ تحديد أعمدة الحركة خلال الفترة (لمنع الجمع المزدوج):")
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

                if st.button("🚀 تأكيد السحب والترحيل المباشر للقيم"):
                    execute_query("DELETE FROM income_statement WHERE branch_code = ? AND month = ?", (selected_b_code, active_m))

                    rows_imported = 0
                    total_rev = 0.0
                    total_exp = 0.0

                    for row_idx, row in df_excel.iterrows():
                        acc_name = str(row[col_acc]).strip()

                        if pd.isna(row[col_acc]) or any(k in acc_name for k in ["None", "اسم", "رقم الحساب", "nan", "", "الاسم", "إجمالي", "المجموع", "الرصيد"]):
                            continue

                        try:
                            val_debit = float(row[col_debit]) if pd.notna(row[col_debit]) else 0.0
                        except:
                            val_debit = 0.0

                        try:
                            val_credit = float(row[col_credit]) if pd.notna(row[col_credit]) else 0.0
                        except:
                            val_credit = 0.0

                        if val_debit > 0:
                            total_exp += val_debit
                            execute_query("""
                                INSERT INTO income_statement (branch_code, month, account_name, amount, category)
                                VALUES (?, ?, ?, ?, ?)
                            """, (selected_b_code, active_m, acc_name, val_debit, "مصروفات"))
                            rows_imported += 1

                        if val_credit > 0:
                            total_rev += val_credit
                            execute_query("""
                                INSERT INTO income_statement (branch_code, month, account_name, amount, category)
                                VALUES (?, ?, ?, ?, ?)
                            """, (selected_b_code, active_m, acc_name, val_credit, "إيرادات"))
                            rows_imported += 1

                    net_profit = total_rev - total_exp
                    status_str = "ربح 🟢" if net_profit >= 0 else "خسارة 🔴"
                    card_color = "#ECFDF5" if net_profit >= 0 else "#FEF2F2"
                    border_color = "#10B981" if net_profit >= 0 else "#EF4444"

                    st.markdown(f"""
                        <div style='background-color: {card_color}; border: 2px solid {border_color}; border-radius: 12px; padding: 20px; margin-top: 20px;'>
                            <h3>✅ تم سحب البيانات ودقة التجميع 100%!</h3>
                            <p><b>الفرع:</b> {selected_b_select} | <b>الشهر:</b> {active_m} | <b>عدد الصفوف المرحّلة:</b> {rows_imported}</p>
                            <hr>
                            <h4>📊 الخلاصة الحقيقية للقائمة المالية:</h4>
                            <ul>
                                <li><b>إجمالي الإيرادات (الدائن الحقيقي):</b> {total_rev:,.2f} ريال</li>
                                <li><b>إجمالي المصروفات (المدين الحقيقي):</b> {total_exp:,.2f} ريال</li>
                                <li><b>صافي الربح / الخسارة:</b> <span style='font-size: 20px; font-weight: bold;'>{net_profit:,.2f} ريال ({status_str})</span></li>
                            </ul>
                        </div>
                    """, unsafe_allow_html=True)

                    st.session_state['active_import_month'] = None
                    st.session_state['active_import_branch'] = None
                    st.rerun()
    else:
        st.error("⚠️ لا توجد فروع مسجلة! يرجى إضافة فروع أولاً من التبويب الأول.")

    st.markdown("---")
    st.markdown("### 🗑️ مسح وإعادة تنشيط سحب الشهور والفروع")
    with st.expander("إدارة مسح البيانات لإعادة السحب"):
        branches_data = get_dataframe("SELECT branch_code, branch_name FROM branches")
        b_options = ["جميع الفروع"] + (branches_data['branch_code'].astype(str) + " - " + branches_data['branch_name'].astype(str)).tolist() if not branches_data.empty else ["جميع الفروع"]

        del_branches = st.multiselect("🎯 اختر الفرع / الفروع لمسح بياناتها (اختيار متعدد):", b_options, default=["جميع الفروع"])
        del_months = st.multiselect("📅 اختر الشهر / الشهور المراد مسحها (اختيار متعدد):", MONTHS)

        if st.button("⚠️ تأكيد مسح البيانات وإعادة فتح زر السحب"):
            if del_months:
                selected_codes = [b.split(" - ")[0] for b in del_branches if "جميع الفروع" not in b]
                for m in del_months:
                    if "جميع الفروع" in del_branches or not selected_codes:
                        execute_query("DELETE FROM income_statement WHERE month = ?", (m,))
                    else:
                        for code in selected_codes:
                            execute_query("DELETE FROM income_statement WHERE month = ? AND branch_code = ?", (m, code))
                st.success("✨ تم مسح البيانات المحددة بنجاح واُعيد فتح إمكانية السحب!")
                st.rerun()
            else:
                st.warning("يرجى تحديد شهر واحد على الأقل للمسح.")