import os
import importlib
import streamlit as st

def get_available_templates():
    """
    قراءة واكتشاف جميع القوالب الموجودة داخل مجلد templates تلقائياً
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    template_modules = {}
    
    if os.path.exists(templates_dir):
        for file in sorted(os.listdir(templates_dir)):
            if file.startswith("template_") and file.endswith(".py"):
                module_name = file[:-3]
                try:
                    mod = importlib.import_module(f"pages_modules.tab3_components.templates.{module_name}")
                    if hasattr(mod, "TEMPLATE_TITLE") and hasattr(mod, "render"):
                        template_modules[mod.TEMPLATE_TITLE] = mod
                except Exception as e:
                    pass
    return template_modules

def render_templates(selected_template, **kwargs):
    """
    استدعي القالب المختار ديناميكياً
    """
    available_templates = get_available_templates()
    
    # تحديث قائمة القوالب في الجلسة إذا زادت
    st.session_state['template_list'] = list(available_templates.keys())
    
    if selected_template in available_templates:
        mod = available_templates[selected_template]
        mod.render(**kwargs)
    else:
        st.info("💡 يرجى اختيار قالب تحليلي من القائمة المنسدلة أعلاه.")