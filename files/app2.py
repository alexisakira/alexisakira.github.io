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
JUMP = MODEL["large_raise"]
JUMP_LIMITS = JUMP["input_limits"]
# Plausible answers. Outside these ranges, the app asks the user to check the answer instead of predicting.
PHD_YEAR_MIN = YEAR - 70
MAX_COUNTS = {"top5": 50, "other": 400, "invited": 100, "recent_top5": 10, "recent_other": 40}
SALARY_MIN, SALARY_MAX = 30_000, 2_000_000

st.markdown('<p class="highlight-text">How it works:</p>', unsafe_allow_html=True)
for line in [
    f"- We use public salary records of {SAMPLE['people']:,} economics professors with complete records at "
    f"{SAMPLE['campuses']} schools of U.S. public universities from {SAMPLE['years'][0]} to {SAMPLE['years'][1]}.",
    "- We predict your annual base salary from your rank, PhD year, publications, NBER affiliation, "
    "years at your current school, and the U.S. News score of your department. "
    "The salary does not include summer pay or other extra pay.",
    f"- We predict the salary for {SAMPLE['years'][1]} and adjust it to {YEAR} "
    "with consumer price inflation (CPI).",
    f"- We tested the model on schools that it had not seen. For half of the professors, "
    f"the prediction was within {TYPICAL_ERROR}% of their actual salary.",
    "- For associate and full professors, we also predict the chance of a large raise in a year "
    "from the raises of tenured professors at public universities outside the University of California.",
    "- Our data cover only public universities. Private universities, business schools, "
    "and schools outside the U.S. may pay differently.",
]:
    st.markdown(f'<p class="list-text">{line}</p>', unsafe_allow_html=True)

st.markdown('<p class="list-text">Disclaimer: the model is still experimental</p>', unsafe_allow_html=True)


def month_name(month):
    """'2026-10' -> 'October 2026'."""
    names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]
    return f"{names[int(month[5:]) - 1]} {month[:4]}"


def pct(log_points):
    """Percent change in salary implied by a change in log salary."""
    return 100 * (math.exp(log_points) - 1)


