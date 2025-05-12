import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load OpenAI key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Code Review Assistant", layout="centered")

st.title("🧠 Code Review Assistant")
st.markdown("Paste your code below and get suggestions + explanations!")

language = st.selectbox("Select language", ["Python", "JavaScript", "Java", "C++", "Other"])
code_input = st.text_area("✏️ Paste your code here", height=300)

if st.button("🔍 Review My Code"):
    if not code_input.strip():
        st.warning("Please paste some code before submitting.")
    else:
        with st.spinner("Analyzing your code..."):
            prompt = f"""
You are an expert software engineer. Review the following {language} code and:
1. Suggest improvements
2. Explain each suggestion
3. Point out any bugs or inefficiencies

Code:
{code_input}
"""
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            feedback = response.choices[0].message.content
            st.success("✅ Review complete!")
            st.markdown("### 🔧 Suggestions & Explanations")
            st.markdown(feedback)
