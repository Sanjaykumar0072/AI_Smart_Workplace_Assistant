import streamlit as st
from ai_engine import ask_ai
from document_utils import read_pdf

st.set_page_config(page_title="AI Workplace Assistant", layout="centered")

st.title("🤖 AI-Powered Smart Workplace Assistant")

option = st.selectbox(
    "Choose what you want to do:",
    ("Ask a Question", "Summarize Text", "Ask from Document")
)

if option == "Ask a Question":
    user_input = st.text_area("Enter your question:")
    if st.button("Ask AI"):
        if user_input.strip():
            response = ask_ai(user_input)
            st.subheader("Answer:")
            st.write(response)
        else:
            st.warning("Please enter a question.")

elif option == "Summarize Text":
    text_input = st.text_area("Paste text to summarize:")
    if st.button("Summarize"):
        if text_input.strip():
            prompt = f"Summarize the following text in 5 bullet points:\n\n{text_input}"
            response = ask_ai(prompt)
            st.subheader("Summary:")
            st.write(response)
        else:
            st.warning("Please paste some text.")

elif option == "Ask from Document":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    question = st.text_input("Ask a question from the document:")

    if st.button("Get Answer"):
        if uploaded_file and question.strip():
            document_text = read_pdf(uploaded_file)
            prompt = f"""
            Use the following document to answer the question.
            Document:
            {document_text}

            Question: {question}
            """
            response = ask_ai(prompt)
            st.subheader("Answer from Document:")
            st.write(response)
        else:
            st.warning("Please upload a PDF and enter a question.")