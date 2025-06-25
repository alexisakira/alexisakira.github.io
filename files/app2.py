import streamlit as st
import math
import time
import httpx
from supabase import create_client, Client
from postgrest.exceptions import APIError

st.set_page_config(page_title="Econ Salary", page_icon="📈", layout="centered")

SUPABASE_URL = "https://auqqsiljywsnqghtechh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1cXFzaWxqeXdzbnFnaHRlY2hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjEwMzAsImV4cCI6MjA2MDI5NzAzMH0.jaDhkMMokUoBIOep1x2gUvdo5kVNzLcd6P_LZbQm8f4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def _call(fn, tries=3, pause=1):
    for i in range(tries):
        try:
            return fn()
        except (httpx.ConnectError, APIError):
            if i == tries - 1:
                raise
            time.sleep(pause)

if "already_logged" not in st.session_state:
    try:
        _call(lambda: supabase.table("visits").insert({}).execute())
    except Exception:
        st.warning("Visitor logging failed.")
    st.session_state["already_logged"] = True

try:
    res = _call(lambda: supabase.table("visits").select("id", count="exact").execute())
    visits = res.count
except Exception:
    visits = "N/A"

st.title("Predicting Salaries of Economics Professors in the United States")
st.markdown(f"#### 👥 Total Visitors: `{visits}`")

def compute_y(Theory, Econometrics, TPhD, THired, N_pub, N_top5, Tenure, Full, USNews):
    log_y = 11.8583 - 0.0026605 * Theory + 0.030356 * Econometrics \
    + 0.023127 * TPhD - 0.0002489 * TPhD**2 - 0.02081 * THired + 0.00027308 * THired**2 \
    + 0.0014252 * (N_pub - N_top5) + 0.042406 * N_top5 - 0.00064717 * TPhD * N_top5\
    +
