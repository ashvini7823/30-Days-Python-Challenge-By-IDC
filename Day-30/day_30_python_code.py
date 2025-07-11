# --------------------------------------
# Random Quiz Generator App
# --------------------------

import requests
import random
import streamlit as st
import time

# -------------------------------
# 🎯 Constants (Category Filters)
# -------------------------------
CATEGORY = {
    "Any Category": "",
    "General Knowledge": "9",
    "Entertainment: Books": "10",
    "Entertainment: Film": "11",
    "Entertainment: Music": "12",
    "Entertainment: Musicals & Theatres": "13",
    "Entertainment: Television": "14",
    "Entertainment: Video Games": "15",
    "Entertainment: Board Games": "16",
    "Science & Nature": "17",
    "Science: Computers": "18",
    "Science: Mathematics": "19",
    "Mythology": "20",
    "Sports": "21",
    "Geography": "22",
    "History": "23",
    "Politics": "24",
    "Art": "25",
    "Celebrities": "26",
    "Animals": "27",
    "Vehicles": "28",
    "Entertainment: Comics": "29",
    "Science: Gadgets": "30",
    "Entertainment: Japanese Anime & Manga": "31",
    "Entertainment: Cartoon & Animations": "32",
}

DIFFICULTY = {
    "Any Difficulty": "",
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard"
}

QTYPE = {
    "Any Type": "",
    "Multiple Choice": "multiple",
    "True / False": "boolean"
}

QUESTION_NUMBERS = [f"Q{i+1}." for i in range(10)]

# ----------------------------------
# 🧠 Initialize Session State
# ----------------------------------
def initialize_state():
    defaults = {
        "category": "",
        "difficulty": "",
        "type": "",
        "page": "home",
        "question_index": 0,
        "quiz": [],
        "answers": ["Not Selected"] * 10,
        "shuffled_options": {},
        "scores": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ----------------------------------
# 🔗 Fetch Quiz from API
# ----------------------------------
def fetch_quiz():
    try:
        url = f"https://opentdb.com/api.php?amount=10&category={CATEGORY[st.session_state.category]}&difficulty={DIFFICULTY[st.session_state.difficulty]}&type={QTYPE[st.session_state.type]}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        st.session_state.quiz = data.get("results", [])
    except requests.exceptions.RequestException as e:
        st.error(f"🔌 Network error: {e}")
        st.session_state.quiz = []

# ----------------------------------
# 🏠 Home Page UI
# ----------------------------------
def home_page():

    col1, col2, col3 = st.columns(3)
    
    with col2:
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZzF3MnhqZjhlNmhxbXdxOXNtdXl0bzZ5YmdkMjRibnpqMXl2ajEyNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/3ohhwMDyS6rv3sB8yI/giphy.gif", width = 200)
     
    st.title("🎯 Random Quiz Generator!")

    st.session_state.category = st.selectbox("Category:", list(CATEGORY.keys()))
    st.session_state.difficulty = st.selectbox("Difficulty:", list(DIFFICULTY.keys()))
    st.session_state.type = st.selectbox("Type:", list(QTYPE.keys()))

    if st.button("Start the Quiz!"):
        st.session_state.question_index = 0
        st.session_state.answers = ["Not Selected"] * 10
        st.session_state.shuffled_options = {}
        fetch_quiz()
        if st.session_state.quiz:
            st.session_state.page = "quiz"
            st.rerun()

# ----------------------------------
# ❓ Quiz Page Logic
# ----------------------------------
def quiz_page():
    
    st.title("🧠 Brain Buster Arena!")

    # 📌 Current question
    idx = st.session_state.question_index
    current_quiz = st.session_state.quiz[idx]

    # Shuffle options only once
    if idx not in st.session_state.shuffled_options:
        options = current_quiz["incorrect_answers"].copy()
        options.append(current_quiz["correct_answer"])
        random.shuffle(options)
        st.session_state.shuffled_options[idx] = options

    options = st.session_state.shuffled_options[idx]
    prev_selection = st.session_state.answers[idx]

    default_index = options.index(prev_selection) if prev_selection in options else None
    question_text = f"{QUESTION_NUMBERS[idx]} {current_quiz['question']}"
    st.markdown(question_text)

    selected_option = st.radio(
        label="options",
        options=options,
        index=default_index,
        key=f"radio_{idx}",
        label_visibility="hidden"
    )
    st.session_state.answers[idx] = selected_option

    # Navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Previous", disabled=idx == 0):
            st.session_state.question_index -= 1
            st.rerun()

    with col2:
        if st.button("Next", disabled=idx == 9):
            st.session_state.question_index += 1
            st.rerun()

    with col3:
        if st.button("Submit"):
            score = sum(
                1 for i, q in enumerate(st.session_state.quiz)
                if st.session_state.answers[i] == q["correct_answer"]
            )
            st.session_state.scores = score
            st.session_state.page = "result"
            st.rerun()

# ----------------------------------
# 🏁 Result Page
# ----------------------------------
def result_page():
    st.title("🏁 Quiz Summary")

    score = st.session_state.scores
    percentage = score * 10

    col1, col2 = st.columns(2)

    with col1:
        # sticker
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2RybHVtaDlrdTdvNTBiMzV3ampsYWx2aWhuMmtsaXBpNG10d2lyZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/akb7cs9vSeN5QBazEI/giphy.gif", width = 150)
    with col2:
        # Score banner
        st.markdown(f"""
                        <div style="background: linear-gradient(90deg, #43A047, #2E7D32); padding: 18px 30px; border-radius: 12px; color: white; font-size: 22px; font-weight: 600; text-align: center; width: fit-content; margin-top: 40px; box-shadow: 2px 4px 12px rgba(0,0,0,0.25);">
                        You scored {percentage}% 🎯
                        </div>
                     """, unsafe_allow_html=True)

    # Review each question
    st.subheader("You can review your answers below")
    for i, quiz in enumerate(st.session_state.quiz):
        st.markdown(f"{QUESTION_NUMBERS[i]} {quiz['question']}")
        st.write("Your Answer:")
        if st.session_state.answers[i] == quiz["correct_answer"]:
            st.success(f"✅ {st.session_state.answers[i]}")
        else:
            st.error(f"❌ {st.session_state.answers[i]}")
            st.write("Correct Answer:")
            st.success(quiz["correct_answer"])

    # Summary stats
    st.markdown(f"""
    ### 📊 Your Results:
    - ✅ Correct Answers: **{score} / 10**
    - 🧮 Total Score: **{score * 10} / 100**
    - 📈 Percentage: **{percentage}%**
    """)

    # Motivational feedback
    if percentage == 100:
        st.balloons()
        st.success("🎯 Perfect Score! You're a quiz master!")
    elif percentage >= 80:
        st.balloons()
        st.success("🔥 Great job! You really know your stuff.")
    elif percentage >= 50:
        st.info("👍 Good effort! Keep practicing to improve.")
    else:
        st.info("💡 Don't worry, try again and you'll get better!")

    # Play again button
    if st.button("🔁 Play Again"):
        for key in ["category", "difficulty", "type", "question_index", "quiz", "answers", "shuffled_options", "scores", "gif_list"]:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.page = "home"
        st.rerun()

# ----------------------------------
# 🚀 Run the App
# ----------------------------------
def main():
    initialize_state()
    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "quiz":
        quiz_page()
    elif st.session_state.page == "result":
        result_page()

# Launch the app
if __name__ == "__main__":
    main()

