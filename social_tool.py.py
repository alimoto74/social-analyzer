import streamlit as st
import google.generativeai as genai
import os

# إعداد الأمان والمفتاح
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("Missing API Key in Secrets!")

st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

# قفل الحماية
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("أدخل رمز التنشيط:", type="password")
    if st.button("تفعيل"):
        if pwd == "PRO-2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("الرمز خطأ!")
else:
    # واجهة التطبيق بعد التفعيل
    url = st.text_input("ضع رابط الفيديو أو المنشور هنا:")
    if st.button("🚀 ابدأ التحليل"):
        if url:
            with st.spinner("ذكاء Gemini الاصطناعي يحلل الآن..."):
                try:
                    # السطر السحري لحل مشكلة 404
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"حلل هذا الرابط بعمق واذكر النقاط الأساسية: {url}")
                    st.success("التحليل المكتمل:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"تنبيه تقني: {e}")
