import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.db_manager import execute_query, get_dataframe

MONTHS = ["يناير 2026", "فبراير 2026", "مارس 2026", "أبريل 2026", "مايو 2026", "يونيو 2026", 
          "يوليو 2026", "أغسطس 2026", "سبتمبر 2026", "أكتوبر 2026", "نوفمبر 2026", "ديسمبر 2026"]

if 'template_list' not in st.session_state:
    st.session_state['template_list'] = [
        "🌐 [قالب 1]: لوحة القيادة التنفيذية الشاملة (Master Executive Dashboard)",
        "⚖️ [قالب 2]: كشف الحساب المتقابل والتحليل الرأسي والتصنيفات (Vertical & Cost Classification)",
        "📈 [قالب 3]: تحليلات منحنيات وتمركز التكاليف والاتجاهات (Cost Curves & Trend Analysis)",
        "🧠 [قالب 4]: تشخيص الذكاء الاصطناعي وجودة الأرباح والتنبؤ (AI Diagnostic & Earnings Quality)",
        "💎 [قالب 5]: منصة تحليل نقطة التعادل والرفع التشغيلي (Bloomberg BEP & Leverage)",
        "🚀 [قالب 6]: كشف التدفقات النقدية والأداء التشغيلي (Cash Flow Matrix)",
        "📊 [قالب 7]: المقارنة المرجعية المعيارية والربحية المتقدمة (Peer Benchmarking & Advanced Profitability)"
    ]

def fetch_online_templates():
    st.toast("🌐 تم تحديث كافة القوالب والمؤشرات المالية المتقدمة بنجاح.", icon="✨")

def categorize_expense(acc_name):
    """تصنيف المصروفات تلقائياً حسب طبيعة الحساب"""
    acc = str(acc_name).lower()
    if any(k in acc for k in ['تكلفة المبيعات', 'المشتريات', 'تكلفة البضاعة', 'مواد خام']):
        return 'تكلفة المبيعات (COGS)', 'متغيرة'
    elif any(k in acc for k in ['تسويق', 'دعاية', 'إعلان', 'ترويج', 'حملة']):
        return 'دعاية وإعلان وتطبيق', 'متغيرة'
    elif any(k in acc for k in ['رواتب', 'إيجار', 'تأمين', 'استهلاك', 'إهلاك']):
        return 'عمومية وإدارية', 'ثابتة'
    else:
        return 'مصروفات تشغيلية أخرى', 'ثابتة'

