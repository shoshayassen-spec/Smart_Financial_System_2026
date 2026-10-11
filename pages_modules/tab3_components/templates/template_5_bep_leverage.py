import streamlit as st
import plotly.graph_objects as go
import numpy as np

TEMPLATE_TITLE = "💎 [قالب 5]: منصة تحليل نقطة التعادل والرفع التشغيلي (Bloomberg BEP & Leverage)"

def render(fixed_costs, variable_costs, contribution_margin, contribution_margin_ratio, bep_val, bep_coverage, dol, show_math, **kwargs):
    # 1. عنوان القالب بتصميم الكرت الزجاجي الفاخر 3D
    st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
                    border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 18px; padding: 20px; margin-bottom: 25px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);">
            <h2 style="color: #38BDF8; font-weight: 800; margin: 0; font-size: 22px;">💎 منصة تحليل نقطة التعادل والرفع التشغيلي (BEP & DOL Platform)</h2>
            <p style="color: #94A3B8; font-size: 13px; margin-top: 6px; margin-bottom: 0;">قياس مرونة الأرباح ومستوى المخاطر التشغيلية وهامش الأمان بالفروع</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. كروت المؤشرات المالية الرئيسية (3D Metrics Cards)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: #F87171; font-size: 12px; font-weight: 700;">📌 التكاليف الثابتة</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{fixed_costs:,.2f} <span style="font-size:12px;">ريال</span></div>
                <div style="color: #94A3B8; font-size: 11px;">التزام أعيان وتكاليف إدارية</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: #38BDF8; font-size: 12px; font-weight: 700;">🟢 هامش المساهمة</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{contribution_margin:,.2f} <span style="font-size:12px;">ريال</span></div>
                <div style="color: #38BDF8; font-size: 11px;">نسبة الهامش: {contribution_margin_ratio * 100:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        bep_color = "#10B981" if bep_coverage >= 100 else "#F59E0B"
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid {bep_color}; border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: {bep_color}; font-size: 12px; font-weight: 700;">⚖️ مبيعات التعادل (BEP)</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{bep_val:,.2f} <span style="font-size:12px;">ريال</span></div>
                <div style="color: {bep_color}; font-size: 11px;">تغطية التعادل: {bep_coverage:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        dol_status = "ارتفاع حساسية الأرباح" if dol > 3.0 else ("معتدل" if dol > 1.0 else "منخفض")
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid rgba(168, 85, 247, 0.35); border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: #C084FC; font-size: 12px; font-weight: 700;">⚡ الرفع التشغيلي (DOL)</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{dol:.2f}x</div>
                <div style="color: #C084FC; font-size: 11px;">{dol_status}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. الرسم البياني التفاعلي 3D لمنطقة الأرباح والخسائر ونقطة التعادل
    max_sales = max(bep_val * 2.0, (fixed_costs + variable_costs) * 1.5, 100000.0)
    sales_range = np.linspace(0, max_sales, 100)
    var_cost_ratio = 1.0 - contribution_margin_ratio if contribution_margin_ratio < 1.0 else 0.5
    total_costs_range = fixed_costs + (sales_range * var_cost_ratio)

    fig = go.Figure()

    # خط إجمالي المبيعات
    fig.add_trace(go.Scatter(
        x=sales_range, y=sales_range,
        mode='lines', name='إجمالي الإيرادات',
        line=dict(color='#38BDF8', width=3)
    ))

    # خط التكاليف الكلية
    fig.add_trace(go.Scatter(
        x=sales_range, y=total_costs_range,
        mode='lines', name='التكاليف الكلية',
        line=dict(color='#EF4444', width=3, dash='dash')
    ))

    # خط التكاليف الثابتة
    fig.add_trace(go.Scatter(
        x=sales_range, y=[fixed_costs]*len(sales_range),
        mode='lines', name='التكاليف الثابتة',
        line=dict(color='#F59E0B', width=2, dash='dot')
    ))

    # نقطة التعادل BEP
    fig.add_trace(go.Scatter(
        x=[bep_val], y=[bep_val],
        mode='markers+text', name='نقطة التعادل (BEP)',
        text=[f'<b>BEP: {bep_val:,.0f} ريال</b>'],
        textposition="top center",
        marker=dict(color='#10B981', size=14, symbol='diamond')
    ))

    fig.update_layout(
        title=dict(text="<b>📈 مخطط منطقة الأرباح والخسائر وتقاطع نقطة التعادل</b>", font=dict(size=16, color="#38BDF8")),
        xaxis=dict(title="حجم المبيعات / الإيرادات (ريال)", gridcolor="rgba(255, 255, 255, 0.08)"),
        yaxis=dict(title="المبالغ المالية (ريال)", gridcolor="rgba(255, 255, 255, 0.08)"),
        paper_bgcolor="rgba(15, 23, 42, 0.8)",
        plot_bgcolor="rgba(15, 23, 42, 0.8)",
        font=dict(color="#CBD5E1"),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 4. شرح المعادلات الرياضية والتشخيص المالي
    if show_math:
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.8); border-right: 4px solid #38BDF8; border-radius: 8px; padding: 15px; margin-top: 15px;">
                <h4 style="color: #38BDF8; margin-top:0;">📐 المعادلات المالية المعتمدة في التقييم:</h4>
                <ul style="color: #CBD5E1; font-size: 13px; line-height: 1.8; margin-bottom: 0;">
                    <li><b>هامش المساهمة (Contribution Margin):</b> الإيرادات - التكاليف المتغيرة</li>
                    <li><b>نسبة هامش المساهمة:</b> هامش المساهمة ÷ إجمالي الإيرادات</li>
                    <li><b>مبيعات نقطة التعادل (BEP Sales):</b> التكاليف الثابتة ÷ نسبة هامش المساهمة</li>
                    <li><b>درجة الرفع التشغيلي (DOL):</b> هامش المساهمة ÷ صافي الربح التشغيلي (EBIT) — <i>تقيس نسبة التغير في الأرباح عند تغير المبيعات بـ 1%</i></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)