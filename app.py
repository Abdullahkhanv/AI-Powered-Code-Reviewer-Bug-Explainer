# ==============================
# AI Code Reviewer (Streamlit)
# ==============================

import streamlit as st
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"

# ------------------------------
# 🎨 PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="AI Code Reviewer",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Code Reviewer")
st.caption("Fix bugs. Learn faster. Code smarter 🚀")

# ------------------------------
# 🔐 API KEY INPUT
# ------------------------------
api_key = st.text_input("🔐 Enter GROQ API Key", type="password")

# ------------------------------
# 💻 INPUT SECTION
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    code = st.text_area("💻 Paste Your Code", height=300)

    language = st.selectbox(
        "🌐 Select Language",
        ["Python", "C++", "Java", "JavaScript"]
    )

    beginner_mode = st.checkbox(
        "🧑‍🎓 Explain like I'm a beginner",
        value=True
    )

    uploaded_file = st.file_uploader("📂 Upload Code File")

    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")

# ------------------------------
# 🧠 ANALYSIS FUNCTION
# ------------------------------
def analyze_code():
    if not api_key:
        st.error("❌ Please enter your GROQ API key.")
        return

    if not code.strip():
        st.warning("⚠️ Please enter some code.")
        return

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
You are an expert programming tutor and code reviewer.

Analyze the following {language} code and provide:

1. 🐞 Bugs (if any)
2. 💡 Explanation (simple and clear{" for a beginner" if beginner_mode else ""})
3. ⚡ Optimized Code
4. 📊 Time & Space Complexity (Big-O)

Make the response clean and well structured.

Code:
{code}
"""

        with st.spinner("🔍 Analyzing code..."):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}]
            )

        st.success("✅ Analysis Complete!")
        st.markdown(response.choices[0].message.content)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")


# ------------------------------
# 🚀 BUTTON
# ------------------------------
if st.button("🔍 Analyze Code"):
    analyze_code()
