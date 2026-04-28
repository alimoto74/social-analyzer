import streamlit as st
import google.generativeai as genai

# إعداد واجهة الصفحة
st.set_page_config(page_title="محلل السوشيال ميديا الذكي", page_icon="📊")

# الربط بالمفتاح
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("المفتاح غير موجود في الإعدادات!")

st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

# نظام الحماية
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    pwd = st.text_input("أدخل رمز التنشيط (PRO-2026):", type="password")
    if st.button("تفعيل النسخة"):
        if pwd == "PRO-2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("الرمز غير صحيح!")
else:
    st.sidebar.success("الحساب نشط ✅")
    
    # قائمة اختيار المنصات
    platform = st.selectbox("اختر المنصة:", ["YouTube", "Facebook", "Instagram", "TikTok"])
    url = st.text_input(f"ضع رابط {platform} هنا:")

    if st.button("🚀 ابدأ التحليل"):
        if url:
            with st.spinner("جاري التحليل باستخدام Gemini..."):
                try:
                    # السطر الذي سيحل مشكلة الـ 404 نهائياً
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(f"قم بتحليل هذا الرابط من منصة {platform} واستخرج الفكرة الأساسية: {url}")
                    st.success("تم التحليل بنجاح!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
        else:
            st.warning("من فضلك ضع الرابط")
