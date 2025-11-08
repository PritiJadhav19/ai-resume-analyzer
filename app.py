import streamlit as st
import openai
import PyPDF2
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠")
st.title("🧠 AI Resume Analyzer")
st.write("Upload your resume and paste a job description to get AI feedback!")

# Upload resume
resume_file = st.file_uploader("📄 Upload Resume (PDF only)", type=["pdf"])
job_description = st.text_area("🧾 Paste Job Description")

if st.button("Analyze Resume"):
    if resume_file is not None and job_description:
        # Extract text from PDF
        reader = PyPDF2.PdfReader(resume_file)
        resume_text = ""
        for page in reader.pages:
            resume_text += page.extract_text()

        # Prepare prompt for AI
        prompt = f"""
        You are a career advisor AI.
        Compare this resume with the job description below.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Please provide:
        1. Overall match percentage (0–100%)
        2. Key skills found and missing
        3. Suggestions to improve resume relevance
        """

        # Call OpenAI API
        with st.spinner("Analyzing your resume..."):
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )

        result = response.choices[0].message.content
        st.subheader("🧩 Analysis Result")
        st.write(result)

    else:
        st.warning("Please upload a resume and paste a job description.")
