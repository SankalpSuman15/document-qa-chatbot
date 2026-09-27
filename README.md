# Document Q&A Chatbot

A production-ready **Retrieval-Augmented Generation (RAG)** system that lets you chat with PDF documents. Built with **Langchain**, **FAISS**, and **Groq**.

## Features

- Upload any PDF and ask questions in natural language.
- Semantic search using **FAISS** (fast, local vector DB).
- Powered by **Groq's Llama 3.1** for fast, accurate answers.
- Clean **Streamlit** chat interface.
- Persistent FAISS index - no need to re-upload on every restart.

## Setup

### Prerequisites

- Python 3.10+
- Git
- (Recommended) `uv` package manager

### Option1: Setup using `uv` (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/SankalpSuman15/document-qa-chatbot.git
   ```

   ```bash
   cd document-qa-chatbot
   ```

2. Create a virtual environment:

   ```bash
   uv venv
   ```

3. Activate the virtual environment:
   - **Linux/macOS**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (Powershell)**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**
     ```cmd
     .venv\Scripts\activate.bat
     ```

4. Install dependencies:

   If using `pyproject.toml`:

   ```bash
   uv sync
   ```

   or, if using a lock file:

   ```bash
   uv sync --frozen
   ```

5. Run the Streamlit app:
   ```bash
   streamlit run src/app.py
   ```

### Option 2: Setup using `requirements.txt`

1. Clone the repository:

   ```bash
   git clone https://github.com/SankalpSuman15/document-qa-chatbot.git
   ```

   ```bash
   cd document-qa-chatbot
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - **Linux/macOS**
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (Powershell)**
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**
     ```cmd
     .venv\Scripts\activate.bat
     ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the Streamlit app:

   ```bash
   streamlit run src/app.py
   ```

## Usage

1. Upload the PDF via the sidebar.
2. Click "Ingest PDF" - this builds the FAISS index (takes a few seconds).
3. In the main chat area, type any question about the document.
4. The assistant will answer only using information from the PDF.
5. Use "Clear Chat" to reset the conversation.

## License

### [MIT](LICENSE)
