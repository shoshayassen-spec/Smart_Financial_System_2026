import streamlit as st

TEMPLATE_TITLE = "⚖️ [قالب 2]: كشف الحساب المتقابل والتحليل الرأسي والتصنيفات (Vertical & Cost Classification)"

def render(exp_df, rev_df, total_revenue, show_math, **kwargs):
    st.markdown("### ⚖️ كشف الحساب المتقابل والتحليل الرأسي")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🟢 كشف الإيرادات")
        if not rev_df.empty:
            rev_df_display = rev_df.copy()
            rev_df_display['الوزن النسبي %'] = (rev_df_display['amount'] / total_revenue * 100).round(1) if total_revenue > 0 else 0
            st.dataframe(rev_df_display[['account_name', 'amount', 'الوزن النسبي %']], use_container_width=True)
    
    with col2:
        st.markdown("#### 🔴 كشف المصروفات والوزن النسبي")
        if not exp_df.empty:
            exp_df_display = exp_df.copy()
            exp_df_display['الوزن النسبي %'] = (exp_df_display['amount'] / total_revenue * 100).round(1) if total_revenue > 0 else 0
            st.dataframe(exp_df_display[['account_name', 'amount', 'تصنيف_الميزانية', 'طبيعة_التكلفة', 'الوزن النسبي %']], use_container_width=True)

    if show_math:
        st.info("📐 **معادلة التحليل الرأسي:** الوزن النسبي للبند % = (مبلغ البند ÷ إجمالي الإيرادات) × 100")