import streamlit as st

def render():
    st.markdown("<div class='main-header'>⚙️ التبويب السابع: إعدادات النظام وتفريغ الذاكرة</div>", unsafe_allow_html=True)
    if st.button("🧹 تفريغ الذاكرة المؤقتة (Clear Cache)"):
        st.cache_data.clear()
        st.success("✅ تم تفريغ الذاكرة المؤقتة بنجاح!")