import streamlit as st
import os
from utils.db_manager import DB_PATH, get_dataframe

def render():
    st.markdown("<div class='main-header'>⚙️ التبويب السابع: إعدادات النظام ومركز النسخ الاحتياطي وتفريغ الذاكرة</div>", unsafe_allow_html=True)
    
    # 1. إحصائيات قاعدة البيانات
    st.markdown("#### 📊 حالة النظام وقاعدة البيانات الحالية")
    
    try:
        branches_count = get_dataframe("SELECT COUNT(*) as cnt FROM branches").iloc[0]['cnt']
    except Exception:
        branches_count = 0

    try:
        records_count = get_dataframe("SELECT COUNT(*) as cnt FROM income_statement").iloc[0]['cnt']
    except Exception:
        records_count = 0

    db_size_mb = (os.path.getsize(DB_PATH) / (1024 * 1024)) if os.path.exists(DB_PATH) else 0.0

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown(f"""
            <div class='metric-card-container'>
                <div class='metric-title'>🏢 عدد الفروع المسجلة</div>
                <div class='metric-value'>{branches_count}</div>
                <div class='metric-sub'>نشطة في النظام</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_s2:
        st.markdown(f"""
            <div class='metric-card-container'>
                <div class='metric-title'>📜 إجمالي القيود المالية</div>
                <div class='metric-value'>{records_count:,}</div>
                <div class='metric-sub'>سجل في القوائم</div>
            </div>
        """, unsafe_allow_html=True)

    with col_s3:
        st.markdown(f"""
            <div class='metric-card-container'>
                <div class='metric-title'>💾 حجم قاعدة البيانات</div>
                <div class='metric-value'>{db_size_mb:.2f} MB</div>
                <div class='metric-sub'>SQLite Local File</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. قسم إدارة النسخ الاحتياطي
    st.markdown("#### 🛡️ مركز الحماية والنسخ الاحتياطي (Prevent Data Loss)")
    
    b_col1, b_col2 = st.columns(2)

    with b_col1:
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: 14px; padding: 18px;">
                <h4 style="color: #38BDF8; margin-top:0;">📥 تنزيل نسخة احتياطية من البيانات</h4>
                <p style="color: #CBD5E1; font-size: 13px;">قم بتنزيل قاعدة البيانات المكتملة وحفظها على كمبيوترك الشخصي لضمان عدم ضياع عملك تحت أي ظرف.</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        if os.path.exists(DB_PATH):
            with open(DB_PATH, "rb") as fp:
                st.download_button(
                    label="💾 تنزيل نسخة قاعدة البيانات (.db)",
                    data=fp,
                    file_name="financial_system_backup_2026.db",
                    mime="application/x-sqlite3",
                    use_container_width=True,
                    type="primary"
                )
        else:
            st.warning("⚠️ لا توجد قاعدة بيانات حالية لتصديرها.")

    with b_col2:
        st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.85); border: 1px solid rgba(16, 185, 129, 0.4); border-radius: 14px; padding: 18px;">
                <h4 style="color: #10B981; margin-top:0;">📤 استرجاع نسخة احتياطية سابقة</h4>
                <p style="color: #CBD5E1; font-size: 13px;">إذا قمت بإعادة تشغيل النظام وتريد استعادة كامل الفروع والقيود السابقة، قم برفع الملف الاحتياطي هنا.</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        uploaded_backup = st.file_uploader("اختر ملف قاعدة البيانات (.db)", type=["db"], key="backup_restore_uploader")
        if uploaded_backup is not None:
            if st.button("🔄 استبدال واسترجاع قاعدة البيانات فوراً", type="primary", use_container_width=True):
                try:
                    with open(DB_PATH, "wb") as f:
                        f.write(uploaded_backup.getbuffer())
                    st.success("🎉 تم استرجاع قاعدة البيانات وكامل الفروع والبيانات بنجاح!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء الاسترجاع: {str(e)}")

    st.markdown("---")

    # 3. صيانة الذاكرة المؤقتة
    st.markdown("#### 🧹 أدوات الصيانة وتفريغ الذاكرة المؤقتة")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        if st.button("🧹 تفريغ الذاكرة المؤقتة (Clear Cache)", use_container_width=True):
            st.cache_data.clear()
            st.success("✅ تم تفريغ الذاكرة المؤقتة للرسومات والجداول بنجاح!")

    with col_c2:
        if st.button("🔄 إعادة تنشيط الجلسة (Rerun Session)", use_container_width=True):
            st.rerun()