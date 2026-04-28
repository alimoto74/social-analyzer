import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="محلل السوشيال ميديا الذكي", page_icon="📊", layout="centered")

# جلب مفتاح API من Secrets
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("خطأ: مفتاح API غير موجود في إعدادات Secrets!")

# واجهة التطبيق
st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

# نظام التحقق من رمز التنشيط
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 تفعيل الأداة")
    password = st.text_input("أدخل رمز التنشيط للاستمرار:", type="password")
    if st.button("تفعيل"):
        if password == "PRO-2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("الرمز غير صحيح! راجع المطور.")
else:
    # شريط جانبي لتسجيل الخروج
    st.sidebar.success("تم التنشيط بنجاح ✅")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.authenticated = False
        st.rerun()

    # --- واجهة اختيار المنصة ---
    st.markdown("---")
    platform = st.selectbox(
        "اختر المنصة التي تريد تحليلها:",
        ["YouTube", "Facebook", "Instagram", "TikTok"]
    )
    
    url = st.text_input(f"ضع رابط {platform} هنا:", placeholder="https://...")

    if st.button("🚀 ابدأ التحليل الآن"):
        if url:
            with st.spinner(f"جاري تحليل محتوى {platform}..."):
                try:
                    # استدعاء الموديل بنسخة مستقرة
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"قم بتحليل هذا الرابط {url} من منصة {platform}. استخرج النقاط الرئيسية، نبرة المتحدث، وتوقعاتك لتفاعل الجمهور."
                    
                    response = model.generate_content(prompt)
                    
                    st.success("✅ اكتمل التحليل!")
                    st.markdown("### 📝 التقرير الذكي:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"تنبيه تقني: {e}")
                    st.info("نصيحة: تأكد من أن مفتاح API صحيح ومن عمل Reboot للتطبيق.")
        else:
            st.warning("من فضلك ضع الرابط أولاً!")
