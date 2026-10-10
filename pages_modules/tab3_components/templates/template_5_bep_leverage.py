import streamlit as st

TEMPLATE_TITLE = "💎 [قالب 5]: منصة تحليل نقطة التعادل والرفع التشغيلي (Bloomberg BEP & Leverage)"

def render(fixed_costs, variable_costs, contribution_margin, contribution_margin_ratio, bep_val, bep_coverage, dol, show_math, **kwargs):
    st.markdown("### 💎 تحليل نقطة التعادل والرفع التشغيلي")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("التكاليف الثابتة", f"{fixed_costs:,.2f} ريال")
        st.metric("التكاليف المتغيرة", f"{variable_costs:,.2f} ريال")
    with c2:
        st.metric("هامش المساهمة", f"{contribution_margin:,.2f} ريال")
        st.metric("نسبة هامش المساهمة", f"{contribution_margin_ratio*100:.1f}%")
    with c3:
        st.metric("مبيعات نقطة التعادل (BEP)", f"{bep_val:,.2f} ريال")
        st.metric("درجة الرفع التشغيلي (DOL)", f"{dol:.2f}x")

    if show_math:
        st.info("📐 **المعادلات:** نقطة التعادل = التكاليف الثابتة ÷ نسبة هامش المساهمة | DOL = هامش المساهمة ÷ صافي الربح التشغيلي")