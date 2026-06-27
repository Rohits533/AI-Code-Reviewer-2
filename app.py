import streamlit as st
import ast
import json
import requests

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
# STREAMLIT UI
# ============================================================

st.set_page_config(page_title="AI Code Reviewer", layout="wide")
st.title("🤖 AI Code Reviewer & Debugger")
st.markdown("Paste your Python code below, and the AI will analyze it for bugs, unused variables, and more.")

with st.sidebar:
    st.header("🔑 Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Get your API key from console.groq.com")
    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("1. **Static Analysis** – Detects unused variables and imports.")
    st.markdown("2. **AI Review** – Uses Groq to find bugs and suggest fixes.")

code_input = st.text_area("📄 Paste your Python code here:", height=300, value="""
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

if st.button("🔍 Review Code"):
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
                col1, col2, col3 = st.columns(3)
                col1.metric("Unused Variables", len(analysis_report["unused_variables"]))
                col2.metric("Unused Imports", len(analysis_report["unused_imports"]))
                col3.metric("Total Issues", analysis_report["issues_count"])
                
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
                            severity_color = {
                                "high": "🔴",
                                "medium": "🟡",
                                "low": "🟢"
                            }.get(bug.get("severity", "").lower(), "⚪")
                            st.markdown(f"{severity_color} **Line {bug.get('line', '?')}:** {bug.get('message', 'N/A')}")
                            st.markdown(f"   💡 **Suggestion:** {bug.get('suggestion', 'N/A')}")
                    else:
                        st.success("🎉 No bugs found! Your code looks clean.")
                        
                except Exception as e:
                    st.error(f"AI Review failed: {e}")
                    
