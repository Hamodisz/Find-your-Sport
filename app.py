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

# الأسئلة الأصلية
questions = {
    "English": [
        "1. Do you prefer to be alone or with people?",
        "2. What makes you feel focused for a long time?",
        "3. Do you like being the center of attention?",
        "4. How do you react when someone challenges you?",
        "5. What motivates you most? Winning, fun, or improving?",
        "6. Do you like danger or prefer to stay safe?",
        "7. What type of place makes you feel good? (nature, city, closed room...etc)",
        "8. Do you love tools and gear or simple action?",
        "9. If you had a power, what would it be?",
        "10. What kind of game or activity makes you forget time?",
        "11. Do you like competing with others or with yourself?",
        "12. What's more important: strength, speed, or strategy?",
        "13. Do you enjoy solving problems?",
        "14. What do you usually watch on TikTok or YouTube?",
        "15. Would you rather lead a team or act alone?",
        "16. Do you enjoy exploring new places?",
        "17. How do you feel about high places or speed?",
        "18. What kind of challenge makes you excited?",
        "19. Do you enjoy planning or prefer reacting fast?",
        "20. Do you admire athletes, gamers, or adventurers more?"
    ],
    "العربية": [
        "1. تحب تكون لحالك أو مع ناس؟",
        "2. وش الشي اللي يخليك تركز لفترة طويلة؟",
        "3. تحب تكون محط الأنظار؟",
        "4. وش تسوي إذا أحد تحداك؟",
        "5. وش أكثر شي يحفزك؟ الفوز، المتعة، أو التطور؟",
        "6. تحب الأشياء الخطيرة أو تفضل الأمان؟",
        "7. وش نوع المكان اللي يريحك؟ (طبيعة، مدينة، غرفة...الخ)",
        "8. تحب الأدوات والملابس أو الحركات البسيطة؟",
        "9. لو عندك قوة خارقة، وش بتكون؟",
        "10. وش الشي اللي يخليك تنسى الوقت إذا سويته؟",
        "11. تحب تتنافس مع غيرك أو مع نفسك؟",
        "12. الأهم عندك: القوة، السرعة، أو الذكاء؟",
        "13. تستمتع بحل المشاكل؟",
        "14. غالباً وش تشوف على تيك توك أو يوتيوب؟",
        "15. تحب تقود الفريق أو تشتغل لحالك؟",
        "16. تحب تستكشف أماكن جديدة؟",
        "17. وش شعورك تجاه المرتفعات أو السرعة؟",
        "18. وش نوع التحدي اللي يخليك تتحمس؟",
        "19. تحب تخطط ولا تشتغل بسرعة؟",
        "20. تعجبك الرياضيين، ولا اللاعبين، ولا المغامرين أكثر؟"
    ]
}

st.header("✍️ Answer the Questions")
user_answers = [st.text_input(q) for q in questions[language]]

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
