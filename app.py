import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

st.set_page_config(page_title="Find Your Sport", layout="centered")

# Title
st.markdown("""
<h1 style='text-align: center; color: #3F8CFF;'>🏅 Find Your Sport</h1>
<p style='text-align: center;'>Answer the following questions to get your personalized sport recommendation.</p>
""", unsafe_allow_html=True)

# Language selection
language = st.radio("🌐 Choose your language / اختر لغتك:", ["English", "العربية"])

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("Formatted_Sport_Identity_Data-2.xlsx")

df = load_data()
df["Combined_Answers"] = df[[f"Q{i}" for i in range(1, 21)]].astype(str).agg(' '.join, axis=1)
vectorizer = CountVectorizer().fit_transform(df["Combined_Answers"])
similarity_matrix = cosine_similarity(vectorizer)

def recommend_sport(new_answers):
    input_str = " ".join(new_answers)
    input_vec = CountVectorizer().fit(df["Combined_Answers"]).transform([input_str])
    similarities = cosine_similarity(input_vec, vectorizer).flatten()
    best_match_idx = similarities.argmax()
    result = df.iloc[best_match_idx]
    return {
        "Personality_Archetype": result["Personality_Archetype"],
        "Identity_Archetype": result["Identity_Archetype"],
        "Recommended_Sport_Name": result["Recommended_Sport_Name"],
        "Sport_Description": result["Sport_Description"],
        "Environment": result["Environment"],
        "Tools_Needed": result["Tools_Needed"]
    }

# Questions
questions = {
    "English": [
        "1. What's something that makes you feel strong without praise?",
        "2. What activity makes you forget everything else?",
        "3. Do you like being known? Or mysterious but respected?",
        "4. If facing a rival, would you dominate? Outsmart? Ignore?",
        "5. What proves you're the strongest?",
        "6. What's a powerful scene burned into your memory?",
        "7. Is there something you're obsessed with and wish it were a sport?",
        "8. Do you prefer impressive gear or raw movement?",
        "9. If alone in a fantasy world, what weapon or power would you have?",
        "10. What do you do that others would copy and admire?",
        "11. Preferred environment? Open, closed, dark, natural, urban, effects?",
        "12. Pick your archetype: Tactical Player / Shadow Driver / Ninja Warrior / Lone King / Clever Villain / Silent Killer",
        "13. What makes you feel respected the most?",
        "14. If you travel abroad, what would change inside you?",
        "15. Do you like fame or hate being in the spotlight?",
        "16. How do you usually react when challenged?",
        "17. Share a moment where everyone gave up and you didn’t.",
        "18. What's a dark thought or event that shaped you?",
        "19. Describe your dream life with vehicles and tools.",
        "20. Is there anyone you admire or wish to become like?"
    ],
    "العربية": [
        "1. وش الشي اللي يحسسك إنك قوي بدون ما أحد يمدحك؟",
        "2. وش الشي اللي يخليك تنسى العالم كله حولك؟",
        "3. تحب تكون معروف؟ ولا غامض بس يهابونك؟",
        "4. لو قدامك خصم: تسيطر؟ تتفوق عليه؟ تتجاهله؟",
        "5. وش يثبت إنك الأقوى؟",
        "6. وش أقوى مشهد شفته وعلق في ذاكرتك؟",
        "7. هل في شي مهووس فيه وتتمنى لو له رياضة؟",
        "8. تحب اللبس والأدوات؟ ولا تهمك الحركات؟",
        "9. لو كنت وحيد في عالم خيالي، وش القوة أو السلاح اللي معك؟",
        "10. وش تسوي وتتخيل ناس يقلدونك فيه؟",
        "11. تحب تكون في مكان: مفتوح، مغلق، مظلم، طبيعي، مدني؟",
        "12. اختر وصفك: لاعب تكتيكي / سائق شبح / نينجا / ملك بلا عرش / شرير ذكي / هادئ وقاتل",
        "13. متى تحس باحترام الناس لك؟",
        "14. لو سافرت للخارج، وش الشي اللي راح يتغير فيك؟",
        "15. تحب الشهرة؟ ولا تكره الأضواء؟",
        "16. كيف تتصرف إذا أحد تحداك؟",
        "17. متى استسلم الكل وبقيت أنت؟",
        "18. وش فكرة سوداوية أو لحظة غيرتك؟",
        "19. وصف حياتك الحلم مع السيارات والأدوات؟",
        "20. هل في شخص تتمناه أو تبي تصير مثله؟"
    ]
}

st.header("✍️ Answer the Questions")
user_answers = []
for q in questions[language]:
    user_answers.append(st.text_input(q))

# Recommendation Button
if st.button("🎯 Get Recommendation / احصل على الرياضة الأنسب"):
    if all(user_answers):
        translated_answers = [GoogleTranslator(source='auto', target='en').translate(ans) for ans in user_answers]
        result = recommend_sport(translated_answers)
        st.success("✅ Recommendation Ready / التوصية جاهزة!")
        for k, v in result.items():
            st.markdown(f"**{k.replace('_', ' ')}**: {v}")
    else:
        st.warning("⛔ Please answer all questions. / جاوب على كل الأسئلة من فضلك.")
