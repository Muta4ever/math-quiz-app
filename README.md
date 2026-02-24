# Math Quiz App

An interactive math quiz built with [Streamlit](https://streamlit.io/) that supports arithmetic and calculus problems with a countdown timer, multiple-choice mode, and high score tracking.

## Features

- **Two problem types** — arithmetic (add, subtract, multiply, divide) and calculus (differentiation and integration using SymPy)
- **Three difficulty levels** — easy, medium, and hard (controls the range of numbers used)
- **Configurable quiz length** — 1 to 20 questions per session
- **Countdown timer** — per-question time limit of 5–60 seconds; auto-advances when time runs out
- **Multiple-choice or free-text input** — toggle between selecting an answer or typing one
- **High score tracking** — persisted locally in `highscore.txt`

## Project Structure

```
.
├── app.py            # Streamlit UI and quiz logic
├── problem.py        # QuizProblem class (problem generation and answer checking)
├── highscore.txt     # Auto-created on first run; stores the all-time high score
└── README.md
```

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [SymPy](https://www.sympy.org/)

Install dependencies:

```bash
pip install streamlit sympy
```

## Running the App

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (typically `http://localhost:8501`).

## How It Works

### `QuizProblem` (`problem.py`)

Each problem is created by instantiating `QuizProblem(difficulty, type_)`.

- **Arithmetic** — randomly picks an operator and generates operands within a range determined by difficulty (`easy`: 0–10, `medium`: 0–50, `hard`: 0–100). Division problems are constructed to always produce whole-number answers.
- **Calculus** — generates a monomial `coeff * x^power` and either differentiates or integrates it using SymPy. Answers are SymPy expressions.

The `check_answer(user_input)` method handles both integer comparison (arithmetic) and symbolic comparison via `sp.simplify` (calculus).

### Quiz Flow (`app.py`)

1. The user configures a quiz on the settings screen and clicks **Start Quiz**.
2. Questions are shown one at a time with a live countdown timer.
3. Submitting an answer or running out of time reveals whether the answer was correct.
4. After all questions, a results screen shows the score and compares it to the stored high score.

## Notes

- Calculus answers should be entered using Python/SymPy syntax, e.g. `3*x**2` for 3x².
- The high score tracks the number of correct answers (not percentage), so it is sensitive to the number of questions chosen per session.
- The app uses `time.sleep(1)` + `st.rerun()` to refresh the timer each second, which means the page rerenders every second while a question is active.