import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_city_header():
    """هيدر بطاقات FinTech المتقدمة"""
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.98) 100%);
                    border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 16px; padding: 22px; margin-bottom: 25px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.3); text-align: center;">
            <div style="display: inline-block; background: rgba(56, 189, 248, 0.15); color: #38BDF8; font-size: 12px; font-weight: 700; padding: 4px 14px; border-radius: 20px; margin-bottom: 8px;">
                🏛️ منصة إدارة وتحليل المحافظات والقطاعات الجغرافية
            </div>
            <h2 style="color: #F8FAFC; font-weight: 800; margin: 0; font-size: 24px;">استجلاء وتقارير أداء المدن والمناطق (City Analytics Hub)</h2>
            <p style="color: #94A3B8; font-size: 13px; margin-top: 6px; margin-bottom: 0;">مراقبة تجميعية لحظية مع مفاضلة الفروع وترتيب المدن المباشر</p>
        </div>
    """, unsafe_allow_html=True)


def render_city_selector_and_filter(city_list):
    """شريط التحكم والفلاتر العصرية"""
    col_sel, col_flt = st.columns([2, 1])
    with col_sel:
        selected_city = st.selectbox("🎯 اختر المدينة أو النطاق الجغرافي:", city_list)
    with col_flt:
        status_filter = st.selectbox("🔍 تصفية حسب حالة الأداء:", ["جميع الحالات", "🟢 الفروع الرابحة", "🔴 فروع تحتاج تحسين"])
    return selected_city, status_filter


def render_city_kpi_cards(df, selected_city):
    """كروت المؤشرات العليا بنمط FinTech"""
    branch_count = len(df)
    total_sales = float(df['actual_sales'].sum())
    total_target = float(df['target'].sum())
    total_profit = float(df['net_profit'].sum())
    achieve_rate = (total_sales / total_target * 100.0) if total_target > 0 else 0.0

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
            <div class="fintech-kpi-card">
                <div class="fintech-kpi-title">🏢 فروع القطاع</div>
                <div class="fintech-kpi-val" style="color:#38BDF8;">{branch_count} <span style="font-size:12px;">فرع</span></div>
                <div class="fintech-kpi-sub">تغطية: {selected_city}</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="fintech-kpi-card">
                <div class="fintech-kpi-title">💰 إجمالي مبيعات القطاع</div>
                <div class="fintech-kpi-val" style="color:#F59E0B;">{total_sales:,.0f} <span style="font-size:12px;">ريال</span></div>
                <div class="fintech-kpi-sub">المستهدف: {total_target:,.0f} ريال</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        ach_color = "#10B981" if achieve_rate >= 100.0 else "#EF4444"
        st.markdown(f"""
            <div class="fintech-kpi-card">
                <div class="fintech-kpi-title">🎯 نسبة الإنجاز الموحدة</div>
                <div class="fintech-kpi-val" style="color:{ach_color};">{achieve_rate:.1f}%</div>
                <div class="fintech-kpi-sub">المعدل المعتمد للمنطقة</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        prof_color = "#10B981" if total_profit >= 0 else "#EF4444"
        st.markdown(f"""
            <div class="fintech-kpi-card">
                <div class="fintech-kpi-title">💵 صافي الأرباح المجمعة</div>
                <div class="fintech-kpi-val" style="color:{prof_color};">{total_profit:,.0f} <span style="font-size:12px;">ريال</span></div>
                <div class="fintech-kpi-sub">السيولة النقدية المتبقية</div>
            </div>
        """, unsafe_allow_html=True)


