import streamlit as st

TEMPLATE_TITLE = "📊 [قالب 7]: المقارنة المرجعية المعيارية والربحية المتقدمة (Peer Benchmarking & Advanced Profitability)"

def render(target_achieved, profit_margin, opex_ratio, return_per_expense_riyal, show_math, **kwargs):
    st.markdown("### 📊 المقارنة المرجعية المعيارية")
    
    st.write("🎯 **مؤشرات الأداء المقارنة مقارنة بالمعايير:**")
    data = {
        "المؤشر M": ["نسبة تحقيق المستهدف", "هامش صافي الربح", "نسبة المصروفات للإيراد", "عائد الريال المصروف"],
        "أداء الفرع الحالي": [f"{target_achieved:.1f}%", f"{profit_margin:.1f}%", f"{opex_ratio:.1f}%", f"{return_per_expense_riyal:.2f} ريال"],
        "المعيار المستهدف": ["100%", "20%", "40%", "1.25 ريال"]
    }
    st.table(data)

    if show_math:
        st.info("📐 **المقارنة المعيارية:** تقارن أداء الفرع الحالي بالمعايير التشغيلية المعتمدة للشركة.")