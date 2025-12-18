import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Interview Simulator", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "question" not in st.session_state:
    st.session_state.question = ""

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


tab1, tab2= st.tabs(["Ai interview", "histroy"])
with tab1:
    st.title("AI Interview Simulator")
    st.write("Practice interviews with AI-generated questions and feedback")

    role = st.selectbox(
        "Select Job Role",
        ["Developer", "Designer", "Data Analyst"]
    )
    if role == "Developer":
        domain = st.selectbox(
            "Select Domain",
            ["Frontend", "Backend", "Fullstack"]
        )
    elif role == "Designer":
        domain = st.selectbox(
            "Select Domain",
            ["UI/UX", "Graphic Design", "Product Design"]
        )
    else:
        domain = st.selectbox(
            "Select Domain",
            ["Business Analytics", "Data Science", "Machine Learning"]
        )
        

    if st.button("Generate Interview Question"):
        prompt = f"Generate one technical interview question for a {role} in {domain}.And give question related to domainshould be in one lineand easily to answer them"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        st.session_state.question = response.choices[0].message.content
        st.session_state.chat_history.append(
            {"role": "AI", "content": st.session_state.question}
        )

    if st.session_state.question:
        st.subheader("Interview Question")
        st.info(st.session_state.question)

    answer = st.text_area("Your Answer")

    if st.button("Submit Answer") and answer:
        eval_prompt = f"""
        You are an interviewer for the role of {role}.
        Question: {st.session_state.question}
        Answer: {answer}

        Evaluate the answer.
        Give:
        1. Score out of 10
        2. Short feedback
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": eval_prompt}]
        )

        feedback = response.choices[0].message.content

        st.session_state.chat_history.append({"role": "User", "content": answer})
        st.session_state.chat_history.append({"role": "AI", "content": feedback})

        st.success("Evaluation Complete")
        st.write(feedback)


with tab2:
    st.subheader("Interview History")
    with st.expander("History"):
        if st.session_state.chat_history:
            for chat in st.session_state.chat_history:
                if chat["role"] == "User":
                    st.markdown(f"**You:** {chat['content']}")
                else:
                    st.markdown(f"**AI:** {chat['content']}")
        else:
            st.info("No interview history yet")

    if st.button("Clear Interview History"):
        st.session_state.chat_history.clear()
        st.session_state.question = ""
        st.success("History cleared")








# client = Groq(api_key=st.secrets["GROQ_API_KEY"])