# Model details, with every number taken from app_model.json.
with st.expander("Model details"):
    c, jl = COEF, JUMP["jump_logit"]
    seg1, seg2 = c["top5_tenured"], c["top5_tenured"] + c["top5_tenured_above4"]
    seg3 = seg2 + c["top5_tenured_above8"]
    st.markdown(f"""
**Salary.** We regress the log of the annual base salary on the following variables, with a separate
effect for each year:

- job rank (assistant, associate, or full professor);
- career age (years since the PhD), as a cubic polynomial;
- years at the current school;
- NBER affiliation;
- the U.S. News peer assessment score of the department;
- the numbers of articles in three classes: top-5 journals, other peer-reviewed journals, and invited
  or conference papers.

Holding the other variables fixed, the model gives these differences in salary:

- each top-5 article of an associate or full professor: {pct(seg1):+.1f}% for each of the first four,
  {pct(seg2):+.1f}% for each of the next four, and {pct(seg3):+.1f}% for each article after eight;
- each top-5 article of an assistant professor: {pct(c["top5_untenured"]):+.1f}%;
- each article in another peer-reviewed journal: {pct(c["other_refereed"]):+.2f}%;
- invited or conference papers enter as log(1 + number): one paper {pct(c["invited_log1p"] * math.log(2)):+.1f}%,
  three papers {pct(c["invited_log1p"] * math.log(4)):+.1f}%;
- associate rather than assistant professor: {pct(c["tenure"]):+.1f}%; full rather than associate
  professor: {pct(c["full"]):+.1f}%;
- NBER affiliation: {pct(c["nber"]):+.1f}%;
- each year at the current school: {pct(c["years_at_school"]):+.1f}%;
- each 0.1 point of the U.S. News score: {pct(0.1 * c["score"]):+.1f}%.

These numbers are correlations in our data, not causal effects.

**Data.** We estimate the model on {SAMPLE["person_years"]:,} annual salaries of {SAMPLE["people"]:,}
professors at {SAMPLE["campuses"]} schools from {SAMPLE["years"][0]} to {SAMPLE["years"][1]}. We predict
the salary for {MODEL["base_year"]} and multiply it by {MODEL["inflation"]["factor"]:.3f}, the change in
the consumer price index (CPI-U) from {month_name(MODEL["inflation"]["from_month"])} to
{month_name(MODEL["inflation"]["to_month"])}. If an answer lies beyond the range of our data, we use the edge of the
range instead (for example, a career age of {LIMITS["career_age_max"]} years).

**Accuracy.** We estimated the model again without each school in turn and predicted the salaries of
that school in {SAMPLE["years"][1] - 1} and {SAMPLE["years"][1]}. For half of the professors, the
prediction was within {TYPICAL_ERROR}% of the actual salary, and for
{round(100 * ACCURACY["share_within_20pct"])}% of them, within 20%. The range shown with your prediction
contains the middle half of these errors.

**Large raises.** We call the raise of a professor in a year a large raise if it exceeds the typical
raise at the school in that year by more than {JUMP["threshold"]:.2f} log points (about
{round(100 * JUMP["threshold"])}% of the salary). We model each raise as either a routine raise or a jump.
The probability of a jump rises with top-5 and other peer-reviewed articles of the last two years, falls
with career age, and is higher for professors paid less than the salary model predicts. NBER members
receive larger jumps. We estimate this model on {JUMP["sample"]["raises"]:,} raises of
{JUMP["sample"]["people"]} tenured professors at public universities outside the University of
California from {JUMP["sample"]["years"][0]} to {JUMP["sample"]["years"][1]}, and we use the average
of the year effects of these years. In these data, {round(100 * JUMP["sample"]["share_large"])}% of raises are large.
""")

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
                               value=None, step=1, format="%d",
                               placeholder="Enter the year in YYYY format")
    top5 = st.number_input(
        "How many articles have you published in the top 5 journals?",
        help="American Economic Review, Econometrica, Journal of Political Economy, "
             "Quarterly Journal of Economics, and Review of Economic Studies. "
             "Count research articles only. Do not count AER: Papers and Proceedings, "
             "AER: Insights, comments, or replies.",
        min_value=0, value=0, step=1, format="%d")
    other = st.number_input(
        "How many articles have you published in other peer-reviewed journals?",
        help="Count research articles in any peer-reviewed journal other than the top 5, including AER: Insights "
             "and the American Economic Journals. Do not count comments, replies, book chapters, publications of "
             "the Federal Reserve or other agencies, policy magazines, or the invited and conference papers "
             "of the next question.",
        min_value=0, value=0, step=1, format="%d")
    invited = st.number_input(
        "How many invited or conference papers have you published?",
        help="Count surveys in the Journal of Economic Literature, the Journal of Economic Perspectives, and the "
             "Annual Reviews; papers in AEA Papers and Proceedings (including the AER May issue); and papers in "
             "Brookings Papers on Economic Activity, NBER Macroeconomics Annual, the Carnegie-Rochester "
             "Conference Series on Public Policy, and Tax Policy and the Economy. Do not count comments.",
        min_value=0, value=0, step=1, format="%d")
    recent_top5 = st.number_input(
        "How many of your top-5 articles were published during the last two years?",
        help=f"Count articles published in {YEAR - 1} or {YEAR}, in the same way as above. "
             "We use this number only for associate and full professors.",
        min_value=0, value=0, step=1, format="%d")
    recent_other = st.number_input(
        "How many of your articles in other peer-reviewed journals were published during the last two years?",
        help=f"Count articles published in {YEAR - 1} or {YEAR}, in the same way as above. "
             "We use this number only for associate and full professors.",
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
                                value=None, step=1, format="%d",
                                placeholder="Enter the year in YYYY format")
    current_salary = st.number_input(
        "What is your current annual base salary in dollars? (optional)",
        help="Enter your base salary without summer pay or other extra pay, for example 150000. "
             "We compare it with the prediction and use the difference to compute the chance of a large raise. "
             "If you leave this box blank, we use the predicted salary.",
        min_value=0, value=None, step=1000, format="%d", placeholder="Optional")
    submitted = st.form_submit_button("🔍 Compute Salary")


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def log_salary(age, top5, other, invited, nber, years, tenure, full, score):
    """Predicted log salary in the base year (formula of KT/code/analysis/app_model.py)."""
    c = COEF
    return (c["const"] + c["age"] * age + c["age2_per100"] * age**2 / 100 + c["age3_per10000"] * age**3 / 1e4
            + tenure * (c["top5_tenured"] * top5 + c["top5_tenured_above4"] * max(top5 - 4, 0)
                        + c["top5_tenured_above8"] * max(top5 - 8, 0))
            + (1 - tenure) * c["top5_untenured"] * top5 + c["other_refereed"] * other + c["invited_log1p"] * math.log1p(invited)
            + c["nber"] * nber
            + c["years_at_school"] * years + c["tenure"] * tenure + c["full"] * full + c["score"] * score)


