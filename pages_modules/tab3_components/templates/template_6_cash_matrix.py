import streamlit as st
import plotly.graph_objects as go

TEMPLATE_TITLE = "🚀 [قالب 6]: كشف التدفقات النقدية والأداء التشغيلي (Cash Flow Matrix)"

def render(total_revenue, total_expense, net_profit, ebitda, ebitda_margin, show_math, **kwargs):
    # 1. هيدر القالب بتصميم زجاجي 3D
    st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
                    border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 18px; padding: 20px; margin-bottom: 25px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);">
            <h2 style="color: #F59E0B; font-weight: 800; margin: 0; font-size: 22px;">🚀 مصفوفة التدفقات النقدية والأداء التشغيلي (EBITDA Matrix)</h2>
            <p style="color: #94A3B8; font-size: 13px; margin-top: 6px; margin-bottom: 0;">تتبع الأرباح قبل الفوائد والضرائب والإهلاك وقياس قدرة الفرع على توليد السيولة النقية</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. كروت المؤشرات المالية والأداء التشغيلي 3D
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: #38BDF8; font-size: 12px; font-weight: 700;">💰 إجمالي الإيرادات</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{total_revenue:,.2f} <span style="font-size:12px;">ريال</span></div>
                <div style="color: #94A3B8; font-size: 11px;">التدفق النقدي الداخل</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid rgba(245, 158, 11, 0.4); border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: #F59E0B; font-size: 12px; font-weight: 700;">⚡ أرباح EBITDA التقديرية</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{ebitda:,.2f} <span style="font-size:12px;">ريال</span></div>
                <div style="color: #F59E0B; font-size: 11px;">الأرباح الكاش قبل الإهلاك</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        margin_color = "#10B981" if ebitda_margin >= 15.0 else ("#F59E0B" if ebitda_margin >= 5.0 else "#EF4444")
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid {margin_color}; border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: {margin_color}; font-size: 12px; font-weight: 700;">📊 هامش EBITDA %</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{ebitda_margin:.1f}%</div>
                <div style="color: {margin_color}; font-size: 11px;">مؤشر قوة الربحية التشغيلية</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        net_color = "#10B981" if net_profit >= 0 else "#EF4444"
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid {net_color}; border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: {net_color}; font-size: 12px; font-weight: 700;">💵 صافي التدفق التشغيلي</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{net_profit:,.2f} <span style="font-size:12px;">ريال</span></div>
                <div style="color: {net_color}; font-size: 11px;">السيولة المتبقية النهائية</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. الرسم البياني لشجرة حركة النقدية (Cash Waterfall Visual)
    fig = go.Figure(go.Waterfall(
        name = "التدفق النقدي",
        orientation = "v",
        measure = ["relative", "relative", "total", "relative", "total"],
        x = ["إجمالي الإيرادات", "المصروفات التشغيلية", "EBITDA التقديري", "مخصصات الإهلاك والفوائد", "صافي النقد التشغيلي"],
        textposition = "outside",
        text = [f"+{total_revenue:,.0f}", f"-{total_expense:,.0f}", f"{ebitda:,.0f}", f"-{(ebitda - net_profit):,.0f}", f"{net_profit:,.0f}"],
        y = [total_revenue, -total_expense, 0, -(ebitda - net_profit), 0],
        connector = {"line":{"color":"rgba(255, 255, 255, 0.2)"}},
        decreasing = {"marker":{"color":"#EF4444"}},
        increasing = {"marker":{"color":"#10B981"}},
        totals = {"marker":{"color":"#F59E0B"}}
    ))

    fig.update_layout(
        title=dict(text="<b>🌊 شجرة تحليل التدفقات النقدية والربحية التشغيلية (Waterfall Flow)</b>", font=dict(size=16, color="#F59E0B")),
        paper_bgcolor="rgba(15, 23, 42, 0.8)",
        plot_bgcolor="rgba(15, 23, 42, 0.8)",
        font=dict(color="#CBD5E1"),
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(gridcolor="rgba(255, 255, 255, 0.08)")
    )

    st.plotly_chart(fig, use_container_width=True)

    # 4. الشرح والمعادلات
    if show_math:
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.8); border-right: 4px solid #F59E0B; border-radius: 8px; padding: 15px; margin-top: 15px;">
                <h4 style="color: #F59E0B; margin-top:0;">📐 المعادلة المالية لقالب السيولة التشغيلية:</h4>
                <ul style="color: #CBD5E1; font-size: 13px; line-height: 1.8; margin-bottom: 0;">
                    <li><b>أرباح EBITDA:</b> صافي الربح التشغيلي + مخصصات الإهلاك والإطفاء + الفوائد والضرائب.</li>
                    <li><b>هامش EBITDA %:</b> (أرباح EBITDA ÷ إجمالي الإيرادات) × 100 — <i>يعكس الكفاءة النقدية للنشاط الرئيسي دون التأثر بآليات التمويل أو الإهلاك.</i></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)