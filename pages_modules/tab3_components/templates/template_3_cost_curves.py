import streamlit as st

TEMPLATE_TITLE = "📈 [قالب 3]: تحليلات منحنيات وتمركز التكاليف والاتجاهات (Cost Curves & Trend Analysis)"

def render(exp_df, total_expense, show_math, **kwargs):
    st.markdown("### 📈 تحليلات تمركز التكاليف والاتجاهات")
    if not exp_df.empty:
        cost_group = exp_df.groupby('تصنيف_الميزانية')['amount'].sum().reset_index()
        cost_group['النسبة %'] = (cost_group['amount'] / total_expense * 100).round(1) if total_expense > 0 else 0
        st.write("📊 **توزيع المصروفات حسب الفئة:**")
        st.dataframe(cost_group, use_container_width=True)

    if show_math:
        st.info("📐 **معادلة التمركز:** نسبة تمركز الفئة % = (إجمالي الفئة ÷ إجمالي المصروفات) × 100")