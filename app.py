import streamlit as st
import openai
import os
import time
from dotenv import load_dotenv
import graphviz

# Load OpenAI key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Code Review Assistant", layout="centered")
st.title("🧠 Code Review Assistant")
st.markdown("Paste your code below and get suggestions, a flowchart, and step-by-step animations!")

# Input options
language = st.selectbox("Select language", ["Python", "JavaScript", "Java", "C++", "Other"])
code_input = st.text_area("✏️ Paste your code here", height=300)

if st.button("🔍 Review My Code"):
    if not code_input.strip():
        st.warning("Please paste some code before submitting.")
    else:
        with st.spinner("Analyzing your code..."):
            # AI prompt
            prompt = f"""
You are an expert software engineer. Review the following {language} code and:
1. Suggest improvements
2. Explain each suggestion
3. Point out any bugs or inefficiencies
4. Provide an improved version
5. Describe a flowchart in dot (Graphviz) language
6. Explain how the code executes, step-by-step

Code:
{code_input}
"""
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            content = response.choices[0].message.content

        # Parse sections
        try:
            improved_code = content.split("```")[1]
        except:
            improved_code = "Improved code not found."

        # Display results
        st.success("✅ Review complete!")
        st.markdown("### 🔧 Suggestions & Explanations")
        st.markdown(content)

        # Option to show improved code
        if st.button("✨ Show Improved Code"):
            st.code(improved_code, language=language.lower())

        # Extract and render flowchart
        st.markdown("### 📈 Code Flowchart")
        try:
            dot_section = [block for block in content.split("```") if "digraph]()_
