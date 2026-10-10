import streamlit as st
import pandas as pd
from utils.db_manager import execute_query, get_dataframe

def render():
    st.markdown("<div class='main-page-title no-print'>🏢 التبويب الأول: تكويد وإدارة بيانات الفروع</div>", unsafe_allow_html=True)

    # 1. إضافة فرع جديد
    with st.expander("➕ إضافة فرع جديد", expanded=True):
        col1, col2, col3, col4 = st.columns([1, 2, 2, 1.5])
        with col1:
            code = st.text_input("كود الفرع:", placeholder="101")
        with col2:
            name = st.text_input("اسم الفرع:", placeholder="فرع الرياض - الرئيسي")
        with col3:
            city = st.text_input("المدينة:", placeholder="الرياض")
        with col4:
            target = st.number_input("المستهدف الشهري (ريال):", min_value=0.0, value=100000.0, step=5000.0)

        if st.button("💾 حفظ البيانات", type="primary", use_container_width=True):
            if code and name:
                try:
                    execute_query("INSERT OR REPLACE INTO branches (branch_code, branch_name, city, target) VALUES (?, ?, ?, ?)", 
                                  (code.strip(), name.strip(), city.strip(), target))
                    st.success(f"🎉 تم إضافة/تحديث الفرع [{name}] بنجاح!")
                    st.rerun()
                except Exception as e:
                    st.error(f"🚨 خطأ في الحفظ: {e}")
            else:
                st.warning("⚠️ يرجى ملء كود واسم الفرع على الأقل.")

    st.markdown("---")

    # 2. عرض الفروع المسجلة أمان تام
    st.markdown("### 📋 قائمة الفروع المسجلة")
    
    # جلب الجدول بالكامل تجنباً لأي اختلاف في أسماء الأعمدة
    df_branches = get_dataframe("SELECT * FROM branches")

    if not df_branches.empty:
        # عرض الأعمدة المتاحة فقط بأمان
        cols_map = {
            "branch_code": "كود الفرع",
            "branch_name": "اسم الفرع",
            "city": "المدينة",
            "target": "المستهدف الشهري (ريال)",
            "status": "الحالة"
        }
        df_display = df_branches.rename(columns=cols_map)
        st.dataframe(df_display, use_container_width=True)
        
        # حذف فرع
        with st.expander("🗑️ حذف فرع"):
            b_to_del = st.selectbox("اختر الفرع المراد حذفه:", df_branches["branch_code"].astype(str) + " - " + df_branches["branch_name"])
            if st.button("تأكيد الحذف", type="secondary"):
                del_code = b_to_del.split(" - ")[0]
                execute_query("DELETE FROM branches WHERE branch_code = ?", (del_code,))
                st.success("✨ تم حذف الفرع بنجاح!")
                st.rerun()
    else:
        st.info("💡 لا توجد فروع مسجلة حتى الآن. قم بتمويل القائمة بإضافة فرعك الأول أعلاه.")