import streamlit as st
import google.generativeai as genai
import os

# إعداد الصفحة
st.set_page_config(page_title="محلل السوشيال ميديا الذكي", layout="centered")

# التأكد من وجود المفتاح
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets!")

st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

# نظام التفعيل
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 تفعيل النسخة")
    code = st.text_input("أدخل رمز التنشيط (PRO-2026):", type="password")
    if st.button("تفعيل"):
        if code == "PRO-2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("الرمز غير صحيح!")
else:
    # إظهار تبويب المنصات (مهم جداً)
    st.markdown("---")
    platform = st.selectbox(
        "اختر المنصة التي تريد تحليلها:",
        ["YouTube", "Facebook", "Instagram", "TikTok"]
    )
    
    url = st.text_input(f"ضع رابط {platform} هنا:")

    if st.button("🚀 ابدأ التحليل"):
        if url:
            with st.spinner("جاري التحليل..."):
                try:
                    # استخدام الموديل بتحديد النسخة المستقرة
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # صياغة الطلب
                    prompt = f"حلل هذا الرابط من {platform}: {url}. اعطني ملخصاً ذكياً للمحتوى ونبرة الكلام."
                    
                    response = model.generate_content(prompt)
                    
                    st.success("✅ تم التحليل بنجاح!")
                    st.write(response.text)
                except Exception as e:
                    # عرض الخطأ بشكل مبسط إذا حدث
                    st.error(f"تنبيه تقني: {str(e)}")
        else:
            st.warning("يرجى وضع الرابط أولاً!")
