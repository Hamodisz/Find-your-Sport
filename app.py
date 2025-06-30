import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

data = [
    {
        "Combined_Answers": "Observes quietly Avoids showing off Mental challenge Expresses with motion Prefers silence Tactical Ghost Phantom Rush A fast-paced decision sport where dominance is subtle and skill-based. VR room Training sword",
        "Personality_Archetype": "Tactical Ghost",
        "Identity_Archetype": "The Phantom",
        "Recommended_Sport_Name": "Phantom Rush",
        "Sport_Description": "A fast-paced decision sport where dominance is subtle and skill-based.",
        "Environment": "VR room",
        "Tools_Needed": "Training sword"
    },
    {
        "Combined_Answers": "Avoids showing off Mental challenge Observes quietly Shadow Strategist Phantom Rush A fast-paced decision sport where dominance is subtle and skill-based. Dark indoor arena Sound sensor",
        "Personality_Archetype": "Shadow Strategist",
        "Identity_Archetype": "The Phantom",
        "Recommended_Sport_Name": "Phantom Rush",
        "Sport_Description": "A fast-paced decision sport where dominance is subtle and skill-based.",
        "Environment": "Dark indoor arena",
        "Tools_Needed": "Sound sensor"
    },
    {
        "Combined_Answers": "Observes quietly Avoids showing off Tactical Ghost Urban Arena Tactical competition with indirect interaction and positioning. Dark indoor arena VR headset",
        "Personality_Archetype": "Tactical Ghost",
        "Identity_Archetype": "The Observer",
        "Recommended_Sport_Name": "Urban Arena",
        "Sport_Description": "Tactical competition with indirect interaction and positioning.",
        "Environment": "Dark indoor arena",
        "Tools_Needed": "VR headset"
    }
]

df = pd.DataFrame(data)
vectorizer = CountVectorizer().fit(df["Combined_Answers"])
vectors = vectorizer.transform(df["Combined_Answers"])

def recommend_sport(new_answers):
    input_str = " ".join(new_answers)
    input_vec = vectorizer.transform([input_str])
    similarities = cosine_similarity(input_vec, vectors).flatten()
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
