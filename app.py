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
answers = []
for i in range(1, 21):
    ans = st.text_input(f"Answer for Q{i}", "")
    answers.append(ans)

if st.button("🔍 Find My Sport"):
    if all(answers):
        result = recommend_sport(answers)
        st.subheader("🎯 Your Recommended Sport:")
        for key, value in result.items():
            st.write(f"**{key}**: {value}")
    else:
        st.warning("Please fill in all 20 answers.")
