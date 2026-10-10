import streamlit as st
import pandas as pd
from utils.db_manager import execute_query, get_dataframe

# قاموس الدول والمدن التفاعلي
GEO_DATA = {
    "المملكة العربية السعودية": ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام", "الخبر", "الظهران", "الأحساء", "التبوك", "أبها", "خميس مشيط", "جازان", "نجران", "حائل", "القصيم - بريدة", "عنيزة", "الطائف", "الجبيل", "ينبع"],
    "الإمارات العربية المتحدة": ["أبوظبي", "دبي", "الشارقة", "عجمان", "رأس الخيمة", "الفجيرة", "العين"],
    "دولة الكويت": ["الكويت العاصمة", "حولي", "الأحمدي", "الفروانية", "الجهراء", "مبارك الكبير"],
    "دولة قطر": ["الدوحة", "الريان", "الوكرة", "الخور"],
    "مملكة البحرين": ["المنامة", "المحرق", "الرفاع"],
    "سلطنة عمان": ["مسقط", "صلالة", "صحار"],
    "جمهورية مصر العربية": ["القاهرة", "الإسكندرية", "الجيزة", "المنصورة", "طنطا"],
    "أخرى": ["أخرى"]
}

def render():
    st.markdown("<div class='main-page-title no-print'>🏢 التبويب الأول: تكويد وإدارة بيانات الفروع</div>", unsafe_allow_html=True)

    # 1. إضافة فرع جديد
    with st.expander("➕ إضافة فرع جديد", expanded=True):
        c1, c2, c3 = st.columns([1, 2, 1.5])
        with c1:
            code = st.text_input("كود الفرع:", placeholder="101")
        with c2:
            name = st.text_input("اسم الفرع:", placeholder="فرع الرياض - الرئيسي")
        with c3:
            country = st.selectbox("الدولة:", list(GEO_DATA.keys()), key="add_country")

        c4, c5, c6 = st.columns([2, 1.5, 1])
        with c4:
            city_options = GEO_DATA.get(country, ["أخرى"])
            city = st.selectbox("المدينة (ابحث عن المدينة):", city_options, key="add_city")
        with c5:
            target = st.number_input("المستهدف الشهري (ريال):", min_value=0.0, value=100000.0, step=5000.0)
        with c6:
            status = st.selectbox("الحالة:", ["نشط", "مقفل"], key="add_status")

        if st.button("💾 حفظ البيانات", type="primary", use_container_width=True):
            if code and name:
                try:
                    execute_query("""
                        INSERT OR REPLACE INTO branches (branch_code, branch_name, country, city, target, status) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (code.strip(), name.strip(), country, city, target, status))
                    st.success(f"🎉 تم إضافة/تحديث الفرع [{name}] بنجاح!")
                    st.rerun()
                except Exception as e:
                    st.error(f"🚨 خطأ في الحفظ: {e}")
            else:
                st.warning("⚠️ يرجى ملء كود واسم الفرع على الأقل.")

    st.markdown("---")

    # 2. عرض الفروع المسجلة والإدارة (تعديل وحذف)
    st.markdown("### 📋 قائمة الفروع المسجلة")
    df_branches = get_dataframe("SELECT branch_code, branch_name, country, city, target, status FROM branches")

    if not df_branches.empty:
        df_display = df_branches.rename(columns={
            "branch_code": "كود الفرع",
            "branch_name": "اسم الفرع",
            "country": "الدولة",
            "city": "المدينة",
            "target": "المستهدف الشهري (ريال)",
            "status": "الحالة"
        })
        st.dataframe(df_display, use_container_width=True)

        col_edit, col_del = st.columns(2)

        # قسم التعديل
        with col_edit:
            with st.expander("✏️ تعديل بيانات فرع"):
                branch_list = df_branches["branch_code"].astype(str) + " - " + df_branches["branch_name"]
                selected_b = st.selectbox("اختر الفرع للتعديل:", branch_list, key="edit_select")
                
                if selected_b:
                    b_code = selected_b.split(" - ")[0]
                    curr_data = df_branches[df_branches["branch_code"].astype(str) == b_code].iloc[0]

                    edit_name = st.text_input("اسم الفرع الجديد:", value=str(curr_data["branch_name"]), key="e_name")
                    
                    # تحديد الدولة والمدينة الحالية
                    curr_country = curr_data["country"] if pd.notnull(curr_data["country"]) else "المملكة العربية السعودية"
                    country_idx = list(GEO_DATA.keys()).index(curr_country) if curr_country in GEO_DATA else 0
                    
                    edit_country = st.selectbox("الدولة:", list(GEO_DATA.keys()), index=country_idx, key="e_country")
                    
                    cities_list = GEO_DATA.get(edit_country, ["أخرى"])
                    curr_city = curr_data["city"] if pd.notnull(curr_data["city"]) else cities_list[0]
                    city_idx = cities_list.index(curr_city) if curr_city in cities_list else 0
                    
                    edit_city = st.selectbox("المدينة:", cities_list, index=city_idx, key="e_city")
                    edit_target = st.number_input("المستهدف الشهري:", value=float(curr_data["target"]), step=5000.0, key="e_target")
                    
                    curr_status = curr_data["status"] if pd.notnull(curr_data["status"]) else "نشط"
                    status_idx = 0 if curr_status == "نشط" else 1
                    edit_status = st.selectbox("الحالة:", ["نشط", "مقفل"], index=status_idx, key="e_status")

                    if st.button("🔄 حفظ التعديلات", type="primary", use_container_width=True):
                        execute_query("""
                            UPDATE branches 
                            SET branch_name = ?, country = ?, city = ?, target = ?, status = ? 
                            WHERE branch_code = ?
                        """, (edit_name.strip(), edit_country, edit_city, edit_target, edit_status, b_code))
                        st.success("✨ تم تحديث بيانات الفرع بنجاح!")
                        st.rerun()

        # قسم الحذف
        with col_del:
            with st.expander("🗑️ حذف فرع"):
                b_to_del = st.selectbox("اختر الفرع المراد حذفه:", branch_list, key="del_select")
                if st.button("تأكيد الحذف", type="secondary", use_container_width=True):
                    del_code = b_to_del.split(" - ")[0]
                    execute_query("DELETE FROM branches WHERE branch_code = ?", (del_code,))
                    st.success("✨ تم حذف الفرع بنجاح!")
                    st.rerun()
    else:
        st.info("💡 لا توجد فروع مسجلة حتى الآن. قم بإضافة فرعك الأول أعلاه.")