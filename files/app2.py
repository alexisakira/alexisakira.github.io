import streamlit as st
import json
import math
from pathlib import Path

st.set_page_config(page_title="Econ Salary", page_icon="📈", layout="centered")

st.title("Predicting Salaries of Economics Professors in the United States")

st.markdown("""
    <style>
    @media (prefers-color-scheme: dark) {
        .highlight-text {
            font-size: 20px;
            font-weight: bold;
            color: #FFFFFF !important;  /* White text in dark mode */
            padding: 5px;
        }
        .list-text {
            font-size: 18px;
            color: #DDDDDD !important;  /* Light gray for readability */
            padding-left: 15px;
        }
    }

    @media (prefers-color-scheme: light) {
        .highlight-text {
            font-size: 20px;
            font-weight: bold;
            color: #000000 !important;  /* Black text in light mode */
            padding: 5px;
        }
        .list-text {
            font-size: 18px;
            color: #333333 !important;  /* Dark gray for readability */
            padding-left: 15px;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="highlight-text">Developed by:</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- <a href="https://alexisakira.github.io/">Alexis Akira Toda</a>, Professor, Emory University (data analysis)</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- <a href="https://www.linkedin.com/in/zachary-etzioni-5904aa296/">Zachary Etzioni</a>, Class of 2027, Emory University (web tool)</p>', unsafe_allow_html=True)

# The model and its numbers come from KT/code/analysis/app_model.py (file app_model.json, copied unchanged).
MODEL = json.loads((Path(__file__).parent / "app_model.json").read_text(encoding="utf-8"))
COEF = MODEL["coefficients"]
LIMITS = MODEL["input_limits"]
YEAR = MODEL["display_year"]
ACCURACY = MODEL["accuracy"]["leave_campus_out"]
SAMPLE = MODEL["sample"]
TYPICAL_ERROR = round(100 * (math.exp(ACCURACY["median_abs_error"]) - 1))
SCORE_MIN, SCORE_MAX = LIMITS["score_min"], LIMITS["score_max"]

st.markdown('<p class="highlight-text">How it works:</p>', unsafe_allow_html=True)
for line in [
    f"- We use public salary records of {SAMPLE['people']:,} economics professors at {SAMPLE['campuses']} "
    f"campuses of U.S. public universities from {SAMPLE['years'][0]} to {SAMPLE['years'][1]}.",
    "- We predict your annual base salary from your rank, PhD year, publications, NBER affiliation, "
    "years at your current school, and the U.S. News score of your department. "
    "The salary does not include summer pay or other extra pay.",
    f"- We predict the salary for {SAMPLE['years'][1]} and adjust it to {YEAR} "
    "with consumer price inflation (CPI).",
    f"- We tested the model on schools that it had not seen. For half of the professors, "
    f"the prediction was within {TYPICAL_ERROR}% of their actual salary.",
    "- Our data cover only public universities. Private universities, business schools, "
    "and schools outside the U.S. may pay differently.",
]:
    st.markdown(f'<p class="list-text">{line}</p>', unsafe_allow_html=True)

st.markdown('<p class="list-text">Disclaimer: the model is still experimental</p>', unsafe_allow_html=True)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* Auto-detects dark or light mode */
    @media (prefers-color-scheme: dark) {
        html, body, .stApp {
            background-color: #121212;
            color: white;
        }
        .main-title { color: #FFD700; }  /* Gold Title in Dark Mode */
        .sub-text { color: #DDDDDD; }  /* Lighter Gray for Readability */
        .stNumberInput label, .stRadio label {
            color: white !important;
            font-weight: 600;
        }
        .stRadio div[role="radiogroup"] label {
            color: white !important;
            font-size: 16px;
            font-weight: bold;
        }
        .stNumberInput, .stRadio {
            background: #1E1E1E;
            color: white;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(255,255,255,0.1);
        }
        .stButton button {
            background-color: #1DB954;
            color: black;
        }
    }

    @media (prefers-color-scheme: light) {
        html, body, .stApp {
            background-color: white;
            color: black;
        }
        .main-title { color: #1E1E1E; }  /* Dark Title in Light Mode */
        .sub-text { color: #333333; }
        .stNumberInput label, .stRadio label {
            color: black !important;
            font-weight: 600;
        }
        .stRadio div[role="radiogroup"] label {
            color: black !important;
            font-size: 16px;
            font-weight: bold;
        }
        .stNumberInput, .stRadio {
            background: #F0F0F0;
            color: black;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        }
        .stButton button {
            background-color: #007BFF;
            color: white;
        }
    }

    .main-title {
        font-size: 36px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .sub-text {
        font-size: 18px;
        text-align: center;
        font-weight: 300;
        margin-bottom: 20px;
    }
    .stButton button {
        font-size: 18px;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        filter: brightness(1.1);
    }
    /* Hide the +/- buttons of number boxes, so that users type the numbers. */
    [data-testid="stNumberInputStepUp"], [data-testid="stNumberInputStepDown"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Enter your values below and click Compute Salary.</p>', unsafe_allow_html=True)

# A form sends the answers only when the user clicks the button, so the page does not rerun on every change.
with st.form("questions"):
    rank = st.selectbox("What is your rank?",
                        ["Assistant Professor", "Associate Professor", "Full Professor"])
    phd_year = st.number_input("In what year did you receive your PhD?",
                               min_value=1950, max_value=YEAR, value=None, step=1, format="%d",
                               placeholder="Enter the year in YYYY format")
    top5 = st.number_input(
        "How many articles have you published in the top 5 journals?",
        help="American Economic Review, Econometrica, Journal of Political Economy, "
             "Quarterly Journal of Economics, and Review of Economic Studies. "
             "Count research articles only. Do not count AER: Papers and Proceedings, "
             "AER: Insights, comments, or replies.",
        min_value=0, value=0, step=1, format="%d")
    total = st.number_input(
        "How many articles have you published in peer-reviewed journals in total, including the top 5?",
        help="Count research articles in any peer-reviewed journal. Do not count comments, replies, "
             "book chapters, AEA Papers and Proceedings, Brookings Papers, NBER Macroeconomics Annual, "
             "or surveys in the Journal of Economic Literature, the Journal of Economic Perspectives, "
             "or the Annual Reviews.",
        min_value=0, value=0, step=1, format="%d")
    nber = st.radio("Are you, or have you ever been, an NBER Research Associate or Faculty Research Fellow?",
                    ["No", "Yes"], horizontal=True)
    score = st.number_input(
        "What is the U.S. News peer assessment score of your economics department?",
        help="U.S. News rates economics PhD programs on a scale from 1 to 5 "
             "(https://www.usnews.com/best-graduate-schools/top-humanities-schools/economics-rankings). "
             f"Our data cover scores from {SCORE_MIN:.1f} to {SCORE_MAX:.1f}.",
        min_value=1.0, max_value=5.0, value=None, step=0.1, format="%.1f",
        placeholder="For example, 3.5")
    join_year = st.number_input("In what year did you start your tenure-track or tenured job at your current school?",
                                min_value=1950, max_value=YEAR, value=None, step=1, format="%d",
                                placeholder="Enter the year in YYYY format")
    submitted = st.form_submit_button("🔍 Compute Salary")


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def log_salary(age, top5, other, nber, years, tenure, full, score):
    """Predicted log salary in the base year (formula of KT/code/analysis/app_model.py)."""
    c = COEF
    return (c["const"] + c["age"] * age + c["age2_per100"] * age**2 / 100 + c["age3_per10000"] * age**3 / 1e4
            + c["top5"] * top5 + c["other_refereed"] * other + c["nber"] * nber
            + c["years_at_school"] * years + c["tenure"] * tenure + c["full"] * full + c["score"] * score)


def problems():
    if phd_year is None or join_year is None or score is None:
        return "Please answer every question."
    if total < top5:
        return "The total number of articles must include the top-5 articles."
    if join_year < phd_year - 1:
        return "Please check the years: you started at your current school long before your PhD."
    if score < SCORE_MIN - 1e-9:
        return (f"Our data cover departments with a U.S. News score of {SCORE_MIN:.1f} or higher, "
                f"so we cannot predict salaries for a score of {score:.1f}.")
    return None


if submitted:
    message = problems()
    if message:
        st.warning(message)
    else:
        tenure, full = {"Assistant Professor": (0, 0), "Associate Professor": (1, 0),
                        "Full Professor": (1, 1)}[rank]
        age = clamp(YEAR - phd_year, 0, LIMITS["career_age_max"])
        years = clamp(YEAR - join_year, 0, LIMITS["years_at_school_max"])
        log_y = log_salary(age, min(top5, LIMITS["top5_max"]), min(total - top5, LIMITS["other_refereed_max"]),
                           int(nber == "Yes"), years, tenure, full, min(score, SCORE_MAX))
        salary = math.exp(log_y) * MODEL["inflation"]["factor"]
        low = salary * math.exp(ACCURACY["error_quantiles"]["p25"])
        high = salary * math.exp(ACCURACY["error_quantiles"]["p75"])
        def r(x):
            return int(round(x / 1000) * 1000)
        st.success(f"💰 Your predicted base salary in {YEAR} is **${r(salary):,}**")
        st.markdown(f"Half of the professors in our tests earned within about {TYPICAL_ERROR}% of their "
                    f"prediction. For you, this range is **${r(low):,} to ${r(high):,}**.")
