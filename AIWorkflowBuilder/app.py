import streamlit as st
import json
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API"])

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Workflow Builder", layout="wide")

st.title("🤖 AI Workflow Builder")

# ---------------- SESSION STATE ----------------
if "text" not in st.session_state:
    st.session_state.text = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "translation" not in st.session_state:
    st.session_state.translation = ""
if "key_points" not in st.session_state:
    st.session_state.key_points = []


# ---------------- AI FUNCTION ----------------
def groq_ai(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_completion_tokens=800,
    )
    return response.choices[0].message.content


# ---------------- STEP 1: FILE UPLOAD ----------------
st.header("Step 1️⃣ Upload File")

uploaded_file = st.file_uploader("Upload a text file (.txt)", type=["txt"])

if uploaded_file:
    st.session_state.text = uploaded_file.read().decode("utf-8")
    st.success("✅ File uploaded successfully")

# ---------------- STEP 2: SUMMARIZE ----------------
st.header("Step 2️⃣ Summarize with AI")

if st.button("Generate Summary"):
    with st.status("Summarizing...", expanded=False):
        prompt = f"Summarize the following text:\n\n{st.session_state.text}"
        st.session_state.summary = groq_ai(prompt)
    st.success("✅ Summary generated")

if st.session_state.summary:
    st.subheader("📄 Summary")
    st.write(st.session_state.summary)

# ---------------- STEP 3: TRANSLATE ----------------
st.header("Step 3️⃣ Translate")

target_language = st.selectbox(
    "Select language", ["Tamil", "Hindi", "French", "Spanish"]
)

if st.button("Translate Summary"):
    with st.status("Translating...", expanded=False):
        prompt = f"Translate the following text to {target_language}:\n\n{st.session_state.summary}"
        st.session_state.translation = groq_ai(prompt)
    st.success("✅ Translation completed")

if st.session_state.translation:
    st.subheader("🌍 Translated Text")
    st.write(st.session_state.translation)

# ---------------- STEP 4: KEY POINTS ----------------
st.header("Step 4️⃣ Extract Key Points")

if st.button("Extract Key Points"):
    with st.status("Extracting key points...", expanded=False):
        prompt = (
            "Extract 5 key bullet points from the following text:\n\n"
            f"{st.session_state.summary}"
        )
        points = groq_ai(prompt)
        st.session_state.key_points = points.split("\n")
    st.success("✅ Key points extracted")

if st.session_state.key_points:
    st.subheader("🔑 Key Points")
    for point in st.session_state.key_points:
        st.write("•", point)

# ---------------- FINAL OUTPUT ----------------
st.header("📦 Final Output")

final_output = {
    "summary": st.session_state.summary,
    "translation": st.session_state.translation,
    "key_points": st.session_state.key_points,
}

st.json(final_output)

# ---------------- DOWNLOAD JSON ----------------
st.download_button(
    label="⬇️ Download JSON Report",
    data=json.dumps(final_output, indent=4),
    file_name="ai_workflow_output.json",
    mime="application/json",
)
