import streamlit as st
from problem import QuizProblem
import time
import os
import random

st.set_page_config(page_title="Math Quiz", layout="centered")

# ---------- High-score management ----------
HIGH_SCORE_FILE = "highscore.txt"

def initialize_high_score():
    if not os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write("0")

def get_high_score():
    with open(HIGH_SCORE_FILE, 'r') as f:
        return int(f.read())

def set_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write(str(score))

initialize_high_score()

# ---------- Session state initialization ----------
def init_session_state():
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'correct' not in st.session_state:
        st.session_state.correct = 0
    if 'questions' not in st.session_state:
        st.session_state.questions = []
    if 'question_start' not in st.session_state:
        st.session_state.question_start = None
    if 'settings' not in st.session_state:
        st.session_state.settings = {}
    if 'question_submitted' not in st.session_state:
        st.session_state.question_submitted = False

init_session_state()

# ---------- Quiz Settings ----------
def show_quiz_settings():
    with st.form("quiz_settings"):
        problem_type = st.selectbox("Choose problem type", ["arithmetic", "calculus"])
        difficulty = st.selectbox("Choose difficulty", ["easy", "medium", "hard"])
        num_problems = st.slider("Number of questions", 1, 20, 5)
        time_per_question = st.slider("Time per question (seconds)", 5, 60, 20)
        multiple_choice_mode = st.checkbox("Use multiple-choice questions", value=True)
        start_quiz = st.form_submit_button("Start Quiz")
    
    if start_quiz:
        st.session_state.quiz_started = True
        st.session_state.current_question = 0
        st.session_state.correct = 0
        st.session_state.questions = [QuizProblem(difficulty, problem_type) for _ in range(num_problems)]
        st.session_state.question_start = time.time()
        st.session_state.settings = {
            "problem_type": problem_type,
            "difficulty": difficulty,
            "num_problems": num_problems,
            "time_per_question": time_per_question,
            "multiple_choice_mode": multiple_choice_mode
        }
        st.session_state.question_submitted = False
        st.rerun()  # Force rerun to start the quiz immediately

# ---------- Quiz Logic ----------
def run_quiz():
    s = st.session_state.settings
    idx = st.session_state.current_question
    
    if idx < s["num_problems"]:
        q = st.session_state.questions[idx]
        st.subheader(f"Question {idx + 1} of {s['num_problems']}")
        st.text(q)
        if s["problem_type"] == "calculus":
            st.text("Hint: use x**n format for powers, e.g., 3*x**2")
        
        # ---------- Timer ----------
        elapsed = int(time.time() - st.session_state.question_start)
        remaining = max(0, s["time_per_question"] - elapsed)
        st.progress(idx / s["num_problems"])
        timer_placeholder = st.empty()
        timer_placeholder.text(f"Time remaining: {remaining} seconds")
        
        # ---------- User Answer ----------
        user_answer = None
        if s["multiple_choice_mode"]:
            # Generate and store options persistently for this question
            options_key = f'options_{idx}'
            if options_key not in st.session_state:
                correct_answer = str(q.answer)
                distractors = []
                while len(distractors) < 3:
                    offset = random.randint(-5, 5)
                    distractor = q.answer + offset
                    if distractor != q.answer and distractor not in distractors:
                        distractors.append(distractor)
                options = [correct_answer] + [str(d) for d in distractors]
                random.shuffle(options)
                st.session_state[options_key] = options
            options = st.session_state[options_key]
            user_answer = st.radio("Select the correct answer:", options, key=f"radio{idx}")
        else:
            user_answer = st.text_input("Your answer:", key=f"text{idx}")
        
        # ---------- Submit / Next ----------
        col1, col2 = st.columns(2)
        submit = col1.button("Submit", key=f"submit{idx}")
        next_btn = col2.button("Next", key=f"next{idx}", disabled=not st.session_state.question_submitted and remaining > 0)
        
        # ---------- Check answer ----------
        check_now = False
        if submit or remaining <= 0:
            check_now = True
        
        if check_now and user_answer is not None and not st.session_state.question_submitted:
            st.session_state.question_submitted = True
            if s["multiple_choice_mode"]:
                if str(user_answer) == str(q.answer):
                    st.session_state.correct += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong! Correct answer: {q.answer}")
            else:
                if str(user_answer).strip() == str(q.answer):
                    st.session_state.correct += 1
                    st.success("✅ Correct!")
                else:
                    st.error(f"❌ Wrong! Correct answer: {q.answer}")
        
        # Move to next question
        if next_btn or remaining <= 0:
            st.session_state.current_question += 1
            st.session_state.question_start = time.time()
            st.session_state.question_submitted = False
            st.rerun()  # Force rerun to move to next question
        
        # Force rerun every second for timer update if time left and not submitted
        if remaining > 0 and not st.session_state.question_submitted:
            time.sleep(1)
            st.rerun()
    
    else:
        show_quiz_finished()

# ---------- Quiz Finished ----------
def show_quiz_finished():
    score = st.session_state.correct
    s = st.session_state.settings
    st.subheader("🎉 Quiz Completed!")
    st.write(f"You got {score}/{s['num_problems']} correct ({round(100 * score / s['num_problems'])}%)")
    
    high_score = get_high_score()
    if score > high_score:
        st.balloons()
        st.write(f"🎊 New high score! Previous high score was {high_score}")
        set_high_score(score)
    else:
        st.write(f"High score: {high_score}")
    
    st.progress(1.0)
    
    if st.button("Restart Quiz"):
        st.session_state.quiz_started = False
        st.rerun()

# ---------- Main App ----------
st.title("Math Quiz App")

if not st.session_state.quiz_started:
    show_quiz_settings()
else:
    run_quiz()
