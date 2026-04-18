import streamlit as st
import math
from supabase import create_client, Client

st.set_page_config(page_title="Econ Salary", page_icon="📈", layout="centered")

SUPABASE_URL = "https://auqqsiljywsnqghtechh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImF1cXFzaWxqeXdzbnFnaHRlY2hoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ3MjEwMzAsImV4cCI6MjA2MDI5NzAzMH0.jaDhkMMokUoBIOep1x2gUvdo5kVNzLcd6P_LZbQm8f4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

if "already_logged" not in st.session_state:
    try:
        supabase.table("visits").insert({}).execute()
    except Exception as e:
        st.warning("Visitor logging failed.")
    st.session_state["already_logged"] = True

res = supabase.table("visits").select("id", count="exact").execute()
visits = res.count

st.title("Predicting Salaries of Economics Professors in the United States")
st.markdown(f"#### 👥 Total Visitors: {visits}")

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

st.markdown('<p class="highlight-text">The prediction is based on the following parameters (R-squared 71%):</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- Education</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- Employment</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- Field</p>', unsafe_allow_html=True)
st.markdown('<p class="list-text">- Publications</p>', unsafe_allow_html=True)

# st.markdown('<p class="highlight-text">The predictive model is an extension of <a href="https://econjwatch.org/articles/publications-citations-position-and-compensation-of-economics-professors">Lyu and Toda (2019)</a></p>', unsafe_allow_html=True)
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
    </style>
