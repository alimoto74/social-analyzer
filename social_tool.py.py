import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="VIP Social Media Analyzer", page_icon="📊", layout="centered")

# إعداد مفتاح API - تأكد أن الاسم في Secrets هو GOOGLE_API_KEY
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("خطأ: GOOGLE_API_KEY غير موجود في إعدادات Secrets!")

st.title("📊 Social Media Report Generator (VIP)")

# نظام الحماية
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("أدخل رمز التنشيط (PRO-2026):", type="password")
    if st.button("تفعيل"):
        if pwd == "PRO-2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("الرمز غير صحيح!")
else:
    # الواجهة الاحترافية (كما في صورتك الأخيرة)
    platform = st.selectbox("Platform / المنصة:", ["YouTube", "Instagram", "TikTok", "Facebook"])
    url = st.text_input("Post URL / رابط المنشور")

    col1, col2, col3 = st.columns(3)
    with col1:
        views = st.text_input("Views / المشاهدات", value="0")
    with col2:
        likes = st.text_input("Likes / الإعجابات", value="0")
    with col3:
        comments = st.text_input("Comments / التعليقات", value="0")

    description = st.text_area("Content Description / وصف المحتوى")

    if st.button("🚀 Generate Report / إصدار التقرير"):
        if not url:
            st.warning("يرجى إدخال الرابط")
        else:
            with st.spinner("جاري التحليل..."):
                try:
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    prompt = f"Create a professional report for {platform} post: {url}. Stats: Views={views}, Likes={likes}, Comments={comments}. Content: {description}"
                    response = model.generate_content(prompt)
                    
                    st.success("Report Ready ✅")
                    st.markdown("### 📄 التقرير:")
                    st.write(response.text)
                    
                    st.download_button("📥 Download Report", response.text, file_name="report.txt")
                except Exception as e:
                    st.error(f"تنبيه تقني: {e}")
