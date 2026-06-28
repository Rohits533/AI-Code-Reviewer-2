import streamlit as st
import ast
import json
import requests

st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background: #0f1117;
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
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
    .metric-card {
        background: #1e1e2e;
        padding: 1.2rem 1rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #2a2a3e;
        transition: 0.25s ease;
    }
    .metric-card:hover {
        border-color: #00d4ff;
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 212, 255, 0.1);
    }
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        color: #00d4ff;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #888;
        margin-top: 0.2rem;
    }
    .bug-card {
        background: #1e1e2e;
        padding: 0.9rem 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 0.7rem;
        border: 1px solid #2a2a3e;
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
    .bug-severity {
        font-size: 0.7rem;
        text-transform: uppercase;
        font-weight: 600;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        margin-left: 0.5rem;
    }
    .bug-severity-high { background: #ffebee; color: #c62828; }
    .bug-severity-medium { background: #fff8e1; color: #f57f17; }
    .bug-severity-low { background: #e8f5e9; color: #2e7d32; }
    .bug-suggestion {
        font-size: 0.9rem;
        color: #00d4ff;
        font-weight: 500;
    }
    .rating-badge {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 0.5rem 1.5rem;
        border-radius: 12px;
        display: inline-block;
        background: #1e1e2e;
        border: 1px solid #2a2a3e;
    }
    .rating-A { color: #00c853; }
    .rating-B { color: #00d4ff; }
    .rating-C { color: #ffb300; }
    .rating-D { color: #ff6b6b; }
    .rating-F { color: #d32f2f; }
    .footer {
        text-align: center;
        color: #444;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid #1e1e2e;
    }
    .footer a {
        color: #00d4ff;
        text-decoration: none;
    }
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #7b2ff7 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 14px rgba(0, 212, 255, 0.3);
    }
    .stTextArea textarea {
        background: #1e1e2e !important;
        color: #cdd6f4 !important;
        border: 1px solid #2a2a3e !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.2) !important;
    }
    .sidebar-content {
        padding: 1rem 0;
    }
    .sidebar-content .section-title {
        color: #cdd6f4;
        font-weight: 600;
        margin-top: 1rem;
    }
    .sidebar-content ul {
        color: #888;
        padding-left: 1.2rem;
    }
    .sidebar-content ul li {
        margin: 0.4rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-header">🧠 AI Code Reviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Paste your Python code and get a professional review with static analysis + AI-powered feedback</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/python.png", width=80)
    st.markdown("---")
    st.markdown("### ⚙️ How It Works")
    st.markdown("""
    1. **Static Analysis** – Detects unused variables & imports  
    2. **AI Review** – Finds bugs, security issues & improvements  
    3. **Structured Report** – Clear, actionable feedback with severity ratings
    """)
    st.markdown("---")
    st.markdown("### 🔐 Security")
    st.markdown("✅ Your code is **not stored**  \n✅ API key is securely stored in Streamlit Secrets")
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.markdown(f"**Total Issues Found:** 0 (pending review)")

# ============================================================
# API KEY FROM SECRETS
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
    
    prompt = (
        "You are a senior code reviewer. Review the following Python code and the static analysis report.\n\n"
        "Code:\n```\n" + code + "\n```\n\n"
        "Static Analysis Report:\n" + json.dumps(analysis_report, indent=2) + "\n\n"
        "Return your response only in valid JSON format with this structure:\n"
        '{"summary": "Brief summary", "bugs": [{"line": 1, "message": "Bug description", "severity": "high|medium|low", "suggestion": "Fix"}], "overall_rating": "A|B|C|D|F"}'
    )
    
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You are a senior code reviewer. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['choices'][0]['message']['content']

# ============================================================
# MAIN UI
# ============================================================

col_left, col_right = st.columns([3, 1])

with col_left:
    code_input = st.text_area(
        "📄 Paste your Python code here:",
        height=350,
        value='''def calculate_average(numbers):
    total = 0
    for n in numbers:
        total = total + n
    return total / len(numbers)''',
        help="Paste your Python code and click 'Review' to analyze it."
    )

with col_right:
    st.markdown("### ⚡ Quick Actions")
    review_btn = st.button("🔍 Review Code", use_container_width=True)
    st.markdown("---")
    st.markdown("### 📌 Tips")
    st.markdown("""
    ✅ Works best with Python  
    ✅ Paste any code snippet  
    ✅ Gets static + AI review  
    """)

# ============================================================
# REVIEW LOGIC
# ============================================================

if review_btn:
    if not code_input.strip():
        st.warning("⚠️ Please paste some code to review.")
    else:
        with st.spinner("🔍 Analyzing code..."):
            analysis_report = analyze_code(code_input)
            if "error" in analysis_report:
                st.error(f"Static analysis error: {analysis_report['error']}")
            else:
                # --- Static Analysis Results ---
                st.markdown("---")
                st.subheader("📊 Static Analysis Report")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-number">{len(analysis_report['unused_variables'])}</div>
                        <div class="metric-label">🔹 Unused Variables</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-number">{len(analysis_report['unused_imports'])}</div>
                        <div class="metric-label">📦 Unused Imports</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-number">{analysis_report['issues_count']}</div>
                        <div class="metric-label">⚠️ Total Issues</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with st.expander("📋 View Full Static Analysis"):
                    st.json(analysis_report)
                
                # --- AI Review ---
                try:
                    with st.spinner("🤖 Getting AI review..."):
                        ai_review_json = review_code_with_ai(code_input, analysis_report, groq_api_key)
                        ai_review = json.loads(ai_review_json)
                    
                    st.markdown("---")
                    st.subheader("🤖 AI Review")
                    
                    # Summary
                    st.info(f"**Summary:** {ai_review.get('summary', 'N/A')}")
                    
                    # Rating
                    rating = ai_review.get('overall_rating', 'N/A')
                    rating_class = f"rating-{rating}" if rating in ['A', 'B', 'C', 'D', 'F'] else ""
                    st.markdown(f"""
                    <div style="text-align:center; margin: 1rem 0;">
                        <span class="rating-badge {rating_class}">Overall Rating: {rating}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Bugs
                    bugs = ai_review.get("bugs", [])
                    if bugs:
                        st.markdown("#### 🐞 Issues Found")
                        for bug in bugs:
                            severity = bug.get("severity", "low")
                            severity_class = f"bug-severity-{severity}"
                            css_class = f"bug-card bug-card-{severity}"
                            
                            st.markdown(f"""
                            <div class="{css_class}">
                                <span style="font-weight:600;">Line {bug.get('line', '?')}</span>
                                <span class="bug-severity {severity_class}">{severity}</span>
                                <div style="margin: 0.3rem 0; color: #cdd6f4;">{bug.get('message', 'N/A')}</div>
                                <div class="bug-suggestion">💡 {bug.get('suggestion', 'N/A')}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.success("🎉 No bugs found! Your code looks clean.")
                    
                except Exception as e:
                    st.error(f"❌ AI Review failed: {e}")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit • AST • Groq API<br>
    <a href="https://github.com/Rohits533/AI-Code-Reviewer-2" target="_blank">View on GitHub</a>
</div>
""", unsafe_allow_html=True)
