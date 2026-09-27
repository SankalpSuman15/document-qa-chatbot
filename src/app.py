import os
import tempfile
from dotenv import load_dotenv
import streamlit as st
from rag import RAGSystem

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not found in .env")
    st.stop()

INDEX_NAME = "faiss_index"


def init_rag():
    if "rag" not in st.session_state:
        st.session_state.rag = RAGSystem(groq_api_key=GROQ_API_KEY)
        if os.path.exists(INDEX_NAME):
            try:
                st.session_state.rag.load_index(INDEX_NAME)
                st.session_state.index_loaded = True
            except Exception:
                st.session_state.index_loaded = False
        else:
            st.session_state.index_loaded = False
    return st.session_state.rag


def main():
    st.set_page_config(page_title="Document Q&A Chatbot", layout="wide")
    st.title("Document Q&A Chatbot")
    st.markdown("Upload a PDF and ask questions based on its content.")

    rag = init_rag()
    index_loaded = st.session_state.get("index_loaded", False)

    with st.sidebar:
        st.header("Upload & Ingest")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            if st.button("Ingest PDF"):
                with st.spinner("Processing..."):
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name
                    try:
                        rag.ingest_document(tmp_path, INDEX_NAME)
                        st.session_state.index_loaded = True
                        st.success("PDF ingested successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                    finally:
                        os.unlink(tmp_path)
        st.divider()
        st.caption("Status: " + ("Index ready" if index_loaded else "No index"))

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask a question about your document")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            if not index_loaded:
                response = "Please upload and ingest a pdf first."
            else:
                with st.spinner("Thinking..."):
                    try:
                        response = rag.ask(prompt)
                    except Exception as e:
                        response = f"Error: {e}"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


if __name__ == "__main__":
    main()
