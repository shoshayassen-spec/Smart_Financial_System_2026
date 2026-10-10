import streamlit as st
import pandas as pd
from utils.db_manager import get_dataframe, execute_query
from pages_modules.tab1_components.tab1_ui import render_branch_form

def render():
    st.markdown("<div class='main-page-title no-print'>🏢 التبويب الأول: تكويد وإدارة بيانات الفروع</div>", unsafe_allow_html=True)

    # تهيئة حالة التعديل في Session State
    if 'edit_branch_data' not in st.session_state:
        st.session_state['edit_branch_data'] = None

    col_list, col_form = st.columns([1.3, 1])

    # 1. قسم قائمة الفروع والإدارة الإجرائية
    with col_list:
        st.subheader("📋 قائمة الفروع المسجلة")
        df_branches = get_dataframe("SELECT branch_code, branch_name, city, target, status FROM branches")

        if not df_branches.empty:
            st.dataframe(
                df_branches,
                column_config={
                    "branch_code": "كود الفرع",
                    "branch_name": "اسم الفرع",
                    "city": "المدينة",
                    "target": st.column_config.NumberColumn("التارجت (ريال)", format="%.0f ريال"),
                    "status": "الحالة"
                },
                use_container_width=True
            )

            st.markdown("---")
            st.subheader("⚙️ إجــــراءات وعمليات الفروع")
            
            b_options = (df_branches['branch_code'].astype(str) + " - " + df_branches['branch_name'].astype(str)).tolist()
            selected_b_str = st.selectbox("🎯 اختر فرع لإدارته وتعديله:", b_options)
            selected_code = selected_b_str.split(" - ")[0]

            col_edit, col_freeze, col_activate, col_del = st.columns(4)

            # زر التعديل المباشر
            with col_edit:
                if st.button("✏️ تعديل البيانات", use_container_width=True):
                    branch_info = df_branches[df_branches['branch_code'].astype(str) == selected_code].iloc[0].to_dict()
                    st.session_state['edit_branch_data'] = branch_info
                    st.rerun()

            # زر تجميد
            with col_freeze:
                if st.button("❄️ تجميد", use_container_width=True):
                    execute_query("UPDATE branches SET status = 'مجمد' WHERE branch_code = ?", (selected_code,))
                    st.toast(f"تم تجميد الفرع [{selected_code}] بنجاح", icon="❄️")
                    st.rerun()

            # زر تنشيط
            with col_activate:
                if st.button("🟢 تنشيط", use_container_width=True):
                    execute_query("UPDATE branches SET status = 'نشط' WHERE branch_code = ?", (selected_code,))
                    st.toast(f"تم تنشيط الفرع [{selected_code}] بنجاح", icon="🟢")
                    st.rerun()

            # زر حذف
            with col_del:
                if st.button("🗑️ حذف", use_container_width=True):
                    execute_query("DELETE FROM branches WHERE branch_code = ?", (selected_code,))
                    st.toast(f"تم حذف الفرع [{selected_code}] بنجاح", icon="🗑️")
                    st.rerun()
        else:
            st.info("لا توجد فروع مسجلة حتى الآن.")

    # 2. قسم نموذج الإضافة والتعديل على اليمين
    with col_form:
        if st.session_state['edit_branch_data']:
            if st.button("❌ إلغاء التعديل والعودة للإضافة"):
                st.session_state['edit_branch_data'] = None
                st.rerun()

        submit_btn, branch_code, branch_name, city, target, status, is_edit_mode = render_branch_form(st.session_state['edit_branch_data'])

        if submit_btn:
            if not branch_code or not branch_name:
                st.error("⚠️ يرجى ملء كافة الحقول الأساسية (كود الفرع واسمه).")
            else:
                if is_edit_mode:
                    execute_query("""
                        UPDATE branches 
                        SET branch_name = ?, city = ?, target = ?, status = ? 
                        WHERE branch_code = ?
                    """, (branch_name, city, target, status, branch_code))
                    st.success(f"✅ تم تحديث بيانات الفرع [{branch_code}] بنجاح!")
                    st.session_state['edit_branch_data'] = None
                    st.rerun()
                else:
                    # إضافة فرع جديد
                    check_df = get_dataframe("SELECT branch_code FROM branches WHERE branch_code = ?", (branch_code,))
                    if not check_df.empty:
                        st.error(f"⚠️ كود الفرع [{branch_code}] موجود مسبقاً! استخدم زر التعديل إذا كنت تريد تحديثه.")
                    else:
                        execute_query("""
                            INSERT INTO branches (branch_code, branch_name, city, target, status) 
                            VALUES (?, ?, ?, ?, ?)
                        """, (branch_code, branch_name, city, target, status))
                        st.success(f"🎉 تم إضافة الفرع الجديد [{branch_name}] بنجاح!")
                        st.rerun()