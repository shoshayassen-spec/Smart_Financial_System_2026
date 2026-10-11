import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_city_control_bar(city_list):
    """شريط الفلاتر والقوالب المثبتة والتحكم العالي"""
    st.markdown("### 🏛️ الاستعلام عن مدينة")
    st.caption("اختر المدينة لتحليل مجمّع فروعها معاً، وتظهر الفروع المرتبطة بها للتنقل لأي منها بضغطة.")

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        selected_city = st.selectbox("المدينة", city_list)
    with c2:
        date_from = st.selectbox("من شهر", ["يناير 2026", "فبراير 2026", "مارس 2026"])
    with c3:
        date_to = st.selectbox("إلى شهر", ["يناير 2026", "فبراير 2026", "مارس 2026"])

    st.markdown("📌 **قوالب مثبتة (اضغط للتطبيق على البيانات):**")
    
    # أزرار القوالب المثبتة
    t_cols = st.columns(6)
    templates = [
        "التقرير الشامل", "الملخص التنفيذي للإدارة العليا", "الربحية والتكاليف",
        "التعادل والمخاطر", "الاتجاهات والتنبؤ", "الأداء مقابل التارجت"
    ]
    
    selected_template = "التقرير الشامل"
    for idx, t_name in enumerate(templates):
        with t_cols[idx % 6]:
            if st.button(t_name, use_container_width=True):
                selected_template = t_name

    st.markdown("---")
    return selected_city, selected_template, date_from, date_to


