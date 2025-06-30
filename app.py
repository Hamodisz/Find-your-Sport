import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

st.set_page_config(page_title="Find Your Sport", layout="centered")

# العنوان
st.markdown("""
<h1 style='text-align: center; color: #3F8CFF;'>🏅 Find Your Sport</h1>
<p style='text-align: center;'>A sport tailored to your personality / رياضة تناسب شخصيتك</p>
""", unsafe_allow_html=True)

# اختيار اللغة
language = st.radio("🌐 Choose your language / اختر لغتك:", ["English", "العربية"])

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_excel("Formatted_Sport_Identity_Data-2.xlsx")

df = load_data()
df["Combined_Answers"] = df[[f"Q{i}" for i in range(1, 21)]].astype(str).agg(' '.join, axis=1)
vectorizer = CountVectorizer().fit_transform(df["Combined_Answers"])

# دالة التوصية
def recommend_sport(new_answers):
    input_str = " ".join(new_answers)
    input_vec = CountVectorizer().fit(df["Combined_Answers"]).transform([input_str])
    similarities = cosine_similarity(input_vec, vectorizer).flatten()
    best_match_idx = similarities.argmax()
    result = df.iloc[best_match_idx]
    return {
        "Personality Archetype": result["Personality_Archetype"],
        "Identity Archetype": result["Identity_Archetype"],
        "Recommended Sport Name": result["Recommended_Sport_Name"],
        "Sport Description": result["Sport_Description"],
        "Environment": result["Environment"],
        "Tools Needed": result["Tools_Needed"]
    }

# الأسئلة
questions = {
    "English": [...],  # نفس الأسئلة الـ 20 من قبل
    "العربية": [...]
}

if language == "English":
    question_list = questions["English"]
else:
    question_list = questions["العربية"]

st.header("✍️ Answer the Questions")
user_answers = [st.text_input(q) for q in question_list]

# زر التوصية
if st.button("🎯 Get Recommendation / احصل على الرياضة الأنسب"):
    if all(user_answers):
        translated_answers = [
            GoogleTranslator(source='auto', target='en').translate(ans) if language == "العربية" else ans
            for ans in user_answers
        ]
        result = recommend_sport(translated_answers)
        st.success("✅ Recommendation Ready / التوصية جاهزة!")

        if language == "العربية":
            translated_labels = {
                "Personality Archetype": "نوع الشخصية",
                "Identity Archetype": "الهوية",
                "Recommended Sport Name": "الرياضة المقترحة",
                "Sport Description": "وصف الرياضة",
                "Environment": "البيئة المناسبة",
                "Tools Needed": "الأدوات المطلوبة"
            }

            for k, v in result.items():
                label = translated_labels.get(k, k)
                value = GoogleTranslator(source='en', target='ar').translate(v)
                st.markdown(f"**{label}**: {value}")
        else:
            for k, v in result.items():
                st.markdown(f"**{k}**: {v}")
    else:
        st.warning("⛔ Please answer all questions. / جاوب على كل الأسئلة من فضلك.")
