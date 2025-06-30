import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# واجهة البداية
st.markdown("""
<h1 style='text-align: center; color: #3F8CFF;'>🏁 Find Your Sport</h1>
<p style='text-align: center;'>Answer 20 powerful questions to discover your unique sport identity</p>
""", unsafe_allow_html=True)

start = st.button("🎯 Start Now")

if not start:
    st.stop()

# تحميل البيانات
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

# الأسئلة
st.header("🧠 Your Sport Identity Questions")

q1 = st.text_input("1. What's something that makes you feel strong without praise?")
q2 = st.text_input("2. What activity makes you forget everything else?")
q3 = st.text_input("3. Do you like being known? Or mysterious but respected?")
q4 = st.text_input("4. If facing a rival, would you dominate? Outsmart? Ignore?")
q5 = st.text_input("5. What proves you're the strongest?")
q6 = st.text_input("6. What's a powerful scene burned into your memory?")
q7 = st.text_input("7. Is there something you're obsessed with and wish it were a sport?")
q8 = st.text_input("8. Do you prefer impressive gear or raw movement?")
q9 = st.text_input("9. If alone in a fantasy world, what weapon or power would you have?")
q10 = st.text_input("10. What do you do that others would copy and admire?")
q11 = st.text_input("11. Preferred environment? Open, closed, dark, natural, urban, effects?")
q12 = st.text_input("12. Pick your archetype: Tactical Player / Shadow Driver / Ninja Warrior / Lone King / Clever Villain / Silent Killer")
q13 = st.text_input("13. What makes you feel respected the most?")
q14 = st.text_input("14. If you travel abroad, what would change inside you?")
q15 = st.text_input("15. Do you like fame or hate being in the spotlight?")
q16 = st.text_input("16. How do you usually react when challenged?")
q17 = st.text_input("17. Share a moment where everyone gave up and you didn’t.")
q18 = st.text_input("18. What's a dark thought or event that shaped you?")
q19 = st.text_input("19. Describe your dream life with vehicles and tools.")
q20 = st.text_input("20. Is there anyone you admire or wish to become like?")

answers = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10,
           q11, q12, q13, q14, q15, q16, q17, q18, q19, q20]

# زر النتيجة
if st.button("🚀 Get My Sport Recommendation"):
    if all(answers):
        result = recommend_sport(answers)
        st.success("🎯 Your personalized sport has been found!")
        for k, v in result.items():
            st.markdown(f"**{k.replace('_', ' ')}**: {v}")
    else:
        st.warning("Please answer all questions before getting your sport.")
