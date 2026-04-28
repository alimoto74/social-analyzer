import streamlit as st
import google.generativeai as genai

# إعداد الصفحة والواجهة
st.set_page_config(page_title="محلل السوشيال ميديا الذكي", page_icon="📊", layout="centered")

# الربط بمفتاح API من الإعدادات
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("خطأ: مفتاح API غير مفعّل في Secrets!")

st.title("📊 محلل السوشيال ميديا الذكي (VIP)")

# --- نظام التفعيل بالرمز ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 تفعيل النسخة الاحترافية")
    pwd = st.text_input("أدخل رمز التنشيط:", type="password")
    if st.button("دخول"):
        if pwd == "PRO-2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("الرمز غير صحيح!")
else:
    # --- الواجهة الرئيسية بعد التنشيط ---
    st.sidebar.success("الحساب نشط ✅")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.authenticated = False
        st.rerun()

    # خيار اختيار المنصة (الذي طلبته)
    platform = st.selectbox(
        "اختر المنصة:",
        ["YouTube", "Facebook", "Instagram", "TikTok"]
    )
    
    url = st.text_input(f"ضع رابط {platform} هنا:", placeholder="https://...")

    if st.button("🚀 ابدأ التحليل الآن"):
        if url:
            with st.spinner(f"جاري تحليل محتوى {platform} عبر Gemini 1.5..."):
                try:
                    # السطر السحري لتجنب خطأ 404 نهائياً
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    
                    prompt = f"حلل هذا الرابط {url} من منصة {platform}. اذكر النقاط الأساسية، أسلوب الطرح، ومدى تفاعل الجمهور المتوقع."
                    
                    response = model.generate_content(prompt)
                    
                    st.success("✅ اكتمل التحليل!")
                    st.markdown("### 📝 التقرير النهائي:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"تنبيه تقني: {e}")
                    st.info("نصيحة: إذا استمر الخطأ، يرجى حذف التطبيق من Streamlit وإعادة ربطه بـ GitHub.")
        else:
            st.warning("من فضلك ضع الرابط أولاً!")
