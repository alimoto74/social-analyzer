import streamlit as st
import google.generativeai as genai

# 1. إعداد المفتاح
genai.configure(api_key="AIzaSyDvgGljJPtGBkZwFvCO4QHAeGKQmVsxKaw")

# 2. تعريف الموديل
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)

st.set_page_config(page_title="محلل السوشيال ميديا المحمي", layout="wide")

# --- نظام الحماية ---
# هنا تحدد كود التنشيط الذي ستعطيه لأصدقائك
ACCESS_CODE = "PRO-2026" 

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.title("🔐 تفعيل الأداة")
    user_code = st.text_input("أدخل رمز التنشيط للاستمرار:", type="password")
    if st.button("تفعيل"):
        if user_code == ACCESS_CODE:
            st.session_state['authenticated'] = True
            st.success("تم التفعيل بنجاح!")
            st.rerun()
        else:
            st.error("الرمز خاطئ! يرجى التواصل مع صاحب الأداة.")
else:
    # --- الكود الأصلي للأداة يوضع هنا بعد التفعيل ---
    st.title("📊 محلل السوشيال ميديا الذكي (نسخة الـ VIP)")
    if st.button("تسجيل الخروج"):
        st.session_state['authenticated'] = False
        st.rerun()
    
    st.markdown("---")
    platform = st.selectbox("اختر المنصة", ["YouTube", "Instagram", "TikTok", "LinkedIn", "X (Twitter)"])
    url = st.text_input(f"ضع رابط {platform} هنا:")

    if st.button("🚀 ابدأ التحليل الآن"):
        if url:
            with st.spinner('جاري التحليل...'):
                try:
                    prompt = f"حلل هذا الرابط كخبير سوشيال ميديا باللغة العربية: {url}"
                    response = model.generate_content(prompt)
                    st.success("✅ تم التحليل!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
