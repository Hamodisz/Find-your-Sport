
import streamlit as st

# ----------------------------
# Language Selection
# ----------------------------
lang = st.sidebar.selectbox("Select Language / اختر اللغة", ["English", "العربية"])

# ----------------------------
# Questions in Both Languages
# ----------------------------
questions = {
    "English": [
        "What makes you feel strong without anyone praising you?",
        "What pulls you into a flow state easily?",
        "Do you prefer to be known or mysterious but respected?",
        "If facing an opponent, do you strike, outsmart, control, or ignore?",
        "In competition, what proves you're the strongest?",
        "What’s the most powerful scene you remember?",
        "Is there something you love deeply and wish had its own sport?",
        "Do you prefer gear/style or pure movement?",
        "In a fantasy world, what power or weapon would you have?",
        "What action makes others say: 'That’s legendary'?",
        "What kind of place do you enjoy most?",
        "Which persona fits you best?"
    ],
    "العربية": [
        "وش الشي اللي تحسسك إنك قوي بدون ما أحد يمدحك؟",
        "وش يسحبك لعالم ثاني بسرعة؟",
        "تحب تكون معروف؟ ولا غامض بس يهابونك؟",
        "قدام خصم... تضرب؟ تتفوق؟ تسيطر؟ تتجاهل؟",
        "وش يثبت إنك الأقوى في التحدي؟",
        "أقوى مشهد تتذكره في حياتك؟",
        "في شي تعشقه وتتمنى يكون له رياضة؟",
        "تحب اللبس والأدوات؟ ولا الحركة نفسها؟",
        "بعالم خيالي... وش القوة أو السلاح اللي معك؟",
        "وش تسوي ويخلي الناس يقولون عنك أسطورة؟",
        "تحب الأماكن المفتوحة؟ طبيعية؟ مظلمة؟",
        "أي وصف يعبر عنك؟"
    ]
}

# ----------------------------
# Collect Answers
# ----------------------------
st.title("Find Your Sport 🔍🏅")

answers = []
for q in questions[lang]:
    a = st.text_input(q)
    answers.append(a)

if st.button("Get My Sport Recommendation 🎯"):
    if all(ans.strip() != "" for ans in answers):
        # Fake logic (replace with real model)
        st.success("🎽 Your Sport: Phantom Rush")
        st.write("A fast-paced decision sport where dominance is subtle and skill-based.")
        st.write("🧠 Personality: Tactical Ghost")
        st.write("🌍 Environment: VR Room")
        st.write("🛠 Tools: Training Sword")
    else:
        st.warning("Please answer all questions.")
