import streamlit as st

TEMPLATE_TITLE = "🧠 [قالب 4]: تشخيص الذكاء الاصطناعي وجودة الأرباح والتنبؤ (AI Diagnostic & Earnings Quality)"

def render(net_profit, profit_margin, opex_ratio, cogs_ratio, show_math, **kwargs):
    st.markdown("### 🧠 تشخيص الذكاء الاصطناعي وجودة الأرباح")
    
    health_status = "ممتازة 🟢" if profit_margin > 20 else ("متوسطة 🟡" if profit_margin > 0 else "حرجة 🔴")
    st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.9); border-right: 5px solid #38BDF8; border-radius: 12px; padding: 18px;">
            <h4>🤖 التقييم التشخيصي للفرع: <span style="color:#38BDF8;">{health_status}</span></h4>
            <p>• <b>نسبة تكلفة المبيعات (COGS):</b> {cogs_ratio:.1f}%</p>
            <p>• <b>نسبة المصروفات التشغيلية (OPEX):</b> {opex_ratio:.1f}%</p>
            <p>• <b>توصية الذكاء الاصطناعي:</b> {"التركيز على خفض المصروفات الثابتة وتحسين هامش المبيعات." if profit_margin <= 0 else "الأداء المالي متوازن ويوصى بزيادة المبيعات."}</p>
        </div>
    """, unsafe_allow_html=True)

    if show_math:
        st.info("📐 **معيار الجودة:** هامش ربح أعلى من 20% يعتبر أداءً تشغيلياً ممتازاً.")