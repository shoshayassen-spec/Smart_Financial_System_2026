import streamlit as st
import pandas as pd

TEMPLATE_TITLE = "🧠 [قالب 4]: تشخيص الذكاء الاصطناعي وجودة الأرباح والتنبؤ (AI Diagnostic & Earnings Quality)"

def render(net_profit, profit_margin, opex_ratio, cogs_ratio, show_math, **kwargs):
    total_revenue = kwargs.get('total_revenue', 0.0)
    total_expense = kwargs.get('total_expense', 0.0)
    b_target = kwargs.get('b_target', 0.0)
    target_achieved = kwargs.get('target_achieved', 0.0)
    bep_val = kwargs.get('bep_val', 0.0)
    bep_coverage = kwargs.get('bep_coverage', 0.0)

    st.markdown("### 🧠 تقرير التشخيص المالي الذكي وتوصيات الخبير")

    # تحديد الحالة الصحية العامة
    if profit_margin >= 20 and target_achieved >= 90:
        health_status = "ممتازة جداً 🟢"
        health_class = "ai-box-success"
        score = 95
    elif profit_margin > 5 and target_achieved >= 70:
        health_status = "متوازنة ومستقرة 🟡"
        health_class = "ai-box-info"
        score = 75
    else:
        health_status = "حرجة وتتطلب تدخلاً عاجلاً 🔴"
        health_class = "ai-box-error"
        score = 40

    # مؤشر درجة جودة الأرباح
    st.progress(score / 100)
    st.markdown(f"<p style='text-align: center; font-weight: bold;'>مؤشر جودة الأرباح والصحة المالية للفرع: <span style='font-size: 18px;'>{score} / 100</span> ({health_status})</p>", unsafe_allow_html=True)
    st.markdown("---")

    # --- 1. نقاط القوة المالية ---
    strengths = []
    if profit_margin > 15:
        strengths.append(f"هامش صافي ربح مرتفع بـ <b>{profit_margin:.1f}%</b> يتجاوز المستهدفات المعيارية للقطاع.")
    if cogs_ratio < 50:
        strengths.append(f"كفاءة عالية في ضبط تكلفة المبيعات (COGS) عند <b>{cogs_ratio:.1f}%</b> من إجمالي الإيرادات.")
    if target_achieved >= 100:
        strengths.append(f"تجاوز مستهدف المبيعات المحدد بنسبة تحقيق بلغت <b>{target_achieved:.1f}%</b>.")
    if bep_coverage > 130:
        strengths.append(f"تغطية مريحة لنقطة التعادل بنسبة <b>{bep_coverage:.1f}%</b> مما يقلل مخاطر التشغيل.")

    if not strengths:
        strengths.append("المحافظة على استمرارية العمليات التشغيلية وتغطية التكاليف الأساسية.")

    st.markdown(f"""
        <div class='ai-box-success'>
            <h4>🟢 1. أبرز نقاط القوة والأداء المتميز:</h4>
            <ul>
                {"".join([f"<li>{s}</li>" for s in strengths])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. نقاط الضعف والمخاطر التشغيلية ---
    weaknesses = []
    if opex_ratio > 40:
        weaknesses.append(f"ارتفاع نسبة المصروفات التشغيلية (OpEx) لتصل إلى <b>{opex_ratio:.1f}%</b> من الإيراد، مما يضغط على الأرباح.")
    if cogs_ratio > 60:
        weaknesses.append(f"ارتفاع تكلفة البضاعة المباعة (COGS) لـ <b>{cogs_ratio:.1f}%</b>، يرجى مراجعة أسعار الموردين والهدر.")
    if target_achieved < 80:
        weaknesses.append(f"عجز في تحقيق مستهدف المبيعات بقيمة متبقية قدرها <b>{abs(total_revenue - b_target):,.2f} ريال</b>.")
    if profit_margin <= 0:
        weaknesses.append("الفرع يسجل خسائر تشغيلية تتطلب إعادة هيكلة فورية للتكاليف.")

    if not weaknesses:
        weaknesses.append("لا توجد مخاطر تشغيلية جوهرية بارزة في الفترة الحالية.")

    st.markdown(f"""
        <div class='ai-box-warning'>
            <h4>🔴 2. نقاط الضعف والمخاطر المرصودة:</h4>
            <ul>
                {"".join([f"<li>{w}</li>" for w in weaknesses])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # --- 3. مبادرات ورؤى الذكاء الاصطناعي المقترحة ---
    st.markdown(f"""
        <div class='ai-box-info'>
            <h4>💡 3. التوصيات والمبادرات الإستراتيجية المقترحة للقيادة:</h4>
            <ol>
                <li><b>تحسين جودة الهامش:</b> {"العمل على إعادة تفاوض عقود التوريد لخفض COGS بـ 3-5%." if cogs_ratio > 50 else "التركيز على تنشيط المبيعات ذات الهامش الربحي المرتفع."}</li>
                <li><b>ترشيد المصروفات الثابتة:</b> {"مراجعة بنود الإيجار والرواتب واستغلال الأصول الثابتة بكفاءة أكبر." if opex_ratio > 35 else "ضبط المصروفات المتغيرة ومراقبة الإنفاق الدائم."}</li>
                <li><b>خطة النمو والهدف:</b> تكثيف الحملات التسويقية الموجهة لتغطية الفجوة عن المستهدف البالغة <b>{max(0, b_target - total_revenue):,.2f} ريال</b>.</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

    if show_math:
        st.markdown("<div class='math-review-section'>", unsafe_allow_html=True)
        st.info("📐 **معايير خوارزمية التشخيص:**\n"
                "- **أداء ممتاز:** هامش ربح > 20% + تحقيق الهدف > 90%.\n"
                "- **أداء متوازن:** هامش ربح بين 5% - 20%.\n"
                "- **أداء حرج:** هامش ربح < 5% أو وجود خسائر.")
        st.markdown("</div>", unsafe_allow_html=True)