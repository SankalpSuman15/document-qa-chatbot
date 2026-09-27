import os
import logging
from typing import Optional

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGSystem:
    def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=0.0,
            max_retries=2,
        )

        self.vectorstore: Optional[FAISS] = None
        self.retriever = None
        self.prompt = ChatPromptTemplate.from_template("""
            You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say "I don't know".
            Keep the answer concise.

            Question: {question}
            Context: {context}
            Answer:
        """)
        logger.info("RAG System initialized with model: %s", model_name)

    def ingest_document(self, pdf_path: str, index_name: str = "faiss_index") -> None:
        if not os.path.exists(pdf_path):
            logger.error("PDF file does not exist: %s", pdf_path)
            raise FileNotFoundError(f"PDF file does not exist: {pdf_path}")

        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstore.save_local(index_name)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        logger.info(
            "Document ingested and indexed successfully from: %s to index: %s",
            pdf_path,
            index_name,
        )

    def load_index(self, index_name: str = "faiss_index") -> None:
        if not os.path.exists(index_name):
            logger.error("Index directory does not exist: %s", index_name)
            raise FileNotFoundError(f"Index directory does not exist: {index_name}")

        self.vectorstore = FAISS.load_local(
            index_name, self.embeddings, allow_dangerous_deserialization=True
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        logger.info("Index loaded successfully from: %s", index_name)

    def ask(self, question: str) -> str:
        if not self.retriever:
            logger.error(
                "Retriever is not initialized. Load an index or ingest a document first."
            )
            raise ValueError(
                "Retriever is not initialized. Load an index or ingest a document first."
            )

        rag_chain = (
            {"context": self.retriever, "question": lambda x: x}
            | self.prompt
            | self.llm
        )

        response = rag_chain.invoke(question)
        return response.content
import os
import logging
from typing import Optional

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGSystem:
    def __init__(self, groq_api_key: str, model_name: str = "llama-3.1-8b-instant"):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=0.0,
            max_retries=2,
        )

        self.vectorstore: Optional[FAISS] = None
        self.retriever = None
        self.prompt = ChatPromptTemplate.from_template("""
            You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say "I don't know".
            Keep the answer concise.

            Question: {question}
            Context: {context}
            Answer:
        """)
        logger.info("RAG System initialized with model: %s", model_name)

    def ingest_document(self, pdf_path: str, index_name: str = "faiss_index") -> None:
        if not os.path.exists(pdf_path):
            logger.error("PDF file does not exist: %s", pdf_path)
            raise FileNotFoundError(f"PDF file does not exist: {pdf_path}")

        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        chunks = text_splitter.split_documents(documents)

        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstore.save_local(index_name)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        logger.info(
            "Document ingested and indexed successfully from: %s to index: %s",
            pdf_path,
            index_name,
        )

    def load_index(self, index_name: str = "faiss_index") -> None:
        if not os.path.exists(index_name):
            logger.error("Index directory does not exist: %s", index_name)
            raise FileNotFoundError(f"Index directory does not exist: {index_name}")

        self.vectorstore = FAISS.load_local(
            index_name, self.embeddings, allow_dangerous_deserialization=True
        )
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 4})
        logger.info("Index loaded successfully from: %s", index_name)

    def ask(self, question: str) -> str:
        if not self.retriever:
            logger.error(
                "Retriever is not initialized. Load an index or ingest a document first."
            )
            raise ValueError(
                "Retriever is not initialized. Load an index or ingest a document first."
            )

        rag_chain = (
            {"context": self.retriever, "question": lambda x: x}
            | self.prompt
            | self.llm
        )

        response = rag_chain.invoke(question)
        return response.content
