import streamlit as st
import ast
import json
import requests

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS (Properly Escaped)
# ============================================================

st.markdown("""
<style>
    /* Main header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0 0.5rem 0;
    }
    .sub-header {
        text-align: center;
        font-size: 1.1rem;
        color: #888;
        margin-bottom: 2rem;
    }
    /* Metric cards */
    .metric-card {
        background: #f8f9fa;
        padding: 1.2rem 1rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #eee;
        transition: 0.25s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.06);
        border-color: #667eea;
    }
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1a1a1a;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        margin-top: 0.2rem;
    }
    /* Bug cards */
    .bug-card {
        background: #ffffff;
        padding: 0.9rem 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 0.7rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: 0.2s;
    }
    .bug-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.06);
    }
    .bug-card-low {
        border-left-color: #00c853;
    }
    .bug-card-medium {
        border-left-color: #ffb300;
    }
    .bug-card-high {
        border-left-color: #d32f2f;
    }
    .bug-line {
        font-weight: 600;
        color: #333;
    }
    .bug-severity {
        font-size: 0.7rem;
        text-transform: uppercase;
        font-weight: 600;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        background: #f0f0f0;
        color: #666;
        margin-left: 0.5rem;
    }
    .bug-severity-high { background: #ffebee; color: #c62828; }
    .bug-severity-medium { background: #fff8e1; color: #f57f17; }
    .bug-severity-low { background: #e8f5e9; color: #2e7d32; }
    .bug-message {
        margin: 0.3rem 0;
        color: #444;
    }
    .bug-suggestion {
        font-size: 0.9rem;
        color: #667eea;
        font-weight: 500;
    }
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: scale(1.01);
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #f0f0f0;
    }
    .footer a {
        color: #667eea;
        text-decoration: none;
    }
    /* Rating badge */
    .rating-badge {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 0.5rem 1.5rem;
        border-radius: 12px;
        display: inline-block;
        background: #f0f0f0;
        color: #333;
    }
    .rating-A { background: #e8f5e9; color: #2e7d32; }
    .rating-B { background: #e3f2fd; color: #0d47a1; }
    .rating-C { background: #fff8e1; color: #f57f17; }
    .rating-D { background: #ffebee; color: #c62828; }
    .rating-F { background: #ffebee; color: #b71c1c; }
    .severity-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }
    .dot-high { background: #d32f2f; }
    .dot-medium { background: #ffb300; }
    .dot-low { background: #00c853; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-header">🤖 AI Code Reviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Paste any code — get a professional senior developer review</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR — Instructions
# ============================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/python.png", width=70)
    st.markdown("### ⚙️ Review Settings")
    
    language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "Java", "C++", "Go", "Rust"],
        index=0
    )
    
    review_focus = st.selectbox(
        "Review Focus",
        ["Full Review", "Bugs & Security", "Performance", "Code Style", "Documentation"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 📊 How it works")
    st.markdown("""
    1. **Static Analysis** – Detects unused variables & imports  
    2. **AI Review** – Finds bugs, security issues & improvements  
    3. **Structured Report** – Clear, actionable feedback
    """)
    st.markdown("---")
    st.markdown("### 🔐 Security")
    st.markdown("Your code is **not stored**. API key is securely stored in Streamlit Secrets.")

# ============================================================
# GET API KEY FROM SECRETS
# ============================================================

try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("🚨 GROQ_API_KEY not found in Streamlit Secrets. Please add it in the app settings.")
    st.stop()

# ============================================================
# STATIC ANALYSIS ENGINE
# ============================================================

def analyze_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"Syntax Error: {e}"}

    report = {
        "unused_variables": [],
        "unused_imports": [],
        "issues_count": 0,
    }

    assigned = set()
    used = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned.add(target.id)
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                used.add(node.id)
    unused_vars = assigned - used
    report["unused_variables"] = list(unused_vars)

    imported = set()
    used_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                used_names.add(node.id)
    unused_imports = imported - used_names
    report["unused_imports"] = list(unused_imports)

    report["issues_count"] = len(report["unused_variables"]) + len(report["unused_imports"])
    return report

# ============================================================
# AI REVIEW ENGINE
# ============================================================

def review_code_with_ai(code, analysis_report, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""
You are a senior code reviewer. Review the following Python code and the static analysis report.

Code:
