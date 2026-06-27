
import streamlit as st
import ast
import json
import requests

st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")

# ============================================================
# CUSTOM CSS FOR BETTER UI
# ============================================================

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }
    .bug-card {
        background: #ffffff;
        padding: 0.8rem 1.2rem;
        border-radius: 8px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 0.6rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
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
    .stButton button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
        transition: 0.3s;
    }
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,114,255,0.3);
    }
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1rem 0;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-header">🤖 AI Code Reviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Paste your Python code and let AI analyze it for bugs, unused variables, and improvements</div>', unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/python--v1.png", width=80)
    st.markdown("### 🔑 Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Get your API key from console.groq.com")
    st.markdown("---")
    st.markdown("### 📊 How it works")
    st.markdown("""
    1. **Static Analysis** – Detects unused variables and imports.
    2. **AI Review** – Uses Groq to find bugs and suggest fixes.
    """)
    st.markdown("---")
    st.markdown("### 🛠️ Built with")
    st.markdown("• Streamlit • AST • Groq API")

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
{code}

text

Static Analysis Report:
{json.dumps(analysis_report, indent=2)}

Return your response **only** in valid JSON format with the following structure:
{{
    "summary": "Brief summary of issues",
    "bugs": [
        {{
            "line": <line_number>,
            "message": "Description of the bug",
            "severity": "high|medium|low",
            "suggestion": "Suggested fix"
        }}
    ],
    "overall_rating": "A|B|C|D|F"
}}
"""
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

col1, col2 = st.columns([3, 1])

with col1:
    code_input = st.text_area("📄 Paste your Python code here:", height=350, value="""
import os
import sys

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    return average

def process_data(data):
    if data:
        print("Processing...")
    # Missing else clause

def unused_function():
    x = 10
    print("This function is never called")
""")

with col2:
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔍 Review Code", use_container_width=True):
        if not groq_api_key:
            st.error("Please enter your Groq API key in the sidebar.")
        elif not code_input.strip():
            st.warning("Please paste some code to review.")
        else:
            with st.spinner("Analyzing code..."):
                analysis_report = analyze_code(code_input)
                if "error" in analysis_report:
                    st.error(f"Static analysis error: {analysis_report['error']}")
                else:
                    st.subheader("📊 Static Analysis Report")
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Unused Variables", len(analysis_report["unused_variables"]))
                    col_b.metric("Unused Imports", len(analysis_report["unused_imports"]))
                    col_c.metric("Total Issues", analysis_report["issues_count"])
                    
                    with st.expander("View Full Static Analysis"):
                        st.json(analysis_report)
                    
                    try:
                        with st.spinner("Getting AI review..."):
                            ai_review_json = review_code_with_ai(code_input, analysis_report, groq_api_key)
                            ai_review = json.loads(ai_review_json)
                        
                        st.subheader("🤖 AI Review")
                        st.info(f"**Summary:** {ai_review.get('summary', 'N/A')}")
                        st.metric("Overall Rating", ai_review.get('overall_rating', 'N/A'))
                        
                        if "bugs" in ai_review and ai_review["bugs"]:
                            st.subheader("🐞 Bugs Found")
                            for bug in ai_review["bugs"]:
                                severity = bug.get("severity", "").lower()
                                css_class = "bug-card"
                                if severity == "low":
                                    css_class += " bug-card-low"
                                elif severity == "medium":
                                    css_class += " bug-card-medium"
                                elif severity == "high":
                                    css_class += " bug-card-high"
                                
                                st.markdown(f"""
                                <div class="{css_class}">
                                    <strong>Line {bug.get('line', '?')}</strong> • <span style="text-transform:uppercase;font-size:0.8rem;color:#666;">{severity}</span><br>
                                    {bug.get('message', 'N/A')}<br>
                                    <span style="color:#0072ff;font-size:0.9rem;">💡 {bug.get('suggestion', 'N/A')}</span>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.success("🎉 No bugs found! Your code looks clean.")
                            
                    except Exception as e:
                        st.error(f"AI Review failed: {e}")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    Built with ❤️ using Streamlit • AST • Groq API<br>
    AI Code Reviewer v2.0
</div>
""", unsafe_allow_html=True)