""", unsafe_allow_html=True)


st.markdown('<p class="main-title">Enter your values below and click Compute Salary.</p>', unsafe_allow_html=True)

with st.container():
    TPhD = st.number_input("How many years ago did you finish PhD?", min_value=0, step=1, max_value = 50, format="%d")
    region = st.selectbox("Where did you get your undergraduate degree?",
                         ["North America (Canada and U.S.)","Europe","Latin America (Mexico, Central & South America)","Other"])
    PhD = st.selectbox("Where did you get your PhD from?",
                        ["Columbia University",
                         "Harvard University",
                         "Massachusetts Institute of Technology",
                         "Northwestern University",
                         "Princeton University",
                         "Stanford University",
                         "University of California, Berkeley",
                         "University of Chicago",
                         "University of Michigan",
                         "University of Minnesota",
                         "University of Pennsylvania",
                         "University of Wisconsin, Madison",
                         "Yale University",
                         "Other"])
    field = st.selectbox("What is your field?",
                         ["Economic Theory","Econometrics","Other"])
    # top 5 journals
    npubtop5 = st.number_input("""How many papers have you published in the following journals? American Economic Review (exclude AEA P&P),
        Econometrica, Journal of Political Economy, Quarterly Journal of Economics, Review of Economic Studies.""", min_value=0, step=1, format="%d")
    # Alist top journals
    npubAlist = st.number_input("""How many papers have you published in the following journals? 
    American Journal of Health Economics, Explorations in Economic History, 
    Games and Economic Behavior, Health Economics, 
    Journal of the Association of Environmental and Resource Economists, 
    Journal of Business and Economic Statistics, Journal of Development Econnomics, 
    Journal of Environmental Economics and Management, Journal of Economic Growth, 
    Journal of Economic History, Journal of Economic Theory, Journal of Finance, 
    Journal of Financial Economics, Journal of Health Economics, Journal of Human Resources, 
    Journal of Industrial Economics, Journal of International Economics, 
    Journal of Money, Credit, and Banking, Journal of Monetary Economics, Journal of Econometrics, 
    Journal of Labor Econmics, Journal of Public Economics, Journal of Urban Economics, 
    Marketing Science, Management Science, Public Choice, RAND Journal of Economics, Theoretical Economics.""",
        min_value=0, step=1, format="%d")
    # top non-econ journals
    npubnonecon = st.number_input("""How many papers have you published in the following journals? 
    Nature, Science, PNAS, JAMA, NEJM, Lancet, 
    American Political Science Review, American Journal of Political Science, Journal of Politics, 
    American Journal of Sociology, American Sociological Review, Demography, 
    Academy of Management Journal, Academy of Management Review, Journal of Management.""",
        min_value=0, step=1, format="%d")
    
    rank = st.selectbox("What is your job rank?",
                        ["Assistant Professor", "Associate Professor", "Full Professor"])
    #USNews = st.number_input("What is the [US News Peer Assessment Score](https://www.usnews.com/best-graduate-schools/top-humanities-schools/economics-rankings) of your department? Enter 1.0 if your school is not listed.", min_value = 1.0, max_value = 5.0, value = "min", step = 0.1, format="%0.1f")

# mapping logic for undergraduate region
def get_region_variables(region_string):
    region_map = {
        "North America":         [1, 0, 0],
        "Europe":                [0, 1, 0],
        "Latin America":         [0, 0, 1]
    }
    # Return the vector if found, otherwise return a vector of all zeros
    return region_map.get(region_string, [0] * 3)

# mapping logic for PhD institution
def get_PhD_variables(PhD_string):
    # Map school names to their respective binary vectors
    phd_map = {
        "Columbia University":                  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Harvard University":                   [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Massachusetts Institute of Technology": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Northwestern University":              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Princeton University":                 [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        "Stanford University":                  [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        "University of California, Berkeley":   [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        "University of Chicago":                [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        "University of Michigan":               [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        "University of Minnesota":              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "University of Pennsylvania":           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        "University of Wisconsin, Madison":     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        "Yale University":                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
    }
    
    # Return the vector if found, otherwise return a vector of all zeros
    return phd_map.get(PhD_string, [0] * 13)

# mapping logic for field
def get_field_variables(field_string):
    if field_string == "Economic Theory":
        return 1, 0
    elif field_string == "Econometrics":
        return 0, 1
    return 0, 0

# mapping logic for job rank
def get_rank_variables(rank_string):
    if rank_string == "Assistant Professor":
        return 0, 0  # Tenure=0, Full=0
    elif rank_string == "Associate Professor":
        return 1, 0  # Tenure=1, Full=0
    elif rank_string == "Full Professor":
        return 1, 1  # Tenure=1, Full=1
    return 0, 0

# regression coefficients of region fixed effects
b_region = [x / 100 for x in [1.8055, 2.2216, 5.3901]]

# regression coefficients of PhD institution fixed effects
b_PhD = [x / 100 for x in [0.2449, 5.0381, 2.0904, 7.6036, -1.9453, 3.9239, 0.2782, 1.6398, -0.3535, 2.9533, -4.1081, 3.1088, 4.4463]]

# function to compute salary
def compute_y(TPhD, region_vec, phd_vec, Theory, Econometrics, npubtop5, npubAlist, npubnonecon, Tenure, Full):
    # pre-compute inner product
    region_impact = sum(x * coef for x, coef in zip(b_region, region_vec))
    phd_impact = sum(x * coef for x, coef in zip(b_PhD, phd_vec))
    log_y = (12.0258 - 0.008607 * TPhD + 0.000109 * TPhD**2 + region_impact + phd_impact
    - 0.017493 * Theory + 0.016830 * Econometrics
    + 0.056209 * npubtop5 + 0.006409 * npubAlist + 0.004529 * npubnonecon - 0.000845 * TPhD * npubtop5
    + 0.2129 * Tenure + 0.2513 * Full)
    return int(round(1.029*1.027*math.exp(log_y)/1000)*1000)

if st.button("🔍 Compute Salary"):
    # Convert categorical rank to the binary variables the model needs
    region_vec = get_region_variables(region)
    phd_vec = get_PhD_variables(PhD)
    Theory, Econometrics = get_field_variables(field)
    Tenure, Full = get_rank_variables(rank)
    salary = compute_y(TPhD, region_vec, phd_vec, Theory, Econometrics, npubtop5, npubAlist, npubnonecon, Tenure, Full)
    st.success(f"💰 Your expected salary in 2025 is **${salary:,}**")
