import streamlit as st
import math

from supabase import create_client, Client

SUPABASE_URL = "https://auqqsiljywsnqghtechh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1cXFzaWxqeXdzbnFnaHRlY2hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjEwMzAsImV4cCI6MjA2MDI5NzAzMH0.jaDhkMMokUoBIOep1x2gUvdo5kVNzLcd6P_LZbQm8f4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if "already_logged" not in st.session_state:
    supabase.table("visits").insert({}).execute()
    st.session_state["already_logged"] = True

res = supabase.table("visits").select("id", count="exact").execute()
visits = res.count

def compute_y(Theory, Econometrics, TPhD, THired, N_pub, N_top5, Tenure, Full, USNews):
    log_y = 11.8184 - 0.011855 * Theory + 0.028621 * Econometrics \
    + 0.025465 * TPhD - 0.00035786 * TPhD**2 - 0.021768 * THired + 0.00029833 * THired**2 \
    + 0.0015756 * (N_pub - N_top5) + 0.024981 * N_top5 \
    + 0.11574 * Tenure + 0.14999 * Full + 0.04377 * USNews + 0.068116 * (max(USNews - 3,0))**2
    return int(round(1.029*math.exp(log_y)))

st.set_page_config(page_title="Econ Salary", page_icon="📈", layout="centered")

st.title("Predicting Salaries of Economics Professors in the United States")

st.markdown(f"#### 👥 Total Visitors: `{visits}`")


st.markdown("""<style> ... </style>""", unsafe_allow_html=True) 

st.markdown('<p class="highlight-text">Developed by:</p>', unsafe_allow_html=True)

st.markdown('<p class="main-title">Enter your values below and click Compute Salary.</p>', unsafe_allow_html=True)

with st.container():
    TPhD = st.number_input("How many years ago did you finish PhD?", min_value=0, step=1, format="%d")
    THired = st.number_input("How many years have you been working at your current institution?", min_value=0, step=1, format="%d")
    Theory = st.radio("Is your research mainly about theoretical analysis of economic models? Choose Yes (1) or No (0).", [0, 1])
    Econometrics = st.radio("Is your research mainly about econometrics or statistics? Choose Yes (1) or No (0).", [0, 1])
    N_pub = st.number_input("How many papers have you published?...", min_value=0, step=1, format="%d")
    N_top5 = st.number_input("How many papers have you published in so-called 'Top 5' economics journals?", min_value=0, step=1, format="%d")
    Tenure = st.radio("Do you have tenure? Choose Yes (1) or No (0).", [0, 1])
    Full = st.radio("Are you a full professor? Choose Yes (1) or No (0).", [0, 1])
    USNews = st.number_input("What is the [US News Peer Assessment Score](https://www.usnews.com...)", min_value = 1.0, max_value = 5.0, value = "min", step = 0.1, format="%0.1f")

if st.button("🔍 Compute Salary"):
    salary = compute_y(Theory, Econometrics, TPhD, THired, N_pub, N_top5, Tenure, Full, USNews)
    st.success(f"💰 Your expected salary in 2024 is **${salary:,}**")
