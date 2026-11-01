"""Read-only Stage 1 dashboard."""
import sqlite3
import pandas as pd
import streamlit as st
from common import DATA, REPORTS, read_json

st.set_page_config(page_title="Stage 1: ETL and EDA", layout="wide")

# Custom styling: Blue (#015cbf) & Yellow (#fed600) with centered headings
st.markdown("""
<style>
    /* Hide Streamlit 3-dot hamburger menu, toolbar, and footer */
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }
    header [data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    [data-testid="stDecoration"] {
        visibility: hidden !important;
        display: none !important;
    }
    footer {
        visibility: hidden !important;
        display: none !important;
    }

    /* Centered headings */
    h1, h2, h3, h4, h5, h6 {
        text-align: center !important;
    }
    .caption-text {
        text-align: center !important;
        color: #475569;
        font-size: 1.05rem;
        margin-top: -6px;
        margin-bottom: 24px;
    }

    /* Main Title Styling with Yellow Accent Bar */
    h1 {
        color: #015cbf !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
        padding-bottom: 12px;
        border-bottom: 4px solid #fed600;
        max-width: 900px;
        margin: 0 auto 10px auto !important;
    }

    /* Subheadings in Blue */
    h2, h3, h4 {
        color: #015cbf !important;
        font-weight: 700 !important;
        margin-top: 24px !important;
        margin-bottom: 14px !important;
    }

    /* Metric Card Styling with Blue & Yellow Accents (Flat, No Gradients) */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #fed600;
        border-left: 4px solid #015cbf;
        padding: 14px 20px;
        border-radius: 8px;
    }
    [data-testid="stMetricValue"] {
        color: #015cbf !important;
        font-weight: 800;
        font-size: 2.1rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #1e293b !important;
        font-weight: 600;
        font-size: 1rem !important;
    }

    /* Expander header styling */
    .streamlit-expanderHeader {
        background-color: #f8fafc !important;
        color: #015cbf !important;
        font-weight: 600 !important;
        border-left: 3px solid #fed600 !important;
        border-radius: 6px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Stage 1: Python Dataset ETL and Analysis")
st.markdown('<p class="caption-text">API extraction, validation, database loading and dataset verification</p>', unsafe_allow_html=True)

if not (DATA / "code_similarity.db").exists():
    st.info("Run Days 1-6 from the README to generate your dataset and reports.")
else:
    with sqlite3.connect(f"file:{(DATA / 'code_similarity.db').as_posix()}?mode=ro", uri=True) as conn:
        counts = pd.read_sql_query("SELECT COUNT(*) AS solutions, COUNT(DISTINCT problem_id) AS problems FROM solutions", conn).iloc[0]
        summaries = pd.read_sql_query("SELECT solution_id, problem_id, difficulty, lines, token_count, node_count FROM solutions LIMIT 500", conn)
        runs = pd.read_sql_query("SELECT * FROM pipeline_runs", conn)

    a, b = st.columns(2)
    a.metric("Loaded solutions", f"{int(counts.solutions):,}")
    b.metric("Problems", f"{int(counts.problems):,}")

    st.write("")
    st.subheader("Solution features (up to 500 rows)")
    st.dataframe(summaries, hide_index=True, use_container_width=True)

    with st.expander("Pipeline runs"):
        st.dataframe(runs, hide_index=True, use_container_width=True)

for name in ["quality", "stage1_gate"]:
    if (REPORTS / f"{name}.json").exists():
        with st.expander(name.replace("_", " ").title()):
            st.json(read_json(REPORTS / f"{name}.json"))

if (REPORTS / "eda.png").exists():
    st.image(str(REPORTS / "eda.png"), caption="Dataset analysis", use_container_width=True)

if (REPORTS / "eda.md").exists():
    st.markdown((REPORTS / "eda.md").read_text(encoding="utf-8"))
