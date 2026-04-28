import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="محلل السوشيال ميديا", layout="centered")

# الربط بالمفتاح
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])

st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("أدخل رمز التنشيط (PRO-2026):", type="password")
    if st.button("تفعيل"):
        if pwd == "PRO-2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("الرمز خطأ")
else:
    # التبويب الذي تريده (YouTube, Facebook, etc)
    platform = st.selectbox("اختر المنصة:", ["YouTube", "Facebook", "Instagram", "TikTok"])
    url = st.text_input(f"ضع رابط {platform} هنا:")

    if st.button("🚀 ابدأ التحليل"):
        if url:
            with st.spinner("جاري التحليل..."):
                try:
                    # نحدد الموديل بدون كلمة models/ لحل خطأ 404
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"حلل هذا الرابط من {platform}: {url}")
                    st.success("تم التحليل!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
