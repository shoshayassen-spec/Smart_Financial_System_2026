import streamlit as st
import plotly.graph_objects as go
import pandas as pd

TEMPLATE_TITLE = "📊 [قالب 7]: المقارنة المرجعية المعيارية والربحية المتقدمة (Peer Benchmarking & Advanced Profitability)"

def render(target_achieved, profit_margin, opex_ratio, return_per_expense_riyal, show_math, **kwargs):
    # 1. عنوان القالب بتصميم الكرت الزجاجي الفاخر 3D
    st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
                    border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 18px; padding: 20px; margin-bottom: 25px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);">
            <h2 style="color: #10B981; font-weight: 800; margin: 0; font-size: 22px;">📊 منصة المقارنة المرجعية المعيارية (Peer Benchmarking Platform)</h2>
            <p style="color: #94A3B8; font-size: 13px; margin-top: 6px; margin-bottom: 0;">قياس ومفاضلة أداء الفرع مقابل المستهدفات المعيارية المعتمدة للشركة</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. كروت المؤشرات المرجعية (3D Metrics Cards)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        target_color = "#10B981" if target_achieved >= 100.0 else ("#F59E0B" if target_achieved >= 80.0 else "#EF4444")
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid {target_color}; border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: {target_color}; font-size: 12px; font-weight: 700;">🎯 تحقيق المستهدف</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{target_achieved:.1f}%</div>
                <div style="color: {target_color}; font-size: 11px;">المعيار المطلوب: 100.0%</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        margin_color = "#10B981" if profit_margin >= 20.0 else ("#F59E0B" if profit_margin >= 10.0 else "#EF4444")
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid {margin_color}; border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: {margin_color}; font-size: 12px; font-weight: 700;">📈 هامش صافي الربح</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{profit_margin:.1f}%</div>
                <div style="color: {margin_color}; font-size: 11px;">المعيار المطلوب: 20.0%</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        opex_color = "#10B981" if opex_ratio <= 40.0 else "#EF4444"
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid {opex_color}; border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: {opex_color}; font-size: 12px; font-weight: 700;">📉 نسبة المصروفات للإيراد</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{opex_ratio:.1f}%</div>
                <div style="color: {opex_color}; font-size: 11px;">المعيار المستهدف: ≤ 40.0%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        return_color = "#10B981" if return_per_expense_riyal >= 1.25 else "#F59E0B"
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
                        border: 1px solid {return_color}; border-radius: 14px; padding: 16px; text-align: center;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.3);">
                <div style="color: {return_color}; font-size: 12px; font-weight: 700;">💵 عائد الريال المصروف</div>
                <div style="color: #F8FAFC; font-size: 20px; font-weight: 800; margin: 8px 0;">{return_per_expense_riyal:.2f} <span style="font-size:12px;">ريال</span></div>
                <div style="color: {return_color}; font-size: 11px;">المعيار المطلوب: ≥ 1.25 ريال</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. الرسم البياني الراداري المقارن (Radar Benchmarking Chart)
    categories = ['تحقيق المستهدف', 'هامش الربح', 'كفاءة المصروفات', 'عائد الريال']
    
    # تحويل القيم لنسب مئوية معيارية على مقياس 100%
    branch_scores = [
        min(target_achieved, 150.0),
        min((profit_margin / 20.0) * 100.0, 150.0),
        min(((100.0 - opex_ratio) / 60.0) * 100.0, 150.0),
        min((return_per_expense_riyal / 1.25) * 100.0, 150.0)
    ]
    benchmark_scores = [100.0, 100.0, 100.0, 100.0]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=branch_scores,
        theta=categories,
        fill='toself',
        name='أداء الفرع الحالي',
        line_color='#10B981',
        fillcolor='rgba(16, 185, 129, 0.25)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=benchmark_scores,
        theta=categories,
        fill='toself',
        name='المعيار المستهدف (Benchmark)',
        line_color='#38BDF8',
        fillcolor='rgba(56, 189, 248, 0.15)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 150], gridcolor="rgba(255, 255, 255, 0.1)"),
            angularaxis=dict(gridcolor="rgba(255, 255, 255, 0.1)", font=dict(color="#CBD5E1"))
        ),
        title=dict(text="<b>🕸️ التقييم الراداري الشامل للفرع مقابل المستهدف المعياري</b>", font=dict(size=16, color="#10B981")),
        paper_bgcolor="rgba(15, 23, 42, 0.8)",
        plot_bgcolor="rgba(15, 23, 42, 0.8)",
        font=dict(color="#CBD5E1"),
        showlegend=True,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
    )

    st.plotly_chart(fig, use_container_width=True)

    # 4. جدول التقييم والتحليل المعياري
    st.markdown("#### 📋 جدول المفاضلة والمطابقة المعيارية")
    
    table_data = {
        "مؤشر الأداء": ["نسبة تحقيق المستهدف", "هامش صافي الربح", "نسبة المصروفات للإيراد", "عائد الريال المصروف"],
        "أداء الفرع": [f"{target_achieved:.1f}%", f"{profit_margin:.1f}%", f"{opex_ratio:.1f}%", f"{return_per_expense_riyal:.2f} ريال"],
        "المعيار المعتمد": ["100.0%", "20.0%", "40.0%", "1.25 ريال"],
        "التقييم": [
            "🟢 متفوق" if target_achieved >= 100.0 else "🔴 يحتاج تحسين",
            "🟢 مطابق" if profit_margin >= 20.0 else "🔴 منخفض",
            "🟢 ممتاز" if opex_ratio <= 40.0 else "⚠️ مرتفع",
            "🟢 ممتاز" if return_per_expense_riyal >= 1.25 else "⚠️ غير كافٍ"
        ]
    }
    df_bench = pd.DataFrame(table_data)
    st.dataframe(df_bench, use_container_width=True, hide_index=True)

    # 5. الشرح والمعادلات
    if show_math:
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.8); border-right: 4px solid #10B981; border-radius: 8px; padding: 15px; margin-top: 15px;">
                <h4 style="color: #10B981; margin-top:0;">📐 منهجية المقارنة المعيارية:</h4>
                <ul style="color: #CBD5E1; font-size: 13px; line-height: 1.8; margin-bottom: 0;">
                    <li><b>عائد الريال المصروف:</b> إجمالي الإيرادات ÷ إجمالي المصروفات التشغيلية.</li>
                    <li><b>المعيار المرجعي (Benchmarking):</b> مقارنة مؤشرات الفرع بأداء أفضل الفروع أو المستهدفات المعتمدة من مجلس الإدارة.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)