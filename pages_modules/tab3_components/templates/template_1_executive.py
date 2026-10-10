import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

TEMPLATE_TITLE = "🌐 [قالب 1]: لوحة القيادة التنفيذية الشاملة (Master Executive Dashboard)"

def render(total_revenue, b_target, exp_df, rev_df, total_expense, net_profit, profit_margin, cost_per_sales_riyal, return_per_expense_riyal, show_math, **kwargs):
    cogs_amount = kwargs.get('cogs_amount', total_expense * 0.45)
    opex_amount = kwargs.get('opex_amount', total_expense - cogs_amount)
    target_achieved = kwargs.get('target_achieved', (total_revenue / b_target * 100) if b_target > 0 else 0.0)

    st.markdown("### 🌐 لوحة القيادة التنفيذية الشاملة")
    
    # --- 1. البطاقات التنفيذية عالية التباين ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 12px; padding: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <h4 style="color: #38BDF8; margin: 0 0 12px 0;">📊 مؤشرات الأداء والربحية</h4>
                <p style="margin-bottom: 6px;"><b>إجمالي الإيرادات:</b> <span style="color:#4ADE80; font-weight:bold;">{total_revenue:,.2f} ريال</span></p>
                <p style="margin-bottom: 6px;"><b>تكلفة المبيعات (COGS):</b> <span style="color:#FBBF24; font-weight:bold;">{cogs_amount:,.2f} ريال</span></p>
                <p style="margin-bottom: 6px;"><b>المصروفات التشغيلية (OpEx):</b> <span style="color:#F87171; font-weight:bold;">{opex_amount:,.2f} ريال</span></p>
                <p style="margin-bottom: 0px;"><b>صافي الربح / الخسارة:</b> <span style="color:#FFFFFF; font-weight:bold; font-size:16px;">{net_profit:,.2f} ريال</span> (هامش: {profit_margin:.1f}%)</p>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <h4 style="color: #10B981; margin: 0 0 12px 0;">🎯 كفاءة الريال والمستهدف</h4>
                <p style="margin-bottom: 6px;"><b>تكلفة الريال المباع:</b> <span style="color:#38BDF8; font-weight:bold;">{cost_per_sales_riyal:.2f} ريال</span></p>
                <p style="margin-bottom: 6px;"><b>العائد لكل ريال مصروف:</b> <span style="color:#4ADE80; font-weight:bold;">{return_per_expense_riyal:.2f} ريال</span></p>
                <p style="margin-bottom: 6px;"><b>المستهدف الشهري:</b> <span style="color:#FFFFFF; font-weight:bold;">{b_target:,.2f} ريال</span></p>
                <p style="margin-bottom: 0px;"><b>نسبة تحقيق الهدف:</b> <span style="color:#FBBF24; font-weight:bold;">{target_achieved:.1f}%</span></p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 2. مؤشرات السرعة (Gauge Charts) والمخططات الحية ---
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        fig_gauge1 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = target_achieved,
            title = {'text': "🎯 نسبة تحقيق المستهدف (%)"},
            number = {'suffix': "%"},
            gauge = {
                'axis': {'range': [None, 150]},
                'bar': {'color': "#3B82F6"},
                'steps': [
                    {'range': [0, 70], 'color': "#7F1D1D"},
                    {'range': [70, 100], 'color': "#78350F"},
                    {'range': [100, 150], 'color': "#064E3B"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 100
                }
            }
        ))
        fig_gauge1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"), height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge1, use_container_width=True)

    with col_g2:
        fig_gauge2 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = profit_margin,
            title = {'text': "📈 هامش صافي الربح (%)"},
            number = {'suffix': "%"},
            gauge = {
                'axis': {'range': [-20, 50]},
                'bar': {'color': "#10B981" if profit_margin >= 0 else "#EF4444"},
                'steps': [
                    {'range': [-20, 0], 'color': "#991B1B"},
                    {'range': [0, 15], 'color': "#854D0E"},
                    {'range': [15, 50], 'color': "#065F46"}
                ]
            }
        ))
        fig_gauge2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"), height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge2, use_container_width=True)

    # --- 3. الرسم البياني المقارن لهيكل المال ---
    st.markdown("#### 📊 المقارنة الهيكلية للإيرادات والتكاليف والأرباح")
    summary_data = pd.DataFrame({
        'البند': ['إجمالي الإيرادات', 'تكلفة المبيعات (COGS)', 'المصروفات التشغيلية (OpEx)', 'صافي الربح'],
        'المبلغ (ريال)': [total_revenue, cogs_amount, opex_amount, net_profit]
    })
    
    fig_bar = px.bar(
        summary_data,
        x='البند',
        y='المبلغ (ريال)',
        color='البند',
        text_auto=',.2f',
        color_discrete_map={
            'إجمالي الإيرادات': '#3B82F6',
            'تكلفة المبيعات (COGS)': '#F59E0B',
            'المصروفات التشغيلية (OpEx)': '#EF4444',
            'صافي الربح': '#10B981'
        }
    )
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    if show_math:
        st.markdown("<div class='math-review-section'>", unsafe_allow_html=True)
        st.info("📐 **معادلات لوحة القيادة التنفيذية:**\n"
                "- **صافي الربح** = الإيرادات - (تكلفة المبيعات + المصروفات التشغيلية)\n"
                "- **العائد لكل ريال** = الإيرادات ÷ إجمالي المصروفات\n"
                "- **نسبة تحقيق الهدف** = (الإيراد الفعلي ÷ المستهدف) × 100")
        st.markdown("</div>", unsafe_allow_html=True)