def large_raise_prob(top5_2y, other_2y, full, career_age, years_since_hire, pay_gap, nber):
    """Chance that a raise exceeds the typical raise at the school by the threshold (formula of
    KT/code/analysis/app_model.py, with the raise-weighted average year effect)."""
    c, rt, t = JUMP["jump_logit"], JUMP["routine"], JUMP["threshold"]
    z = (c["const"] + c["top5_2y"] * top5_2y + c["other_refereed_2y"] * other_2y + c["full"] * full
         + c["career_age"] * career_age + c["years_since_hire"] * years_since_hire + c["pay_gap"] * pay_gap)
    pi = 1 / (1 + math.exp(-z))
    lam = math.exp(JUMP["jump_rate"]["const"] + JUMP["jump_rate"]["nber"] * nber)
    routine_tail = rt["bp"] / (rt["bp"] + rt["bm"]) * math.exp(-t / rt["bp"])   # asymmetric Laplace, mode 0
    return (1 - pi) * (1 - rt["tie_prob_mean"]) * routine_tail + pi * math.exp(-lam * t)


def problems():
    if phd_year is None or join_year is None or score is None:
        return "Please answer every question."
    if not PHD_YEAR_MIN <= phd_year <= YEAR:
        return f"Please enter a PhD year between {PHD_YEAR_MIN} and {YEAR}."
    if not phd_year - 1 <= join_year <= YEAR:
        return (f"Please enter the year you started at your current school between {phd_year - 1} "
                f"(the year before your PhD) and {YEAR}.")
    for value, key, what in [(top5, "top5", "top-5 articles"),
                             (other, "other", "articles in other peer-reviewed journals"),
                             (invited, "invited", "invited or conference papers"),
                             (recent_top5, "recent_top5", "top-5 articles during the last two years"),
                             (recent_other, "recent_other",
                              "articles in other peer-reviewed journals during the last two years")]:
        if value > MAX_COUNTS[key]:
            return f"Please check the number of {what}: we accept at most {MAX_COUNTS[key]}."
    if recent_top5 > top5 or recent_other > other:
        return "The articles published during the last two years cannot exceed all your articles of the same kind."
    if current_salary is not None and not SALARY_MIN <= current_salary <= SALARY_MAX:
        return (f"Please enter your annual base salary in dollars, between ${SALARY_MIN:,} and ${SALARY_MAX:,}, "
                "or leave the box blank.")
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
        log_y = log_salary(age, min(top5, LIMITS["top5_max"]), min(other, LIMITS["other_refereed_max"]),
                           min(invited, LIMITS["invited_max"]),
                           int(nber == "Yes"), years, tenure, full, min(score, SCORE_MAX))
        salary = math.exp(log_y) * MODEL["inflation"]["factor"]
        low = salary * math.exp(ACCURACY["error_quantiles"]["p25"])
        high = salary * math.exp(ACCURACY["error_quantiles"]["p75"])
        def r(x):
            return int(round(x / 1000) * 1000)
        st.success(f"💰 Your predicted base salary in {YEAR} is **${r(salary):,}**")
        st.markdown(f"Half of the professors in our tests earned within about {TYPICAL_ERROR}% of their "
                    f"prediction. For you, this range is **${r(low):,} to ${r(high):,}**.")
        pay_gap = 0.0
        if current_salary is not None:
            pay_gap = math.log(current_salary / salary)
            word = "above" if pay_gap >= 0 else "below"
            st.markdown(f"Your current salary is **{abs(round(100 * (current_salary / salary - 1)))}% {word}** "
                        "the prediction.")
        if tenure:
            prob = large_raise_prob(
                min(recent_top5, JUMP_LIMITS["top5_2y_max"]),
                min(recent_other, JUMP_LIMITS["other_refereed_2y_max"]), full,
                clamp(YEAR - phd_year, JUMP_LIMITS["career_age_min"], JUMP_LIMITS["career_age_max"]),
                clamp(YEAR - 1 - join_year, 0, JUMP_LIMITS["years_since_hire_max"]),
                clamp(pay_gap, JUMP_LIMITS["pay_gap_min"], JUMP_LIMITS["pay_gap_max"]), int(nber == "Yes"))
            shown = "less than 1%" if prob < 0.005 else f"{round(100 * prob)}%"
            st.info(f"📈 Your chance of a large raise in a year is **{shown}**.")
            st.markdown(
                f"A large raise exceeds the typical raise at your school by about "
                f"{round(100 * JUMP['threshold'])}% of your salary or more. Such raises are rare: "
                f"{round(100 * JUMP['sample']['share_large'])}% of the raises in our data. They often come with "
                "outside offers. We estimate this chance from the raises of tenured professors at public "
                "universities outside the University of California.")
        else:
            st.markdown("We predict the chance of a large raise only for associate and full professors.")
