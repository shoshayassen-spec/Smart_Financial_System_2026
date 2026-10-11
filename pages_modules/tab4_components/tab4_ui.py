import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_city_header():
    """هيدر زجاجي فاخر للتبويب الرابع"""
    st.markdown("""
        <div style="text-align: center; background: linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
                    border: 1px solid rgba(56, 189, 248, 0.35); border-radius: 18px; padding: 20px; margin-bottom: 25px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.2);">
            <h2 style="color: #38BDF8; font-weight: 800; margin: 0; font-size: 22px;">🏙️ التبويب الرابع: منصة تحليلات وتقارير المدن والمناطق</h2>
            <p style="color: #94A3B8; font-size: 13px; margin-top: 6px; margin-bottom: 0;">تجميع المخرجات المالية، المفاضلة بين الفروع التابعة، وتحليل أداء القطاعات الجغرافية</p>
        </div>
    """, unsafe_allow_html=True)


def render_city_selector(city_list):
    """شريط اختيار المدينة"""
    col_sel, _ = st.columns([2, 1])
    with col_sel:
        selected_city = st.selectbox("🎯 اختر المدينة / المنطقة للتحليل المالي المجمع:", city_list)
    return selected_city


def render_city_kpi_cards(df, selected_city):
    """عرض كروت الأداء المالي المجمع للمدينة"""
    branch_count = len(df)
    total_sales = float(df['actual_sales'].sum())
    total_target = float(df['target'].sum())
    total_profit = float(df['net_profit'].sum())
    achieve_rate = (total_sales / total_target * 100.0) if total_target > 0 else 0.0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
            <div class="city-card-container" style="border-color: rgba(56, 189, 248, 0.4);">
                <div class="city-card-title">🏢 فروع المدينة</div>
                <div class="city-card-value" style="color:#38BDF8;">{branch_count} <span style="font-size:12px;">فروع</span></div>
                <div style="color:#94A3B8; font-size:11px;">تغطية: {selected_city}</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="city-card-container" style="border-color: rgba(245, 158, 11, 0.4);">
                <div class="city-card-title">💰 إجمالي مبيعات المدينة</div>
                <div class="city-card-value" style="color:#F59E0B;">{total_sales:,.0f} <span style="font-size:12px;">ريال</span></div>
                <div style="color:#94A3B8; font-size:11px;">المستهدف: {total_target:,.0f} ريال</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        achieve_color = "#10B981" if achieve_rate >= 100.0 else "#EF4444"
        st.markdown(f"""
            <div class="city-card-container" style="border-color: {achieve_color};">
                <div class="city-card-title">🎯 نسبة تحقيق الهدف</div>
                <div class="city-card-value" style="color:{achieve_color};">{achieve_rate:.1f}%</div>
                <div style="color:#94A3B8; font-size:11px;">متوسط أداء قطاع المدينة</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        profit_color = "#10B981" if total_profit >= 0 else "#EF4444"
        st.markdown(f"""
            <div class="city-card-container" style="border-color: {profit_color};">
                <div class="city-card-title">💵 صافي أرباح المدينة</div>
                <div class="city-card-value" style="color:{profit_color};">{total_profit:,.0f} <span style="font-size:12px;">ريال</span></div>
                <div style="color:#94A3B8; font-size:11px;">السيولة المجمعة المتبقية</div>
            </div>
        """, unsafe_allow_html=True)


def render_top_bottom_branches(df, selected_city):
    """مقارنة أعلى وأدنى الفروع أداءً داخل المدينة"""
    st.markdown(f"#### 🏆 مفاضلة الفروع داخل مدينة: <span style='color:#38BDF8;'>{selected_city}</span>", unsafe_allow_html=True)

    if len(df) == 0:
        return

    # ترتيب الفروع حسب صافي الربح والنسبة
    top_branch = df.sort_values(by='net_profit', ascending=False).iloc[0]
    bottom_branch = df.sort_values(by='net_profit', ascending=True).iloc[0]

    col_top, col_bot = st.columns(2)

    with col_top:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);
                        border: 1px solid #10B981; border-radius: 14px; padding: 18px;">
                <div style="color: #10B981; font-weight: 800; font-size: 15px;">🥇 أعلى فرع أداءً (الفرع الذهبي)</div>
                <h3 style="color: #F8FAFC; margin: 8px 0; font-size: 20px;">{top_branch.get('branch_name', 'غير محدد')}</h3>
                <p style="color: #CBD5E1; font-size: 13px; margin: 0;">
                    • صافي الربح: <b>{top_branch.get('net_profit', 0.0):,.0f} ريال</b><br>
                    • نسبة المستهدف: <b>{top_branch.get('target_achieved', 0.0):.1f}%</b><br>
                    • كود الفرع: <b>{top_branch.get('branch_code', '-')}</b>
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_bot:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(15, 23, 42, 0.9) 100%);
                        border: 1px solid #EF4444; border-radius: 14px; padding: 18px;">
                <div style="color: #F87171; font-weight: 800; font-size: 15px;">⚠️ أدنى فرع أداءً (يحتاج معالجة)</div>
                <h3 style="color: #F8FAFC; margin: 8px 0; font-size: 20px;">{bottom_branch.get('branch_name', 'غير محدد')}</h3>
                <p style="color: #CBD5E1; font-size: 13px; margin: 0;">
                    • صافي الربح: <b>{bottom_branch.get('net_profit', 0.0):,.0f} ريال</b><br>
                    • نسبة المستهدف: <b>{bottom_branch.get('target_achieved', 0.0):.1f}%</b><br>
                    • كود الفرع: <b>{bottom_branch.get('branch_code', '-')}</b>
                </p>
            </div>
        """, unsafe_allow_html=True)