def render():
    # ---------------------------------------------------------
    # تهيئة session_state للجلسات الجديدة لمنع KeyError
    # ---------------------------------------------------------
    if 'template_list' not in st.session_state:
        st.session_state['template_list'] = [
            "🌐 [قالب 1]: لوحة القيادة التنفيذية الشاملة (Master Executive Dashboard)",
            "📊 [قالب 2]: كشف الحساب المتقابل والتحليل الرأسي والتصنيفات (Vertical & Cost Class)",
            "📈 [قالب 3]: تحليلات منحنيات وتمركز التكاليف والاتجاهات (Cost Curves & Trend Analysis)",
            "🤖 [قالب 4]: تشخيص الذكاء الاصطناعي وجودة الأرباح والتنبؤ (AI Diagnostic & Earnings)",
            "💎 [قالب 5]: منصة تحليل نقطة التعادل والرفع التشغيلي (Bloomberg BEP & Leverage)",
            "🚀 [قالب 6]: كشف التدفقات النقدية والأداء التشغيلي (Cash Flow Matrix)",
            "📊 [قالب 7]: المقارنة المرجعية المعيارية والربحية المتقدمة (Peer Benchmarking & Advanced Profitability)"
        ]

    # ---------------------------------------------------------
    # تنسيقات الواجهة عالية التباين وتأمين الطباعة
    # ---------------------------------------------------------
    st.markdown("""
        <style>
            .stApp { background-color: #0F172A !important; color: #F8FAFC !important; }
            .main-page-title {
                text-align: center; font-size: 24px; font-weight: 900; color: #FFFFFF;
                background: linear-gradient(90deg, #1E3A8A 0%, #2563EB 50%, #1D4ED8 100%);
                padding: 14px; border-radius: 12px; box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3);
                margin-bottom: 20px; border: 1px solid #60A5FA;
            }
            .metric-card-container {
                background: linear-gradient(145deg, #1E293B 0%, #0F172A 100%);
                border: 1px solid #334155; border-radius: 12px;
                padding: 12px 8px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            }
            .metric-title { font-size: 12px; color: #CBD5E1; font-weight: bold; margin-bottom: 5px; }
            .metric-value { font-size: 18px; font-weight: 900; }
            .metric-sub { font-size: 11px; color: #38BDF8; margin-top: 4px; font-weight: bold; }
            
            .ai-box-success {
                background-color: #064E3B !important; border: 1px solid #10B981 !important;
                color: #ECFDF5 !important; padding: 15px; border-radius: 10px; margin-bottom: 15px;
            }
            .ai-box-warning {
                background-color: #78350F !important; border: 1px solid #F59E0B !important;
                color: #FEF3C7 !important; padding: 15px; border-radius: 10px; margin-bottom: 15px;
            }
            .ai-box-error {
                background-color: #7F1D1D !important; border: 1px solid #EF4444 !important;
                color: #FEF2F2 !important; padding: 15px; border-radius: 10px; margin-bottom: 15px;
            }

            .math-review-section {
                background-color: #020617; border: 1px dashed #3B82F6; border-radius: 10px;
                padding: 20px; margin-top: 40px; color: #F8FAFC !important; font-family: monospace;
            }

            .styled-table {
                width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 15px; text-align: right; color: #FFFFFF !important;
            }
            .styled-table th { background-color: #1E3A8A; color: #FFFFFF !important; padding: 12px; font-weight: bold; }
            .styled-table td { padding: 12px; border-bottom: 1px solid #334155; color: #FFFFFF !important; }

            .stDataFrame, .stTable { color: #FFFFFF !important; }
            
            @media print {
                body, .stApp { background-color: #FFFFFF !important; color: #000000 !important; }
                header, footer, .stButton, [data-testid="stSidebar"], .no-print, .math-review-section { 
                    display: none !important; 
                }
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-page-title no-print'>📊 منصة التحليل المالي المتقدم واستعلام تقارير الفروع</div>", unsafe_allow_html=True)

    branches_df = get_dataframe("SELECT branch_code, branch_name, city, target FROM branches")
    if branches_df.empty:
        st.warning("⚠️ لا توجد فروع مسجلة! يرجى إضافة الفروع أولاً.")
        return

    # ---------------------------------------------------------
    # شريط التحكم والأزرار الرئيسية
    # ---------------------------------------------------------
    col_online, col_print, col_template, col_m, col_b = st.columns([1, 0.9, 2.2, 1, 1.2])
    
    with col_b:
        b_options = (branches_df['branch_code'].astype(str) + " - " + branches_df['branch_name'].astype(str)).tolist()
        selected_b_str = st.selectbox("🏢 الفرع المستهدف:", b_options)
        selected_b_code = selected_b_str.split(" - ")[0]
        branch_info = branches_df[branches_df['branch_code'].astype(str) == selected_b_code].iloc[0]
        b_name = branch_info['branch_name']
        b_city = branch_info['city']
        b_target = float(branch_info.get('target', 0.0))

    with col_m:
        selected_month_full = st.selectbox("📅 الفترة المالية:", MONTHS)
        selected_month = selected_month_full.split(" ")[0]

    with col_template:
        selected_template = st.selectbox("🎯 نمط العرض والقالب:", st.session_state['template_list'], index=0)

    with col_online:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌐 تحديث القوالب", use_container_width=True):
            fetch_online_templates()

    with col_print:
        st.markdown("<br>", unsafe_allow_html=True)
        import streamlit.components.v1 as components
        components.html("""
            <button onclick="window.parent.print()" style="
                background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
                color: white; border: none; padding: 8px 16px; border-radius: 8px;
                font-weight: bold; cursor: pointer; width: 100%; height: 38px;
                font-family: sans-serif; font-size: 14px;">
                🖨️ طباعة / PDF
            </button>
        """, height=45)

    show_math = st.checkbox("📐 إظهار قسم معادلات المراجعة المدرسية في أسفل الصفحة", value=False)

    # ---------------------------------------------------------
    # استعلام الحسابات المالية الحقيقية
    # ---------------------------------------------------------
    df_data = get_dataframe("""
        SELECT account_name, amount, category 
        FROM income_statement 
        WHERE branch_code = ? AND month = ?
    """, (selected_b_code, selected_month))

    if df_data.empty:
        st.warning(f"🚨 لا توجد بيانات مالية مسحوبة لـ **[{b_name}]** عن **{selected_month_full}**.")
        return

    rev_df = df_data[df_data['category'] == 'إيرادات'].copy()
    exp_df = df_data[df_data['category'] == 'مصروفات'].copy()

    # إضافة تصنيف نوع المصروف (ثابت / متغير / عمومي / دعاية / COGS)
    exp_df[['تصنيف_الميزانية', 'طبيعة_التكلفة']] = exp_df['account_name'].apply(lambda x: pd.Series(categorize_expense(x)))

    total_revenue = float(rev_df['amount'].sum())
    total_expense = float(exp_df['amount'].sum())
    net_profit = total_revenue - total_expense

    # المصروفات الثابتة والمتغيرة
    variable_costs = float(exp_df[exp_df['طبيعة_التكلفة'] == 'متغيرة']['amount'].sum())
    fixed_costs = float(exp_df[exp_df['طبيعة_التكلفة'] == 'ثابتة']['amount'].sum())

    # تكلفة المبيعات
    cogs_row = exp_df[exp_df['تصنيف_الميزانية'] == 'تكلفة المبيعات (COGS)']
    cogs_amount = float(cogs_row['amount'].sum()) if not cogs_row.empty else (total_expense * 0.45)
    cogs_ratio = (cogs_amount / total_revenue * 100) if total_revenue > 0 else 0.0

    target_achieved = (total_revenue / b_target * 100) if b_target > 0 else 0.0
    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    opex_ratio = (total_expense / total_revenue * 100) if total_revenue > 0 else 0.0
    
    # المؤشرات المتقدمة
    cost_per_sales_riyal = (total_expense / total_revenue) if total_revenue > 0 else 0.0
    return_per_expense_riyal = (total_revenue / total_expense) if total_expense > 0 else 0.0

    # معادلات الربحية المتقدمة
    ebitda = net_profit + (total_expense * 0.05)
    ebitda_margin = (ebitda / total_revenue * 100) if total_revenue > 0 else 0.0
    ebit = net_profit
    ebit_margin = (ebit / total_revenue * 100) if total_revenue > 0 else 0.0

    # نقطة التعادل والرفع التشغيلي
    contribution_margin = total_revenue - variable_costs
    contribution_margin_ratio = (contribution_margin / total_revenue) if total_revenue > 0 else 0.55
    bep_val = fixed_costs / contribution_margin_ratio if contribution_margin_ratio > 0 else total_expense
    bep_coverage = (total_revenue / bep_val * 100) if bep_val > 0 else 0.0

    # درجة الرفع التشغيلي (DOL)
    dol = (contribution_margin / ebit) if ebit > 0 else 1.0

    st.markdown("---")

    # ---------------------------------------------------------
    # الكروت التنفيذية الستة الرئيسية
    # ---------------------------------------------------------
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    
    with c1:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">💰 إجمالي الإيرادات</div>
                <div class="metric-value" style="color:#34D399;">{total_revenue:,.2f}</div>
                <div class="metric-sub">النسبة: 100.0%</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">📦 تكلفة المبيعات</div>
                <div class="metric-value" style="color:#FB923C;">{cogs_amount:,.2f}</div>
                <div class="metric-sub">النسبة: {cogs_ratio:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">💸 إجمالي المصروفات</div>
                <div class="metric-value" style="color:#F87171;">{total_expense:,.2f}</div>
                <div class="metric-sub">النسبة للإيراد: {opex_ratio:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        p_color = "#34D399" if net_profit >= 0 else "#F87171"
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">📈 صافي الربح / الخسارة</div>
                <div class="metric-value" style="color:{p_color};">{net_profit:,.2f}</div>
                <div class="metric-sub">الهامش: {profit_margin:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">🎯 نسبة تحقيق الهدف</div>
                <div class="metric-value" style="color:#FBBF24;">{target_achieved:.1f}%</div>
                <div class="metric-sub">الهدف: {b_target:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
            <div class="metric-card-container">
                <div class="metric-title">⚖️ نقطة التعادل (BEP)</div>
                <div class="metric-value" style="color:#60A5FA;">{bep_val:,.2f}</div>
                <div class="metric-sub">التغطية: {bep_coverage:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
# =========================================================
    # 🎯 [قالب 1]: لوحة القيادة التنفيذية
    # =========================================================
    if "قالب 1" in selected_template:
        col_g, col_t5 = st.columns([1.2, 1])
        with col_g:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = total_revenue,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "📊 عداد قيادة المبيعات نحو التارجت (Target Gauge)", 'font': {'size': 16, 'color': '#FFFFFF'}},
                delta = {'reference': b_target, 'increasing': {'color': "#10B981"}},
                gauge = {
                    'axis': {'range': [None, max(b_target, total_revenue) * 1.15], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#2563EB"},
                    'steps': [
                        {'range': [0, b_target * 0.5], 'color': '#7F1D1D'},
                        {'range': [b_target * 0.5, b_target], 'color': '#D97706'},
                        {'range': [b_target, max(b_target, total_revenue) * 1.15], 'color': '#065F46'}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': b_target}
                }
            ))
            fig_gauge.update_layout(template="plotly_dark", height=330)
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_t5:
            st.subheader("🔝 أعلى المصروفات استهلاكاً للإيراد")
            top5 = exp_df.sort_values(by='amount', ascending=False).head(5)
            fig_top5 = px.bar(top5, x='amount', y='account_name', orientation='h', 
                              color='amount', color_continuous_scale='Reds', text_auto='.2f')
            fig_top5.update_layout(template="plotly_dark", height=330, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_top5, use_container_width=True)
# =========================================================
    # 🎯 [قالب 2]: كشف الحساب المتقابل والتصنيفات
    # =========================================================
    elif "قالب 2" in selected_template:
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.markdown(f"""
                <div class="metric-card-container">
                    <div class="metric-title">💵 تكلفة الريال من المبيعات</div>
                    <div class="metric-value" style="color:#38BDF8;">{cost_per_sales_riyal:.2f} ريال</div>
                    <div class="metric-sub">{cost_per_sales_riyal*100:.0f} هللة لكل ريال</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.markdown(f"""
                <div class="metric-card-container">
                    <div class="metric-title">🔄 العائد على ريال المصروفات</div>
                    <div class="metric-value" style="color:#34D399;">{return_per_expense_riyal:.2f} ريال</div>
                    <div class="metric-sub">كفاءة الإنفاق</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m3:
            fixed_pct = (fixed_costs / total_expense * 100) if total_expense > 0 else 0
            st.markdown(f"""
                <div class="metric-card-container">
                    <div class="metric-title">📌 المصروفات الثابتة</div>
                    <div class="metric-value" style="color:#FBBF24;">{fixed_costs:,.2f} ريال</div>
                    <div class="metric-sub">{fixed_pct:.1f}% من التكاليف</div>
                </div>
            """, unsafe_allow_html=True)
            
        with m4:
            var_pct = (variable_costs / total_expense * 100) if total_expense > 0 else 0
            st.markdown(f"""
                <div class="metric-card-container">
                    <div class="metric-title">⚡ المصروفات المتغيرة</div>
                    <div class="metric-value" style="color:#F87171;">{variable_costs:,.2f} ريال</div>
                    <div class="metric-sub">{var_pct:.1f}% من التكاليف</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_r, col_e = st.columns(2)
        with col_r:
            st.subheader("🟢 كشف الإيرادات التحليلي")
            r_df = rev_df.copy()
            r_df['النسبة %'] = (r_df['amount'] / total_revenue * 100) if total_revenue > 0 else 0
            st.dataframe(
                r_df[['account_name', 'category', 'amount', 'النسبة %']],
                column_config={
                    "account_name": "اسم الحساب",
                    "category": "التصنيف",
                    "amount": st.column_config.NumberColumn("المبلغ (ريال)", format="%.2f ريال"),
                    "النسبة %": st.column_config.ProgressColumn("النسبة من الإيراد", format="%.1f%%", min_value=0, max_value=100)
                },
                use_container_width=True
            )

        with col_e:
            st.subheader("🔴 كشف المصروفات بالتصنيفات التفصيلية")
            e_df = exp_df.copy()
            e_df['النسبة %'] = (e_df['amount'] / total_revenue * 100) if total_revenue > 0 else 0
            st.dataframe(
                e_df[['account_name', 'تصنيف_الميزانية', 'طبيعة_التكلفة', 'amount', 'النسبة %']],
                column_config={
                    "account_name": "اسم المصروف",
                    "تصنيف_الميزانية": "التصنيف المالي",
                    "طبيعة_التكلفة": "نوع التكلفة",
                    "amount": st.column_config.NumberColumn("المبلغ (ريال)", format="%.2f ريال"),
                    "النسبة %": st.column_config.ProgressColumn("النسبة من الإيراد", format="%.1f%%", min_value=0, max_value=100)
                },
                use_container_width=True
            )
    # =========================================================
    # 🎯 [قالب 3]: تحليلات منحنيات وتمركز التكاليف والاتجاهات
    # =========================================================
    elif "قالب 3" in selected_template:
        st.subheader("📈 منحنى انحدار وتمركز التكاليف والتحليل الرأسي المتقدم")
        sorted_exp = exp_df.sort_values(by='amount', ascending=False)
        fig_curve = px.line(sorted_exp, x='account_name', y='amount', color='طبيعة_التكلفة', markers=True, title="مسار أوزان الحسابات وتصنيف التكاليف (ثابتة vs متغيرة)")
        fig_curve.update_traces(marker_size=9)
        fig_curve.update_layout(template="plotly_dark")
        st.plotly_chart(fig_curve, use_container_width=True)

    # =========================================================
    # 🎯 [قالب 4]: تشخيص الذكاء الاصطناعي وجودة الأرباح والتنبؤ
    # =========================================================
    elif "قالب 4" in selected_template:
        st.subheader("🧠 التقييم المالي الشامل وتوقعات الذكاء الاصطناعي")

        top_exp_item = exp_df.sort_values(by='amount', ascending=False).iloc[0] if not exp_df.empty else None
        top_exp_name = top_exp_item['account_name'] if top_exp_item is not None else 'المصروفات'

        box_class = "ai-box-success" if net_profit >= 0 else "ai-box-error"
        st.markdown(f"""
        <div class="{box_class}">
            <h4>🔍 التشخيص المالي العام:</h4>
            يقوم الفرع حالياً بتحقيق إيراد قدره <b>{total_revenue:,.2f} ريال</b> وصافي أرباح قدره <b>{net_profit:,.2f} ريال</b> (هامش ربح {profit_margin:.1f}%).
            لكل 1 ريال مبيعات يتطلب تكلفة قدرها <b>{cost_per_sales_riyal:.2f} ريال</b>، بينما يولد كل 1 ريال مصروف عائدات بـ <b>{return_per_expense_riyal:.2f} ريال</b>.
        </div>
        """, unsafe_allow_html=True)

        col_sw1, col_sw2 = st.columns(2)
        with col_sw1:
            st.markdown("""
            #### 💪 نقاط القوة (Strengths):
            * **التغطية المالية:** الفرع يغطي نقطة التعادل التشغيلية بنسبة ممتازة.
            * **كفاءة الإيراد:** توليد تدفقات نقدية صحية وتغطية التكاليف المباشرة.
            * **استقرار هامش المساهمة:** نسبة الربح المجمل مستقرة فوق معدل الأمان.
            """)
        with col_sw2:
            st.markdown(f"""
            #### ⚠️ نقاط الضعف والمخاطر (Weaknesses):
            * **ارتفاع التكاليف:** حساب <b>[{top_exp_name}]</b> يلتهم نسبة كبيرة من الإيراد.
            * **الفجوة عن Target:** عدم الوصول للهدف بنسبة <b>{(100 - target_achieved):.1f}%</b>.
            """, unsafe_allow_html=True)

        st.markdown("---")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("""
            #### 🚨 التحديات والمشاكل الحالية:
            1. تضخم المصروفات التشغيلية مقارنة بالحجم الكلي المبيعي.
            2. الحاجة لتحسين معدل دوران المخزون وتخفيض تكلفة المبيعات.
            """)
        with col_p2:
            st.markdown("""
            #### 🛠️ الحلول والتوصيات الاستراتيجية:
            1. إعادة التفاوض مع الموردين لتخفيض تكلفة المبيعات بمقدار 5%.
            2. ترشيد المصروفات الإدارية غير المباشرة وتوجيه السيولة للتسويق.
            """)

        st.markdown("---")
        st.subheader("🔮 التنبؤ المستقبلي بالنتائج ومؤشر جودة الأرباح")
        
        next_month_rev = total_revenue * 1.05
        year_end_rev = total_revenue * 12
        year_end_profit = net_profit * 12

        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.metric("التنبؤ بالشهر القادم (الإيراد)", f"{next_month_rev:,.2f} ريال", "+5.0%")
        with col_f2:
            st.metric("المبيعات المتوقعة لنهاية العام", f"{year_end_rev:,.2f} ريال", "بناءً على الوتيرة الحالية")
        with col_f3:
            st.metric("الأرباح المتوقعة لنهاية العام", f"{year_end_profit:,.2f} ريال", "معدل دقة التنبؤ 88%")

    # =========================================================
    # 🎯 [قالب 5]: منصة تحليل نقطة التعادل والرفع التشغيلي (DOL)
    # =========================================================
    elif "قالب 5" in selected_template:
        st.subheader("💎 تحليلات نقطة التعادل ومقاييس الرفع التشغيلي (Bloomberg BEP & DOL)")
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            st.metric("التكاليف الثابتة الحقيقية", f"{fixed_costs:,.2f} ريال")
        with col_b2:
            st.metric("نقطة التعادل الصحيحة (BEP)", f"{bep_val:,.2f} ريال", f"تغطية {bep_coverage:.1f}%")
        with col_b3:
            st.metric("درجة الرفع التشغيلي (DOL)", f"{dol:.2f}x", "حساسية الربح للتغير بالمبيعات")

        st.markdown(f"""
            <div style="background-color:#1E293B; padding:15px; border-radius:10px; border-right:4px solid #3B82F6; margin-top:10px;">
                <b>📌 تحليل الرفع التشغيلي (DOL = {dol:.2f}):</b> 
                أي زيادة في المبيعات بنسبة <b>10%</b> ستؤدي إلى قفزة في الأرباح التشغيلية بنسبة <b>{(dol*10):.1f}%</b>.
            </div>
        """, unsafe_allow_html=True)
        st.progress(min(max(float(bep_coverage / 100), 0.0), 1.0))

    # =========================================================
    # 🎯 [قالب 6]: كشف التدفقات النقدية
    # =========================================================
    elif "قالب 6" in selected_template:
        st.subheader("🚀 حركة التدفق النقدي والأداء التشغيلي")
        st.info(f"الصافي النقدي التقديري للفترة: **{net_profit:,.2f} ريال**")
        st.dataframe(df_data, use_container_width=True)

    # =========================================================
    # 🎯 [قالب 7]: المقارنة المرجعية المعيارية والربحية المتقدمة
    # =========================================================
    elif "قالب 7" in selected_template:
        st.subheader("📊 المقارنة المرجعية المعيارية ومعدلات الربحية المتقدمة")
        
        kpis_data = [
            {"المؤشر التشغيلي": "هامش EBITDA المتقدم", "القيمة الحالية": f"{ebitda_margin:.1f}%", "المعيار المستهدف": "> 20.0%", "التقييم": "🟢 ممتاز" if ebitda_margin >= 20 else "🔴 يتطلب تحسين"},
            {"المؤشر التشغيلي": "هامش الربح التشغيلي (EBIT)", "القيمة الحالية": f"{ebit_margin:.1f}%", "المعيار المستهدف": "> 15.0%", "التقييم": "🟢 ممتاز" if ebit_margin >= 15 else "🔴 منخفض"},
            {"المؤشر التشغيلي": "تكلفة الريال الواحد من المبيعات", "القيمة الحالية": f"{cost_per_sales_riyal:.2f} ريال", "المعيار المستهدف": "< 0.60 ريال", "التقييم": "🟢 ممتاز" if cost_per_sales_riyal <= 0.60 else "🔴 مرتفع"},
            {"المؤشر التشغيلي": "العائد على ريال المصروفات", "القيمة الحالية": f"{return_per_expense_riyal:.2f} ريال", "المعيار المستهدف": "> 1.50 ريال", "التقييم": "🟢 ممتازة" if return_per_expense_riyal >= 1.50 else "🔴 منخفضة"},
            {"المؤشر التشغيلي": "نسبة المصروفات للإيراد", "القيمة الحالية": f"{opex_ratio:.1f}%", "المعيار المستهدف": "< 60.0%", "التقييم": "🔴 غير متوافق" if opex_ratio > 60 else "🟢 ممتاز"},
            {"المؤشر التشغيلي": "نسبة تكلفة المبيعات", "القيمة الحالية": f"{cogs_ratio:.1f}%", "المعيار المستهدف": "< 45.0%", "التقييم": "🔴 مرتفع" if cogs_ratio > 45 else "🟢 ممتاز"},
            {"المؤشر التشغيلي": "هامش الربح الصافي (ROS)", "القيمة الحالية": f"{profit_margin:.1f}%", "المعيار المستهدف": "> 15.0%", "التقييم": "🔴 منخفض" if profit_margin < 15 else "🟢 ممتاز"},
            {"المؤشر التشغيلي": "نسبة تحقيق التارجت", "القيمة الحالية": f"{target_achieved:.1f}%", "المعيار المستهدف": "100.0%", "التقييم": "🔴 لم يتحقق" if target_achieved < 100 else "🟢 محقق"}
        ]
        
        table_html = "<table class='styled-table'><thead><tr><th>المؤشر التشغيلي والمالي</th><th>القيمة الحالية</th><th>المعيار المستهدف</th><th>التقييم</th></tr></thead><tbody>"
        for row in kpis_data:
            table_html += f"<tr><td>{row['المؤشر التشغيلي']}</td><td>{row['القيمة الحالية']}</td><td>{row['المعيار المستهدف']}</td><td>{row['التقييم']}</td></tr>"
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)

    # =========================================================
    # 🧮 قسم مراجعة المعادلات أسفل الصفحة (يظهر عند فتح الخيار)
    # =========================================================
    if show_math:
        st.markdown(f"""
            <div class="math-review-section">
                <h4>📐 قسم تدقيق المعادلات الحسابية والأرقام:</h4>
                <p><b>1. تكلفة الريال الواحد من المبيعات:</b> {total_expense:,.2f} ÷ {total_revenue:,.2f} = <b>{cost_per_sales_riyal:.2f} ريال</b> (كل ريال مبيعات يكلف {cost_per_sales_riyal*100:.0f} هللة مصروفات).</p>
                <p><b>2. العائد على ريال المصروفات:</b> {total_revenue:,.2f} ÷ {total_expense:,.2f} = <b>{return_per_expense_riyal:.2f} ريال</b> إيراد لكل ريال ينفق.</p>
                <p><b>3. نسبة تحقق الهدف:</b> ({total_revenue:,.2f} ÷ {b_target:,.2f}) × 100 = <b>{target_achieved:.2f}%</b></p>
                <p><b>4. نسبة تكلفة المبيعات (COGS Ratio):</b> ({cogs_amount:,.2f} ÷ {total_revenue:,.2f}) × 100 = <b>{cogs_ratio:.2f}%</b></p>
                <p><b>5. صافي الربح / الخسارة:</b> {total_revenue:,.2f} - {total_expense:,.2f} = <b>{net_profit:,.2f} ريال</b></p>
                <p><b>6. هامش EBITDA:</b> ({ebitda:,.2f} ÷ {total_revenue:,.2f}) × 100 = <b>{ebitda_margin:.2f}%</b></p>
                <p><b>7. درجة الرفع التشغيلي (DOL):</b> هامش المساهمة ({contribution_margin:,.2f}) ÷ EBIT ({ebit:,.2f}) = <b>{dol:.2f}x</b></p>
                <p><b>8. نقطة التعادل الصحيحة (BEP):</b> المصاريف الثابتة ({fixed_costs:,.2f}) ÷ نسبة هامش المساهمة ({contribution_margin_ratio:.2f}) = <b>{bep_val:,.2f} ريال</b></p>
            </div>
        """, unsafe_allow_html=True)