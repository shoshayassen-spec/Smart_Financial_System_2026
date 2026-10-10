import streamlit as st

TEMPLATE_TITLE = "🌐 [قالب 1]: لوحة القيادة التنفيذية الشاملة (Master Executive Dashboard)"

def render(total_revenue, b_target, exp_df, rev_df, total_expense, net_profit, profit_margin, cost_per_sales_riyal, return_per_expense_riyal, show_math, **kwargs):
    st.markdown("### 🌐 لوحة القيادة التنفيذية الشاملة")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 18px;">
                <h4 style="color: #38BDF8; margin: 0 0 10px 0;">📊 مؤشرات الأداء والربحية</h4>
                <p><b>إجمالي الإيرادات:</b> {total_revenue:,.2f} ريال</p>
                <p><b>إجمالي المصروفات:</b> {total_expense:,.2f} ريال</p>
                <p><b>صافي الربح / الخسارة:</b> {net_profit:,.2f} ريال (هامش: {profit_margin:.1f}%)</p>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 18px;">
                <h4 style="color: #10B981; margin: 0 0 10px 0;">🎯 كفاءة الريال والمستهدف</h4>
                <p><b>تكلفة الريال المباع:</b> {cost_per_sales_riyal:.2f} ريال</p>
                <p><b>العائد لكل ريال مصروف:</b> {return_per_expense_riyal:.2f} ريال</p>
                <p><b>المستهدف الشهري:</b> {b_target:,.2f} ريال</p>
            </div>
        """, unsafe_allow_html=True)

    if show_math:
        st.info("📐 **معادلة القالب:** صافي الربح = الإيرادات - المصروفات | العائد لكل ريال = الإيرادات ÷ المصروفات")