def render_city_analytics_tabs(df, selected_city):
    """تطبيق القوالب المتقدمة (BEP, EBITDA, Benchmarking) على مستوى المدينة"""
    st.markdown("#### 📐 التحليل التشغيلي المتقدم لقوالب المدينة")

    tab_bep, tab_ebitda, tab_bench = st.tabs([
        "💎 [قالب 5]: نقطة تعادل المدينة (BEP)",
        "🚀 [قالب 6]: كشف EBITDA وتدفقات المدينة",
        "📊 [قالب 7]: القياس المعياري وترتيب الفروع"
    ])

    # حساب المجاميع العامة للمدينة
    tot_fixed = float(df['fixed_costs'].sum())
    tot_var = float(df['variable_costs'].sum())
    tot_sales = float(df['actual_sales'].sum())
    tot_profit = float(df['net_profit'].sum())

    cm = tot_sales - tot_var
    cm_ratio = (cm / tot_sales) if tot_sales > 0 else 0.0
    bep_val = (tot_fixed / cm_ratio) if cm_ratio > 0 else 0.0

    # 1. تبويب نقطة التعادل للمدينة
    with tab_bep:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("التكاليف الثابتة المجمعة", f"{tot_fixed:,.0f} ريال")
        with c2:
            st.metric("هامش المساهمة للمدينة", f"{cm:,.0f} ريال", f"{cm_ratio*100:.1f}%")
        with c3:
            st.metric("مبيعات التعادل المطلوبة (BEP)", f"{bep_val:,.0f} ريال")

        # رسم بياني للمقارنة بين المبيعات ونقطة التعادل لكل فرع في المدينة
        fig_bep = go.Figure()
        fig_bep.add_trace(go.Bar(
            x=df['branch_name'], y=df['actual_sales'],
            name='المبيعات الحقيقية', marker_color='#38BDF8'
        ))
        fig_bep.add_trace(go.Bar(
            x=df['branch_name'], y=df['fixed_costs'],
            name='التكاليف الثابتة', marker_color='#EF4444'
        ))
        fig_bep.update_layout(
            title="<b>مبيعات الفروع مقابل التكاليف الثابتة بالمدينة</b>",
            paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#CBD5E1"), barmode='group', margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_bep, use_container_width=True)

    # 2. تبويب EBITDA للتدفقات النقدية
    with tab_ebitda:
        ebitda_val = tot_profit + (tot_fixed * 0.15)  # تقدير إهلاك افتراضي
        ebitda_margin = (ebitda_val / tot_sales * 100.0) if tot_sales > 0 else 0.0

        st.info(f"⚡ **EBITDA المجمع لقطاع {selected_city}:** {ebitda_val:,.0f} ريال | **هامش EBITDA الموحد:** {ebitda_margin:.1f}%")

        fig_ebitda = go.Figure(go.Bar(
            x=df['branch_name'], y=df['net_profit'],
            marker_color=np.where(df['net_profit'] >= 0, '#10B981', '#EF4444'),
            text=[f"{val:,.0f}" for val in df['net_profit']], textposition='outside'
        ))
        fig_ebitda.update_layout(
            title="<b>مساهمة كل فرع في صافي الأرباح التشغيلية للمدينة</b>",
            paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#CBD5E1"), margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_ebitda, use_container_width=True)

    # 3. تبويب القياس المعياري وترتيب فروع المدينة
    with tab_bench:
        df_sorted = df.sort_values(by='target_achieved', ascending=False)

        fig_bench = go.Figure()
        fig_bench.add_trace(go.Bar(
            y=df_sorted['branch_name'], x=df_sorted['target_achieved'],
            orientation='h', marker_color='#10B981', name='نسبة إنجاز الفرع'
        ))
        fig_bench.add_vline(x=100.0, line_dash="dash", line_color="#F59E0B", annotation_text="المستهدف (100%)")

        fig_bench.update_layout(
            title="<b>ترتيب فروع المدينة حسب نسبة تحقيق المستهدف</b>",
            paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#CBD5E1"), margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_bench, use_container_width=True)


def render_city_branches_table(branches_data, selected_city):
    """عرض جدول بيانات الفروع التابعة للمدينة بالتنسيق المتقدم"""
    st.markdown(f"#### 📋 قائمة البيانات الممالية التفصيلية لفروع: <span style='color:#38BDF8;'>{selected_city}</span>", unsafe_allow_html=True)
    
    st.dataframe(
        branches_data,
        column_config={
            "branch_code": "كود الفرع",
            "branch_name": "اسم الفرع",
            "city": "المدينة",
            "manager_name": "مدير الفرع",
            "phone": "رقم التواصل",
            "actual_sales": st.column_config.NumberColumn("المبيعات (ريال)", format="%.0f ريال"),
            "target": st.column_config.NumberColumn("المستهدف (ريال)", format="%.0f ريال"),
            "target_achieved": st.column_config.NumberColumn("نسبة الإنجاز", format="%.1f %%"),
            "fixed_costs": st.column_config.NumberColumn("ت. ثابتة (ريال)", format="%.0f ريال"),
            "variable_costs": st.column_config.NumberColumn("ت. متغيرة (ريال)", format="%.0f ريال"),
            "net_profit": st.column_config.NumberColumn("صافي الربح (ريال)", format="%.0f ريال")
        },
        use_container_width=True,
        hide_index=True
    )