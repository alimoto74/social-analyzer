import streamlit as st
import google.generativeai as genai

# إعداد مفتاح API من Secrets
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("Missing API Key! Please add it in Streamlit Secrets.")

st.set_page_config(page_title="محلل السوشيال ميديا الذكي", page_icon="📊")

st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

# نظام الحماية (رمز التنشيط)
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
    # --- بداية واجهة اختيار المنصة (التي كانت ناقصة) ---
    st.sidebar.success("تم التنشيط بنجاح ✅")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.authenticated = False
        st.rerun()

    platform = st.selectbox(
        "اختر المنصة التي تريد تحليلها:",
        ["YouTube", "Facebook", "Instagram", "TikTok"]
    )
    
    url = st.text_input(f"ضع رابط {platform} هنا:")
    # --- نهاية واجهة الاختيار ---

    if st.button("🚀 ابدأ التحليل الآن"):
        if url:
            with st.spinner(f"جاري تحليل رابط {platform} باستخدام الذكاء الاصطناعي..."):
                try:
                    # استخدام النسخة المستقرة حصراً لتجنب خطأ 404
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    prompt = f"قم بتحليل هذا الرابط {url} من منصة {platform}. استخرج الأفكار الرئيسية، نبرة المحتوى، والمشاعر العامة للجمهور."
                    
                    response = model.generate_content(prompt)
                    
                    st.success("تم التحليل بنجاح!")
                    st.markdown("### 📝 تقرير التحليل:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ تقني: {e}")
        else:
            st.warning("يرجى وضع الرابط أولاً!")
