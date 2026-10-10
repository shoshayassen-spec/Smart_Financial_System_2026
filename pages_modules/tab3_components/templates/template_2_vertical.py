import streamlit as st
import pandas as pd
import plotly.express as px

TEMPLATE_TITLE = "⚖️ [قالب 2]: كشف الحساب المتقابل والتحليل الرأسي والتصنيفات (Vertical & Cost Classification)"

def render(exp_df, rev_df, total_revenue, show_math, **kwargs):
    total_expense = kwargs.get('total_expense', exp_df['amount'].sum() if not exp_df.empty else 0.0)
    net_profit = kwargs.get('net_profit', total_revenue - total_expense)

    st.markdown("### ⚖️ كشف الحساب المتقابل والتحليل الرأسي الشامل")
    
    # --- 1. قسم كشف الحساب المتقابل (إيرادات مقابل مصروفات) ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🟢 كشف الإيرادات والوزن النسبي")
        if not rev_df.empty:
            rev_df_display = rev_df.copy()
            rev_df_display['الوزن النسبي %'] = (rev_df_display['amount'] / total_revenue * 100).round(1) if total_revenue > 0 else 0
            rev_df_display.rename(columns={'account_name': 'اسم الحساب', 'amount': 'المبلغ (ريال)'}, inplace=True)
            st.dataframe(rev_df_display[['اسم الحساب', 'المبلغ (ريال)', 'الوزن النسبي %']], use_container_width=True)
        else:
            st.info("لا توجد بيانات إيرادات مسجلة.")

    with col2:
        st.markdown("#### 🔴 كشف المصروفات والوزن النسبي")
        if not exp_df.empty:
            exp_df_display = exp_df.copy()
            exp_df_display['الوزن النسبي %'] = (exp_df_display['amount'] / total_revenue * 100).round(1) if total_revenue > 0 else 0
            exp_df_display.rename(columns={
                'account_name': 'اسم الحساب', 
                'amount': 'المبلغ (ريال)',
                'تصنيف_الميزانية': 'التصنيف المحاسبي',
                'طبيعة_التكلفة': 'طبيعة التكلفة'
            }, inplace=True)
            st.dataframe(exp_df_display[['اسم الحساب', 'المبلغ (ريال)', 'التصنيف المحاسبي', 'طبيعة التكلفة', 'الوزن النسبي %']], use_container_width=True)
        else:
            st.info("لا توجد بيانات مصروفات مسجلة.")

    st.markdown("---")

    # --- 2. جدول أكثر المصروفات استهلاكاً للأرباح ---
    st.markdown("### 🚨 أكثر المصروفات استهلاكاً لأرباح الفرع")
    if not exp_df.empty:
        top_exp = exp_df.copy()
        top_exp = top_exp.sort_values(by='amount', ascending=False)
        
        top_exp['النسبة من الإيراد %'] = (top_exp['amount'] / total_revenue * 100).round(1) if total_revenue > 0 else 0
        top_exp['النسبة من إجمالي المصروفات %'] = (top_exp['amount'] / total_expense * 100).round(1) if total_expense > 0 else 0
        
        top_exp.rename(columns={
            'account_name': 'اسم بند المصروف',
            'amount': 'القيمة (ريال)',
            'تصنيف_الميزانية': 'الفئة',
            'طبيعة_التكلفة': 'نوع التكلفة'
        }, inplace=True)

        # عرض أثقل 7 بنود استهلاكاً للأرباح
        st.dataframe(
            top_exp[['اسم بند المصروف', 'القيمة (ريال)', 'النسبة من الإيراد %', 'النسبة من إجمالي المصروفات %', 'الفئة', 'نوع التكلفة']].head(7),
            use_container_width=True
        )

        # --- 3. مخطط بياني تفاعلي لتوزيع المصروفات الأكثر استهلاكاً ---
        col_chart1, col_chart2 = st.columns([1.8, 1.2])
        
        with col_chart1:
            fig_bar = px.bar(
                top_exp.head(7),
                x='اسم بند المصروف',
                y='القيمة (ريال)',
                color='القيمة (ريال)',
                title="📊 توزيع أعلى 7 بنود مصروفات استهلاكاً للسيولة والأرباح",
                color_continuous_scale='Reds',
                labels={'اسم بند المصروف': 'بند المصروف', 'القيمة (ريال)': 'المبلغ بالريال'}
            )
            fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"))
            st.plotly_chart(fig_bar, use_container_width=True)

        with col_chart2:
            fig_pie = px.pie(
                top_exp.head(5),
                names='اسم بند المصروف',
                values='القيمة (ريال)',
                title="🍩 نسبة استهلاك البنود الـ5 الكبرى",
                hole=0.4
            )
            fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#FFFFFF"))
            st.plotly_chart(fig_pie, use_container_width=True)

    if show_math:
        st.markdown("<div class='math-review-section'>", unsafe_allow_html=True)
        st.info("📐 **معادلات التحليل الرأسي والمصروفات:**\n"
                "- **الوزن النسبي للبند من الإيراد %** = (مبلغ البند ÷ إجمالي الإيرادات) × 100\n"
                "- **نسبة استهلاك المصروف %** = (مبلغ المصروف ÷ إجمالي المصروفات) × 100")
        st.markdown("</div>", unsafe_allow_html=True)