import streamlit as st
from pages_modules.tab1_components.tab1_cities_data import COUNTRIES_CITIES

def render_branch_form(selected_branch_to_edit=None):
    """
    نموذج إضافة/تعديل فرع
    """
    is_edit_mode = selected_branch_to_edit is not None

    if is_edit_mode:
        st.subheader("✏️ تعديل بيانات الفرع الحالي")
        default_code = str(selected_branch_to_edit.get('branch_code', ''))
        default_name = str(selected_branch_to_edit.get('branch_name', ''))
        default_city = str(selected_branch_to_edit.get('city', 'الرياض'))
        default_target = float(selected_branch_to_edit.get('target', 0.0))
        default_status = str(selected_branch_to_edit.get('status', 'نشط'))
    else:
        st.subheader("➕ إضافة فرع جديد")
        default_code = ""
        default_name = ""
        default_city = "الرياض"
        default_target = 0.0
        default_status = "نشط"

    with st.form(key="branch_management_form", clear_on_submit=not is_edit_mode):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            country = st.selectbox("🌍 اختر الدولة:", list(COUNTRIES_CITIES.keys()))
        with col_c2:
            cities_options = COUNTRIES_CITIES.get(country, COUNTRIES_CITIES["المملكة العربية السعودية 🇸🇦"])
            # دعم البحث السريع المدمج داخل selectbox
            city_idx = cities_options.index(default_city) if default_city in cities_options else 0
            city = st.selectbox("🏙️ المدينة / المنطقة (البحث سريع):", cities_options, index=city_idx)

        branch_code = st.text_input("كود الفرع (مثال: 101 أو 0001):", value=default_code, disabled=is_edit_mode)
        branch_name = st.text_input("اسم الفرع الجديد / المعدل:", value=default_name)
        target = st.number_input("المستهدف الشهري (ريال):", value=default_target, step=1000.0)
        status = st.selectbox("حالة الفرع:", ["نشط", "مجمد"], index=0 if default_status == "نشط" else 1)

        btn_label = "💾 حفظ التعديلات" if is_edit_mode else "➕ إضافة الفرع"
        submit_btn = st.form_submit_button(btn_label, use_container_width=True)

    return submit_btn, branch_code, branch_name, city, target, status, is_edit_mode