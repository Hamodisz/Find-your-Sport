import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Title
st.title("🏅 Find Your Sport")
st.write("Answer the following questions to get your personalized sport recommendation.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("Formatted_Sport_Identity_Data-2.xlsx")
    df["Combined_Answers"] = df[[f"Q{i}" for i in range(1, 21)]].astype(str).agg(' '.join, axis=1)
    return df

df = load_data()

# Recommendation function
def recommend_sport(new_answers):
    input_str = " ".join(new_answers)
    input_vec = CountVectorizer().fit(df["Combined_Answers"]).transform([input_str])
    base_vecs = CountVectorizer().fit_transform(df["Combined_Answers"])
    similarities = cosine_similarity(input_vec, base_vecs).flatten()
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

# User input form
questions = [
    ("وش الشي اللي تحسسك إنك قوي بس بدون ما أحد يمدحك؟", "What makes you feel powerful without needing praise?"),
    ("لو في شي يخليك تنسى كل شي حولك… وش يكون؟", "What’s something that makes you forget everything around you?"),
    ("تحب تكون معروف؟ ولا تحب تكون غامض بس يهابونك؟", "Do you prefer being famous or mysterious and respected?"),
    ("تحب إذا صار فيه خصم قدامك… تضربه بقوة؟ تتفوق عليه بحركة؟ تسيطر على الموقف؟ تتجاهله كأنه ما يستاهل؟", "When facing a rival, do you attack, outsmart, dominate, or ignore?"),
    ("لو دخلت منافسة… وش أهم شي يثبت إنك الأقوى؟", "What proves you're the strongest in a competition?"),
    ("وش أقوى مشهد شفته في حياتك وعلّق براسك؟", "What’s the most powerful scene you’ve ever seen?"),
    ("هل فيه شي تعشقه أو مهووس فيه، وتتمنى لو كان له رياضة؟", "Is there something you're obsessed with that you wish was a sport?"),
    ("تحب الأشياء اللي فيها هيبة ولبس وأدوات؟ ولا تهمك الحركة نفسها؟", "Do you like gear, uniforms and style or just the movement itself?"),
    ("لو كنت وحيد في عالم خيالي… وش نوع السلاح أو القوة اللي تكون معك؟", "In a fantasy world, what weapon or power would you have?"),
    ("وش الشي اللي تسويه وتتخيل لو فيه ناس يقلدونك ويقولون: “أوه هذا أسطوري”؟", "What do you do that you wish others would admire or imitate?"),
    ("تحب تكون في مكان مفتوح؟ مغلق؟ مظلم؟ طبيعي؟ مدني؟ كله مؤثرات؟", "Do you prefer open, closed, dark, natural, urban, or cinematic spaces?"),
    ("وش أقرب وصف لك؟", "Which description fits you best?"),
    ("وش الشي اللي تحس بالهيبة لما تسويه لحد؟", "What makes you feel noble or heroic when you do it for someone?"),
    ("لو سافرت، تتوقع تنسى اللي حولك؟", "If you travel, do you feel like you'd forget your surroundings?"),
    ("هل تحب الشهرة؟ أو الغموض والقوة بدون معرفة؟", "Do you like fame, or prefer to be powerful but unknown?"),
    ("لو واجهك خصم حقيقي، تتجاهله؟ تتفوق عليه؟ تضربه؟", "When facing a real enemy, do you ignore, outsmart, or attack?"),
    ("هل فيه لحظة معينة كل الناس تركوك فيها؟", "Was there a moment everyone left you?"),
    ("وش أكثر لحظة واقعية ما تنساها؟", "What’s a real moment you’ll never forget?"),
    ("لو خيروك تملك أي شي في العالم، وش تختار؟", "If you could own anything in the world, what would it be?"),
    ("هل فيه شي فيك تتمنى الناس يقلدونه؟", "Is there something about you that you'd like others to imitate?")
]

answers = []
for i, (ar, en) in enumerate(questions, 1):
    ans = st.text_input(f"Q{i}. {ar}\n*{en}*", "")
    answers.append(ans)

if st.button("🔍 Find My Sport"):
    if all(answers):
        result = recommend_sport(answers)
        st.subheader("🎯 Your Recommended Sport:")
        for key, value in result.items():
            st.write(f"**{key}**: {value}")
    else:
        st.warning("Please fill in all 20 answers.")
