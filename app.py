# ==============================
# AI Code Reviewer & Bug Explainer
# ==============================

import os
import gradio as gr
from groq import Groq

# ------------------------------
# 🔑 SET YOUR API KEY HERE
# ------------------------------
# Option 1 (recommended in Colab):
# import os
# os.environ["GROQ_API_KEY"] = "your_api_key_here"

# Option 2:
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY is not set. Please add it as an environment variable.")

client = Groq(api_key=api_key)
# ------------------------------
# 🧠 AI FUNCTION
# ------------------------------
def analyze_code(code, language, beginner_mode):
    if not code.strip():
        return "⚠️ Please enter some code first."

    # Prompt engineering (important part)
    prompt = f"""
You are an expert programming tutor and code reviewer.

Analyze the following {language} code and provide:

1. 🐞 Bugs (if any)
2. 💡 Explanation (simple and clear{" for a beginner" if beginner_mode else ""})
3. ⚡ Optimized Code
4. 📊 Time & Space Complexity (Big-O)

Code:
{code}

Make the response well-structured with headings.
"""

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ------------------------------
# 📂 FILE HANDLER
# ------------------------------
def handle_file(file):
    if file is None:
        return ""
    try:
        with open(file.name, "r") as f:
            return f.read()
    except:
        return "❌ Could not read file."


# ------------------------------
# 🎨 GRADIO UI (Gen Z Style)
# ------------------------------
with gr.Blocks(theme=gr.themes.Soft()) as app:

    gr.Markdown(
        """
        # 🤖 AI Code Reviewer
        ### Fix bugs. Learn faster. Code smarter 🚀
        """
    )

    with gr.Row():
        with gr.Column():
            code_input = gr.Textbox(
                label="💻 Paste Your Code",
                lines=15,
                placeholder="Paste your code here..."
            )

            file_upload = gr.File(label="📂 Or Upload Code File")

            language = gr.Dropdown(
                ["Python", "C++", "Java", "JavaScript"],
                label="🌐 Select Language",
                value="Python"
            )

            beginner_mode = gr.Checkbox(
                label="🧑‍🎓 Explain like I'm a beginner",
                value=True
            )

            analyze_btn = gr.Button("🔍 Analyze Code")

        with gr.Column():
            output = gr.Markdown(label="📊 AI Analysis")

    # ------------------------------
    # 🔗 CONNECTIONS
    # ------------------------------
    file_upload.change(
        fn=handle_file,
        inputs=file_upload,
        outputs=code_input
    )

    analyze_btn.click(
        fn=analyze_code,
        inputs=[code_input, language, beginner_mode],
        outputs=output
    )

# ------------------------------
# ▶️ RUN APP
# ------------------------------
app.launch(debug=True)
