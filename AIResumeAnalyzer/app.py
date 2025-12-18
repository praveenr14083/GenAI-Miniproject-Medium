import streamlit as st
import pdfplumber
from groq import Groq
st.set_page_config(page_title="AI Resume Analyzer",layout="centered")

st.title("AI Resume Analyzer")
st.write("Upload your PDF resume and get AI-powered insights")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


if "analysis" not in st.session_state:
    st.session_state.analysis = None

def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text
def analyze_resume(resume_text):

    prompt = f"""You are an expert HR and resume analyst.
Analyze the resume below and return the result in this format:
Skills:
Strengths:
Weaknesses:
Recommended Job Roles:
Resume Improvement Suggestions:
Professional Resume Summary (120-150 words):
Resume:{resume_text}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=1200
    )

    return response.choices[0].message.content
uploaded_file = st.file_uploader("Upload your resume (PDF only)",type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting resume text..."):
        resume_text = extract_pdf_text(uploaded_file)

    if resume_text.strip() == "":
        st.error("Could not extract text from the PDF.")
    else:
        st.success("Resume text extracted successfully!")

    
        if st.button(" Analyze Resume"):
            with st.spinner("Analyzing with AI..."):
                st.session_state.analysis = analyze_resume(resume_text)
        if st.session_state.analysis:
            st.divider()
            st.subheader("AI Resume Analysis")
            st.write(st.session_state.analysis)
            col1, col2 = st.columns([2,0.5])

            with col1:
                if st.button("Regenerate"):
                    with st.spinner("Regenerating..."):
                        st.session_state.analysis = analyze_resume(resume_text)
                        st.rerun()

            with col2:
                st.download_button(
                
                    label="Download",
                    data=st.session_state.analysis,
                    file_name="AI_Resume_Analysis.txt",
                    mime="text/plain"
                )
