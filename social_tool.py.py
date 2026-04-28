import streamlit as st
import google.generativeai as genai

# إعداد مفتاح API من الإعدادات المتقدمة
try:
    genai.configure(api_key=st.secrets["API_KEY"])
except:
    st.error("API Key missing! Please add it in Streamlit Secrets.")

# تحديث الموديل لاستخدام أحدث نسخة مستقرة وتجنب خطأ v1beta
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

# التحقق من رمز التنشيط
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("أدخل رمز التنشيط للاستمرار:", type="password")
    if st.button("تفعيل"):
        if password == "PRO-2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("الرمز غير صحيح!")
else:
    if st.button("تسجيل الخروج"):
        st.session_state.authenticated = False
        st.rerun()

    platform = st.selectbox("اختر المنصة", ["YouTube", "Instagram", "Facebook", "TikTok"])
    url = st.text_input(f"ضع رابط {platform} هنا:")

    if st.button("🚀 ابدأ التحليل الآن"):
        if url:
            with st.spinner("جاري التحليل باستخدام الذكاء الاصطناعي..."):
                try:
                    # طلب التحليل من Gemini
                    prompt = f"قم بتحليل هذا الرابط {url} من منصة {platform} واستخرج أهم النقاط والمشاعر العامة."
                    response = model.generate_content(prompt)
                    st.success("تم التحليل بنجاح!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
        else:
            st.warning("يرجى وضع الرابط أولاً!")
