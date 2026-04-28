import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="VIP Social Media Analyzer", page_icon="📊", layout="centered")

# إعداد مفتاح API من Secrets
# ملاحظة: تأكد أن اسم المفتاح في Secrets هو GOOGLE_API_KEY
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("خطأ: GOOGLE_API_KEY غير موجود في إعدادات Secrets!")

st.title("📊 Social Media Report Generator (VIP)")

# --- نظام الحماية (رمز التنشيط) ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.subheader("🔐 تفعيل النسخة الاحترافية")
    pwd = st.text_input("أدخل رمز التنشيط للاستمرار:", type="password")
    if st.button("تفعيل الآن"):
        if pwd == "PRO-2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("الرمز غير صحيح!")
else:
    # --- الواجهة الرئيسية بعد التفعيل ---
    st.sidebar.success("تم التنشيط بنجاح ✅")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    # إدخال البيانات الأساسية
    platform = st.selectbox("Platform / المنصة:", ["YouTube", "Instagram", "TikTok", "Facebook"])
    url = st.text_input("Post URL / رابط المنشور")

    # تقسيم المدخلات الرقمية في أعمدة
    col1, col2, col3 = st.columns(3)
    with col1:
        views = st.text_input("Views / المشاهدات", value="0")
    with col2:
        likes = st.text_input("Likes / الإعجابات", value="0")
    with col3:
        comments = st.text_input("Comments / التعليقات", value="0")

    description = st.text_area("Content Description / وصف المحتوى (اختياري)")

    if st.button("🚀 Generate Report / إصدار التقرير"):
        if not url:
            st.warning("يرجى إدخال الرابط أولاً")
        else:
            with st.spinner("جاري تحليل البيانات وإصدار التقرير..."):
                try:
                    # استدعاء الموديل
                    model = genai.GenerativeModel("gemini-1.5-flash")

                    # صياغة طلب احترافي للذكاء الاصطناعي
                    prompt = f"""
                    Create a professional social media performance report based on the following data:
                    
                    Platform: {platform}
                    URL: {url}
                    Views: {views}
                    Likes: {likes}
                    Comments: {comments}
                    Description: {description}

                    The report must include these sections in a clear, executive tone:
                    1. Content Overview (What is the post about?)
                    2. Performance Analysis (Analyze the numbers relative to the platform)
                    3. Strengths (What worked well?)
                    4. Weaknesses (What could be better?)
                    5. Improvement Suggestions (Practical advice)
                    6. Viral Opportunities (How to make it go viral?)

                    Language: Support both English and Arabic if possible, but keep the core analysis professional.
                    """

                    response = model.generate_content(prompt)
                    report = response.text

                    st.success("Report Ready / التقرير جاهز ✅")

                    st.markdown("### 📄 Professional Report")
                    st.write(report)

                    # أدوات التصدير
                    st.divider()
                    st.subheader("🛠️ أدوات التصدير")
                    
                    # مربع النسخ
                    st.code(report, language="markdown")

                    # تحميل الملف
                    st.download_button(
                        label="📥 Download Report (.txt)",
                        data=report,
                        file_name=f"{platform}_Performance_Report.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"حدث خطأ تقني: {e}")