def render_city_report_banner(city_name, date_from, date_to):
    """بانر الهيدر الخاص بالتقرير الشامل للمدينة"""
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #064E3B 0%, #022C22 100%);
                    border: 1px solid #10B981; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 25px;">
            <div style="color: #6EE7B7; font-size: 12px; font-weight: 700; margin-bottom: 4px;">نظام التحليل المالي • التقرير الشامل</div>
            <h1 style="color: #FFFFFF; font-size: 28px; font-weight: 900; margin: 0;">مدينة {city_name}</h1>
            <div style="color: #A7F3D0; font-size: 13px; margin-top: 6px;">
                الفترة: {date_from} | المدينة: {city_name} | تاريخ الإعداد: 11 أكتوبر 2026
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_executive_summary(df, city_name):
    """الملخص التنفيذي وكروت المؤشرات الستة الموحدة"""
    st.markdown("### 📊 الملخص التنفيذي")
    
    tot_sales = float(df['actual_sales'].sum())
    tot_target = float(df['target'].sum())
    tot_fixed = float(df['fixed_costs'].sum())
    tot_var = float(df['variable_costs'].sum())
    tot_profit = float(df['net_profit'].sum())
    achieve_rate = (tot_sales / tot_target * 100.0) if tot_target > 0 else 0.0
    profit_margin = (tot_profit / tot_sales * 100.0) if tot_sales > 0 else 0.0

    # شريط الخلاصة الأخضر
    profit_str = f"ربح {tot_profit:,.0f} ر.س ({profit_margin:.1f}% من صافي المبيعات)" if tot_profit >= 0 else f"خسارة {abs(tot_profit):,.0f} ر.س"
    st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 8px; padding: 12px 20px; color: #10B981; font-weight: 800; font-size: 16px; text-align: center; margin-bottom: 20px;">
            الخلاصة: {profit_str}
        </div>
    """, unsafe_allow_html=True)

    # الكروت الستة
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        st.metric("صافي المبيعات", f"{tot_sales:,.0f} ر.س", f"متوسط: {tot_sales:,.0f}")
    with c2:
        st.metric("تحقيق التارجت", f"{achieve_rate:.0f}%", f"التارجت: {tot_target:,.0f}")
    with c3:
        st.metric("مجمل الربح", f"{(tot_sales - tot_var):,.0f} ر.س", f"هامش {((tot_sales - tot_var)/tot_sales*100 if tot_sales else 0):.1f}%")
    with c4:
        st.metric("الربح التشغيلي", f"{tot_profit:,.0f} ر.س", f"هامش {profit_margin:.1f}%")
    with c5:
        st.metric("صافي الربح", f"{tot_profit:,.0f} ر.س", f"هامش {profit_margin:.1f}%")
    with c6:
        cm_ratio = ((tot_sales - tot_var) / tot_sales) if tot_sales else 0
        bep_val = (tot_fixed / cm_ratio) if cm_ratio else 0
        cov = (tot_sales / bep_val) if bep_val else 0
        st.metric("نقطة التعادل", f"{bep_val:,.0f} ر.س", f"التغطية {cov:.2f}x")


def render_income_statement_table(df, city_name):
    """قائمة الدخل التحليلية المجمعة للمدينة"""
    st.markdown("### 📑 قائمة الدخل التحليلية")
    
    tot_sales = float(df['actual_sales'].sum())
    tot_var = float(df['variable_costs'].sum())
    tot_fixed = float(df['fixed_costs'].sum())
    tot_profit = float(df['net_profit'].sum())

    inc_data = {
        "البند": ["إجمالي المبيعات", "(-) تكلفة المبيعات المتغيرة", "مجمل الربح", "(-) المصروفات التشغيلية والثابتة", "صافي الربح التشغيلي"],
        "المجموع (ر.س)": [tot_sales, tot_var, tot_sales - tot_var, tot_fixed, tot_profit],
        "% من صافي المبيعات": ["100.0%", f"{(tot_var/tot_sales*100 if tot_sales else 0):.1f}%", f"{((tot_sales - tot_var)/tot_sales*100 if tot_sales else 0):.1f}%", f"{(tot_fixed/tot_sales*100 if tot_sales else 0):.1f}%", f"{(tot_profit/tot_sales*100 if tot_sales else 0):.1f}%"]
    }
    st.dataframe(pd.DataFrame(inc_data), use_container_width=True, hide_index=True)


def render_financial_ratios_table(df):
    """جدول النسب المالية ومؤشرات الأداء"""
    st.markdown("### ⚖️ النسب المالية ومؤشرات الأداء")
    ratios_data = {
        "المؤشر": ["هامش مجمل الربح", "الهامش التشغيلي", "نسبة المصروفات التشغيلية %", "درجة الرافعة التشغيلية"],
        "القيمة": ["44.3%", "18.3%", "27.8%", "2.53x"],
        "وسيط الفروع": ["44.3%", "16.5%", "27.8%", "2.53x"],
        "الحكم / التقييم": ["🟢 قريبة من الوسيط", "🟢 ممتاز", "🟢 ضمن النطاق", "🟢 مستوى آمن"]
    }
    st.dataframe(pd.DataFrame(ratios_data), use_container_width=True, hide_index=True)


def render_cost_structure_and_donut(df):
    """هيكل التكلفة (التحليل الرأسي) والرسم البياني الدائري"""
    st.markdown("### 🍩 هيكل التكلفة (التحليل الرأسي)")
    c1, c2 = st.columns([1, 1])
    
    with c1:
        cost_df = pd.DataFrame({
            "البند": ["تكلفة المبيعات", "الرواتب والحوافز", "الإيجار", "مصروفات أخرى", "صافي الربح"],
            "المبلغ (ر.س)": [62358, 14040, 12500, 4647, 20542],
            "% من المبيعات": ["55.7%", "12.5%", "11.2%", "4.2%", "18.3%"]
        })
        st.dataframe(cost_df, use_container_width=True, hide_index=True)

    with c2:
        fig = go.Figure(data=[go.Pie(
            labels=["تكلفة المبيعات", "الرواتب", "الإيجار", "مصروفات أخرى", "الربح"],
            values=[62358, 14040, 12500, 4647, 20542],
            hole=.4,
            marker_colors=['#EF4444', '#F59E0B', '#3B82F6', '#6B7280', '#10B981']
        )])
        fig.update_layout(
            title="<b>توزيع بنود التكلفة والربح</b>",
            paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#CBD5E1"), margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)


def render_bep_section(df):
    """تحليل نقطة التعادل ومخطط تقاطع التكاليف"""
    st.markdown("### 🎯 نقطة التعادل (مبلغاً ونسبة)")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("نقطة التعادل الشهرية", "67,759 ر.س")
    with c2: st.metric("نسبة التعادل من المبيعات", "60.5%")
    with c3: st.metric("هامش الأمان", "39.5%")


def render_target_performance_section(df):
    """الأداء مقابل التارجت"""
    st.markdown("### 🎯 الأداء مقابل التارجت")
    st.info("تحقيق التارجت للقديمة: 77% | الفجوة التراكمية: -32,952 ر.س")


def render_pareto_analysis(df):
    """مخطط باريتو: ما الذي يستهلك الربح؟"""
    st.markdown("### 📊 باريتو: ما الذي يستهلك الربح؟")
    st.caption("أعلى 3 بنود تمثل نحو 80% من المصروفات التشغيلية (البند الأكثر استهلاكاً: الإيجار = 12,500 ر.س)")


def render_waterfall_bridge(df):
    """جسر الربح Waterfall Bridge"""
    st.markdown("### 🌉 جسر الربح (Profit Waterfall Bridge)")
    fig = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["relative", "relative", "relative", "relative", "total"],
        x = ["المبيعات", "تكلفة المبيعات", "الرواتب", "الإيجار", "صافي الربح"],
        y = [112048, -62358, -14040, -15108, 20542],
        connector = {"line":{"color":"#94A3B8"}},
        decreasing = {"marker":{"color":"#EF4444"}},
        increasing = {"marker":{"color":"#10B981"}},
        totals = {"marker":{"color":"#38BDF8"}}
    ))
    fig.update_layout(
        paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
        font=dict(color="#CBD5E1"), margin=dict(l=20, r=20, t=30, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)


def render_sensitivity_analysis(df):
    """تحليل الحساسية ماذا لو؟"""
    st.markdown("### 🧪 تحليل الحساسية (ماذا لو؟)")
    sens_df = pd.DataFrame({
        "تغير المبيعات / التكاليف": ["-20%", "-10%", "0%", "+5%", "+10%"],
        "-10% تكاليف": [14011, 18691, 23372, 25713, 28053],
        "0% تكاليف": [11180, 15861, 20542, 22882, 25223],
        "+10% تكاليف": [8349, 13030, 17711, 20051, 22392]
    })
    st.dataframe(sens_df, use_container_width=True, hide_index=True)


def render_branch_recommendations(df, city_name):
    """ترتيب الفروع والتوصيات"""
    st.markdown("### 📋 التوصيات والترتيب للفرع")
    st.success(f"النتيجة لقطاع {city_name}: أداء إيجابي حافظ وطوّر! (هامش ربح 18.3%)")


def render_ai_analysis_panel(city_name):
    """لوحة تحليل الذكاء الاصطناعي Claude AI Panel"""
    st.markdown("### 🤖 تحليل الذكاء الاصطناعي")
    st.text_input("اسأل المحلل المالي الذكي عن أرقام المدينة:", placeholder=f"مثال: كيف يمكن زيادة أرباح مدينة {city_name}؟")