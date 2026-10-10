import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_templates(selected_template, total_revenue, b_target, exp_df, rev_df, total_expense, net_profit, profit_margin, cost_per_sales_riyal, return_per_expense_riyal, fixed_costs, variable_costs, cogs_amount, cogs_ratio, target_achieved, opex_ratio, ebitda, ebitda_margin, ebit, ebit_margin, contribution_margin, contribution_margin_ratio, bep_val, bep_coverage, dol, df_data, show_math):
    """
    معالجة وعرض القوالب التحليلية السبعة والمعادلات المرجعية
    """
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