import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="المحلل الذكي", layout="centered")

# جلب المفتاح
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("المفتاح غير مضبوط في Secrets")

st.title("📊 محلل السوشيال ميديا الذكي")

# نظام التفعيل
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    code = st.text_input("رمز التنشيط (PRO-2026):", type="password")
    if st.button("تفعيل"):
        if code == "PRO-2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("الرمز خطأ")
else:
    # تبويب المنصات
    platform = st.selectbox("اختر المنصة:", ["YouTube", "Facebook", "Instagram", "TikTok"])
    url = st.text_input(f"ضع رابط {platform} هنا:")

    if st.button("ابدأ التحليل"):
        if url:
            with st.spinner("جاري التحليل..."):
                try:
                    # هذا السطر يحل مشكلة 404 للأبد
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"حلل الرابط التالي من {platform}: {url}")
                    st.success("اكتمل التحليل!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"خطأ: {e}")
