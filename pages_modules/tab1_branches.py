import sys
import os
import streamlit as st
import pandas as pd

# ضمان معرفة المسار الرئيسي للنظام
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.db_manager import execute_query, get_dataframe

def render():
    st.markdown("<div class='main-header'>🏢 التبويب الأول: تكويد وبيانات الفروع</div>", unsafe_allow_html=True)
    st.info("💡 يتم هنا إدارة السجلات والتكويد الأساسي لجميع فروع ومناطق الشركة.")

    col_form, col_view = st.columns([1.2, 1.8])

    with col_form:
        st.subheader("➕ إضافة / تعديل فرع")
        with st.form("branch_form", clear_on_submit=True):
            b_code = st.text_input("كود الفرع (مثال: 101 أو 0001)")
            b_name = st.text_input("اسم الفرع الجديد:")
            
            cities_list = ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام", "الخبر", "القصيم", "أبها", "تبوك", "أخرى"]
            b_city = st.selectbox("المدينة / المنطقة:", cities_list)
            
            b_manager = st.text_input("اسم مدير الفرع:")
            b_target = st.number_input("تارجت المبيعات الشهري (ريال):", min_value=0.0, value=150000.0, step=5000.0)
            b_status = st.selectbox("حالة الفرع:", ["نشط", "مجمد", "موقوف"])

            submitted = st.form_submit_button("💾 حفظ بيانات الفرع")
            if submitted:
                if b_code and b_name and b_city:
                    execute_query("""
                        INSERT INTO branches (branch_code, branch_name, city, target, status)
                        VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(branch_code) DO UPDATE SET
                        branch_name=excluded.branch_name,
                        city=excluded.city,
                        target=excluded.target,
                        status=excluded.status
                    """, (b_code.strip(), b_name.strip(), b_city.strip(), b_target, b_status))
                    st.success("✨ تم حفظ بيانات الفرع بنجاح!")
                    st.rerun()
                else:
                    st.error("⚠️ يرجى إكمال الحقول الأساسية (الكود، الاسم، والمدينة)!")

    with col_view:
        st.subheader("📋 قائمة الفروع المسجلة")
        df_branches = get_dataframe("SELECT branch_code AS 'كود الفرع', branch_name AS 'اسم الفرع', city AS 'المدينة', target AS 'التارجت', status AS 'الحالة' FROM branches")
        
        if not df_branches.empty:
            st.dataframe(df_branches, use_container_width=True)
            st.markdown("---")
            
            branch_options = (df_branches['كود الفرع'].astype(str) + " - " + df_branches['اسم الفرع'].astype(str)).tolist()
            selected_b = st.selectbox("🎯 اختر فرع لإدارته التفصيلية:", branch_options)
            code_to_act = selected_b.split(" - ")[0]

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("🗑️ حذف الفرع", type="primary"):
                    execute_query("DELETE FROM branches WHERE branch_code = ?", (code_to_act,))
                    execute_query("DELETE FROM income_statement WHERE branch_code = ?", (code_to_act,))
                    st.success("تم حذف الفرع وبياناته بنجاح!")
                    st.rerun()
            with c2:
                if st.button("❄️ تجميد الفرع"):
                    execute_query("UPDATE branches SET status = 'مجمد' WHERE branch_code = ?", (code_to_act,))
                    st.warning("تم تجميد الفرع.")
                    st.rerun()
            with c3:
                if st.button("🟢 تنشيط الفرع"):
                    execute_query("UPDATE branches SET status = 'نشط' WHERE branch_code = ?", (code_to_act,))
                    st.success("تم إعادة تنشيط الفرع.")
                    st.rerun()
        else:
            st.info("لا توجد فروع مسجلة حتى الآن. قم بتكويد أول فرع من النموذج الأيمن.")