def render_fintech_branch_cards_grid(df):
    """شبكة كروت الفروع الحديثة المماثلة لنظام Artifacts القوالب"""
    st.markdown("#### 📑 كروت أداء الفروع المسجلة (Branch Grid Cards)")

    cols = st.columns(3)
    for idx, row in df.iterrows():
        col_idx = idx % 3
        
        branch_name = row.get('branch_name', 'فرع')
        code = row.get('branch_code', '-')
        sales = row.get('actual_sales', 0.0)
        target = row.get('target', 0.0)
        profit = row.get('net_profit', 0.0)
        ach = row.get('target_achieved', 0.0)

        # تحديد الشارات الملونة
        status_badge = '<span class="badge-green">🟢 ممتاز</span>' if ach >= 100 else ('<span class="badge-yellow">🟡 متوسط</span>' if ach >= 75 else '<span class="badge-red">🔴 متأخر</span>')
        profit_badge = '<span class="badge-green">رابح</span>' if profit >= 0 else '<span class="badge-red">خاسر</span>'

        with cols[col_idx]:
            st.markdown(f"""
                <div class="fintech-grid-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span style="color:#94A3B8; font-size:11px; font-weight:700;">كود: {code}</span>
                        <div>{status_badge} {profit_badge}</div>
                    </div>
                    <h3 style="color:#F8FAFC; font-size:17px; font-weight:800; margin:0 0 10px 0;">{branch_name}</h3>
                    <div class="card-metric-row">
                        <span style="color:#CBD5E1; font-size:12px;">المبيعات الفعلية:</span>
                        <b style="color:#F59E0B; font-size:13px;">{sales:,.0f} ريال</b>
                    </div>
                    <div class="card-metric-row">
                        <span style="color:#CBD5E1; font-size:12px;">نسبة تحقيق الهدف:</span>
                        <b style="color:#38BDF8; font-size:13px;">{ach:.1f}%</b>
                    </div>
                    <div class="card-metric-row">
                        <span style="color:#CBD5E1; font-size:12px;">صافي الربح:</span>
                        <b style="color:{'#10B981' if profit >= 0 else '#EF4444'}; font-size:13px;">{profit:,.0f} ريال</b>
                    </div>
                    <div style="border-top: 1px solid rgba(255,255,255,0.08); margin-top:12px; padding-top:10px; display:flex; justify-content:space-between; font-size:11px; color:#64748B;">
                        <span>تحليل القوالب مفعل</span>
                        <span>JSON ✅</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)


def render_city_analytics_tabs(df, selected_city):
    """تحليلات القوالب المجمعة بتصاميم رسومية متطورة"""
    st.markdown("#### 📐 منصة القوالب التحليلية المجمعة القطاعية")

    tab_bep, tab_ebitda, tab_bench = st.tabs([
        "💎 [قالب 5]: التعادل والرافع المالي",
        "🚀 [قالب 6]: كشف التدفقات وEBITDA",
        "📊 [قالب 7]: الترتيب والمفاضلة المعيارية"
    ])

    tot_fixed = float(df['fixed_costs'].sum())
    tot_var = float(df['variable_costs'].sum())
    tot_sales = float(df['actual_sales'].sum())
    tot_profit = float(df['net_profit'].sum())

    cm = tot_sales - tot_var
    cm_ratio = (cm / tot_sales) if tot_sales > 0 else 0.0
    bep_val = (tot_fixed / cm_ratio) if cm_ratio > 0 else 0.0

    with tab_bep:
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("التكاليف الثابتة", f"{tot_fixed:,.0f} ريال")
        with c2: st.metric("هامش المساهمة", f"{cm:,.0f} ريال", f"{cm_ratio*100:.1f}%")
        with c3: st.metric("نقطة التعادل المجمعة", f"{bep_val:,.0f} ريال")

        fig_bep = go.Figure()
        fig_bep.add_trace(go.Bar(x=df['branch_name'], y=df['actual_sales'], name='المبيعات', marker_color='#38BDF8'))
        fig_bep.add_trace(go.Bar(x=df['branch_name'], y=df['fixed_costs'], name='ت. ثابتة', marker_color='#EF4444'))
        fig_bep.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#CBD5E1"), barmode='group', margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_bep, use_container_width=True)

    with tab_ebitda:
        ebitda_val = tot_profit + (tot_fixed * 0.15)
        ebitda_margin = (ebitda_val / tot_sales * 100.0) if tot_sales > 0 else 0.0

        st.info(f"⚡ **EBITDA قطاع {selected_city}:** {ebitda_val:,.0f} ريال | **هامش EBITDA:** {ebitda_margin:.1f}%")

        fig_eb = go.Figure(go.Bar(
            x=df['branch_name'], y=df['net_profit'],
            marker_color=np.where(df['net_profit'] >= 0, '#10B981', '#EF4444')
        ))
        fig_eb.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#CBD5E1"), margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_eb, use_container_width=True)

    with tab_bench:
        df_sorted = df.sort_values(by='target_achieved', ascending=False)
        fig_bench = go.Figure(go.Bar(
            y=df_sorted['branch_name'], x=df_sorted['target_achieved'],
            orientation='h', marker_color='#10B981'
        ))
        fig_bench.add_vline(x=100.0, line_dash="dash", line_color="#F59E0B")
        fig_bench.update_layout(
            paper_bgcolor="rgba(15, 23, 42, 0.8)", plot_bgcolor="rgba(15, 23, 42, 0.8)",
            font=dict(color="#CBD5E1"), margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_bench, use_container_width=True)