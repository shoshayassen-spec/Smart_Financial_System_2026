import streamlit as st

TEMPLATE_TITLE = "🚀 [قالب 6]: كشف التدفقات النقدية والأداء التشغيلي (Cash Flow Matrix)"

def render(total_revenue, total_expense, net_profit, ebitda, ebitda_margin, show_math, **kwargs):
    st.markdown("### 🚀 كشف التدفقات النقدية والأداء التشغيلي (EBITDA)")
    
    st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 12px; padding: 18px;">
            <h4 style="color: #F59E0B; margin: 0 0 10px 0;">⚡ الأرباح قبل الفوائد والضرائب والإهلاك (EBITDA)</h4>
            <p><b>EBITDA التقديري:</b> {ebitda:,.2f} ريال</p>
            <p><b>هامش EBITDA %:</b> {ebitda_margin:.1f}%</p>
            <p><b>صافي التدفق التشغيلي:</b> {net_profit:,.2f} ريال</p>
        </div>
    """, unsafe_allow_html=True)

    if show_math:
        st.info("📐 **معادلة EBITDA:** صافي الربح + الإهلاك والإطفاء والفوائد")