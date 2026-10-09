import streamlit as st

def render():
    st.markdown("<div class='main-header'>📈 التبويب الخامس: التجميع المالي والمؤشرات الشاملة</div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("إجمالي المبيعات المجمعة", "3,460,000 ريال", "+11.4%")
    m2.metric("إجمالي صافي الأرباح", "680,000 ريال", "+8.2%")
    m3.metric("عدد الفروع العاملة", "28 فرعاً", "نشط")