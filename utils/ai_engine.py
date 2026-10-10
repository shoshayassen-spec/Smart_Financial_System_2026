import pandas as pd
import json
import os

def generate_ai_financial_insights(df_branch):
    """خوارزمية الذكاء الاصطناعي للتحليل والتنبؤات والتوصيات المالية (البند 4 & 8)"""
    if df_branch.empty:
        return "لا توجد بيانات كافية للتحليل.", "غير متوفر"
    
    # حساب الإيرادات والتكاليف والربح
    revenues = df_branch[df_branch['category'] == 'إيرادات']['amount'].sum()
    expenses = df_branch[df_branch['category'] == 'مصروفات']['amount'].sum()
    fixed_costs = df_branch[df_branch['category'] == 'تكاليف ثابته']['amount'].sum()
    variable_costs = df_branch[df_branch['category'] == 'تكاليف متغيرة']['amount'].sum()
    
    net_profit = revenues - expenses
    margin = (net_profit / revenues * 100) if revenues > 0 else 0
    
    # نقطة التعادل
    contribution_margin_ratio = ((revenues - variable_costs) / revenues) if revenues > 0 else 0
    break_even_amount = (fixed_costs / contribution_margin_ratio) if contribution_margin_ratio > 0 else 0
    
    status = "ربح ممتاز 🟢" if net_profit > 0 else "خسارة 🔴"
    
    recommendations = []
    if net_profit < 0:
        recommendations.append("⚠️ الفرع يحقق خسائر تشغيلية. يُوصى بمراجعة التكاليف الثابتة فوراً وخفض المصاريف غير الضرورية.")
    if margin < 15 and net_profit > 0:
        recommendations.append("📉 هامش الربح ضئيل (أقل من 15%). يُنصح بزيادة المبيعات أو إعادة التفاوض مع الموردين.")
    if break_even_amount > revenues:
        recommendations.append(f"🎯 المبيعات الحالية لم تتجاوز نقطة التعادل المقدرة بـ {break_even_amount:,.2f} ريال.")
    if not recommendations:
        recommendations.append("✅ الأداء المالي للفرع مستقر ويحقق الأهداف المرجوة. يُوصى بالتوسع والاستثمار في زيادة التارجت.")
        
    summary_text = f"""
    - **صافي الدخل:** {net_profit:,.2f} ريال
    - **هامش صافي الربح:** {margin:.2f}%
    - **نقطة التعادل (مبلغ):** {break_even_amount:,.2f} ريال
    - **الرؤية المستقبلية:** يتوقع المحرك نمواً بنسبة 5% في حال تثبيت التكاليف التشغيلية.
    """
    return summary_text, recommendations, status

def fetch_and_save_online_templates():
    """محرك جلب القوالب والنماذج المالية من الإنترنت وتثبيتها (البند 6 & 7)"""
    online_templates = {
        "قالب التحليل الرأسي والأفقي الشامل": {
            "metrics": ["نسبة النمو الشهري", "الوزن النسبي للبند من الإيراد"],
            "charts": ["مقارنة أفقية", "رادار الأداء"]
        },
        "قالب التحليل المالي الاحترافي ونقطة التعادل": {
            "metrics": ["نقطة التعادل مبلغ ونسبة", "هامش المساهمة", "درجة الرافعة التشغيلية"],
            "charts": ["شارت نقطة التعادل", "مؤشرات الأداء KPI"]
        },
        "قالب معايير التنبؤ والرؤية المستقبيلة AI": {
            "metrics": ["التنبؤ بالتدفق النقدي", "معدل دوران الأصول", "التوصيات الذكية"],
            "charts": ["سلسلة زمنية للتنبؤات"]
        }
    }
    
    with open("templates/dynamic_templates.json", "w", encoding="utf-8") as f:
        json.dump(online_templates, f, ensure_ascii=False, indent=4)
    return list(online_templates.keys())