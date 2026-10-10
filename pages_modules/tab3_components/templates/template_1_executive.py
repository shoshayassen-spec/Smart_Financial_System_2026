import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

TEMPLATE_TITLE = "🌐 [قالب 1]: لوحة القيادة التنفيذية الشاملة (Master Executive Dashboard)"

def render(total_revenue, b_target, exp_df, rev_df, total_expense, net_profit, profit_margin, cost_per_sales_riyal, return_per_expense_riyal, show_math, **kwargs):
    # 1. استخراج المتغيرات المحاسبية بآمان لتفادي خطأ NameError
    cogs_amount = kwargs.get('cogs_amount', total_expense * 0.45)
    opex_amount = kwargs.get('opex_amount', total_expense - cogs_amount)
    cogs_ratio = kwargs.get('cogs_ratio', (cogs_amount / total_revenue * 100) if total_revenue > 0 else 0.0)
    opex_ratio = kwargs.get('opex_ratio', (opex_amount / total_revenue * 100) if total_revenue > 0 else 0.0)
    target_achieved = kwargs.get('target_achieved', (total_revenue / b_target * 100) if b_target > 0 else 0.0)

    st.markdown("### 🌐 لوحة القيادة التنفيذية الشاملة")
    
    # --- 1. البطاقات التنفيذية عالية التباين ---
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 12px; padding: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <h4 style="color: #38BDF8; margin: 0 0 12px 0;">📊 مؤشرات الأداء والربحية</h4>
                <p style="margin-bottom: 6px;"><b>إجمالي الإيرادات:</b> <span style="color:#4ADE80; font-weight:bold;">{total_revenue:,.2f} ريال</span></p>
                <p style="margin-bottom: 6px;"><b>تكلفة المبيعات (COGS):</b> <span style="color:#FBBF24; font-weight:bold;">{cogs_amount:,.2f} ريال</span> (نسبة: {cogs_ratio:.1f}%)</p>
                <p style="margin-bottom: 6px;"><b>المصروفات التشغيلية (OpEx):</b> <span style="color:#F87171; font-weight:bold;">{opex_amount:,.2f} ريال</span> (نسبة: {opex_ratio:.1f}%)</p>
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

    # --- 2. المؤشرات الأربعة (Gauge Charts) متناسقة الألوان وعالية التباين ---
    st.markdown("#### ⏱️ شاشات القيادة السريعة ومؤشرات النسب الهيكلية")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)

    # مؤشر 1: نسبة تحقيق المستهدف
    with g_col1:
        fig_g1 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = target_achieved,
            title = {'text': "🎯 نسبة المستهدف", 'font': {'size': 14, 'color': '#38BDF8'}},
            number = {'suffix': "%", 'font': {'size': 20, 'color': '#FFFFFF'}},
            gauge = {
                'axis': {'range': [0, 150]},
                'bar': {'color': "#3B82F6"},
                'steps': [
                    {'range': [0, 70], 'color': "#7F1D1D"},
                    {'range': [70, 100], 'color': "#78350F"},
                    {'range': [100, 150], 'color': "#064E3B"}
                ]
            }
        ))
        fig_g1.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"), height=180, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_g1, use_container_width=True)

    # مؤشر 2: هامش صافي الربح
    with g_col2:
        fig_g2 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = profit_margin,
            title = {'text': "📈 هامش الربح", 'font': {'size': 14, 'color': '#38BDF8'}},
            number = {'suffix': "%", 'font': {'size': 20, 'color': '#FFFFFF'}},
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
        fig_g2.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"), height=180, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_g2, use_container_width=True)

    # مؤشر 3: نسبة تكلفة المبيعات COGS
    with g_col3:
        fig_g3 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = cogs_ratio,
            title = {'text': "📦 نسبة COGS", 'font': {'size': 14, 'color': '#38BDF8'}},
            number = {'suffix': "%", 'font': {'size': 20, 'color': '#FFFFFF'}},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#FBBF24"},
                'steps': [
                    {'range': [0, 45], 'color': "#065F46"},
                    {'range': [45, 65], 'color': "#854D0E"},
                    {'range': [65, 100], 'color': "#991B1B"}
                ]
            }
        ))
        fig_g3.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"), height=180, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_g3, use_container_width=True)

    # مؤشر 4: نسبة المصروفات التشغيلية OpEx
    with g_col4:
        fig_g4 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = opex_ratio,
            title = {'text': "🏢 نسبة OpEx", 'font': {'size': 14, 'color': '#38BDF8'}},
            number = {'suffix': "%", 'font': {'size': 20, 'color': '#FFFFFF'}},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "#F87171"},
                'steps': [
                    {'range': [0, 30], 'color': "#065F46"},
                    {'range': [30, 50], 'color': "#854D0E"},
                    {'range': [50, 100], 'color': "#991B1B"}
                ]
            }
        ))
        fig_g4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"), height=180, margin=dict(l=10, r=10, t=30, b=10))
        st.plotly_chart(fig_g4, use_container_width=True)

    st.markdown("---")

    # --- 3. الرسم البياني المقارن لهيكل المال + جدول التجميع المحاسبي ---
    chart_col, table_col = st.columns([1.2, 1.8])

    with chart_col:
        st.markdown("#### 📊 مقارنة الهيكل المالي")
        summary_data = pd.DataFrame({
            'البند': ['الإيرادات', 'COGS', 'OpEx', 'صافي الربح'],
            'المبلغ (ريال)': [total_revenue, cogs_amount, opex_amount, net_profit]
        })
        
        fig_bar = px.bar(
            summary_data,
            x='البند',
            y='المبلغ (ريال)',
            color='البند',
            text_auto=',.0f',
            color_discrete_map={
                'الإيرادات': '#3B82F6',
                'COGS': '#F59E0B',
                'OpEx': '#EF4444',
                'صافي الربح': '#10B981'
            }
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", 
            plot_bgcolor="rgba(0,0,0,0)", 
            font=dict(color="#FFFFFF"), 
            showlegend=False,
            height=320
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with table_col:
        st.markdown("#### 📋 تجميع المصروفات حسب التصنيفات القياسية")
        if not exp_df.empty and 'تصنيف_الميزانية' in exp_df.columns:
            grouped_exp = exp_df.groupby('تصنيف_الميزانية')['amount'].sum().reset_index()
            grouped_exp['النسبة من الإيراد %'] = (grouped_exp['amount'] / total_revenue * 100).round(1) if total_revenue > 0 else 0.0
            grouped_exp['النسبة من إجمالي المصروف %'] = (grouped_exp['amount'] / total_expense * 100).round(1) if total_expense > 0 else 0.0
            grouped_exp.rename(columns={'تصنيف_الميزانية': 'التصنيف المحاسبي', 'amount': 'الإجمالي (ريال)'}, inplace=True)
            
            st.dataframe(
                grouped_exp[['التصنيف المحاسبي', 'الإجمالي (ريال)', 'النسبة من الإيراد %', 'النسبة من إجمالي المصروف %']],
                use_container_width=True,
                height=280
            )
        else:
            st.info("لا توجد بيانات مصروفات مصنفة للعرض.")

    if show_math:
        st.markdown("<div class='math-review-section'>", unsafe_allow_html=True)
        st.info("📐 **معادلات لوحة القيادة التنفيذية:**\n"
                "- **صافي الربح** = الإيرادات - (تكلفة المبيعات COGS + المصروفات التشغيلية OpEx)\n"
                "- **نسبة COGS %** = (تكلفة المبيعات ÷ الإيراد) × 100\n"
                "- **نسبة OpEx %** = (المصروفات التشغيلية ÷ الإيراد) × 100\n"
                "- **العائد لكل ريال** = الإيرادات ÷ إجمالي المصروفات")
        st.markdown("</div>", unsafe_allow_html=True)