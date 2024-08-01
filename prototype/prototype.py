import os
import time
from typing import List, Union

import streamlit as st
import tiktoken
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.runnables import Runnable
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredHTMLLoader,
    WebBaseLoader,
)
from langchain_community.vectorstores import Chroma
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from loguru import logger

store = {}


def main() -> None:
    """
    Main function to set up and run the Streamlit app.
    """
    # Load environment variables (API key)
    load_dotenv()

    model = "openai"

    st.set_page_config(
        page_title="prototype",
        page_icon="🤖",
        layout="wide",
    )

    # Sidebar
    st.sidebar.title("Categories")
    category1 = st.sidebar.expander("Category 1", expanded=False)
    category2 = st.sidebar.expander("Category 2", expanded=True)

    # TODO: Change to be added each time a new chat is created
    with category1:
        st.write("New Chat Title 1")
        st.write("New Chat Title 2")

    with category2:
        st.write("New Chat Title 1")
        st.write("New Chat Title 2")

    st.title("LingChat Prototype")

    # The form for chat input
    # TODO: Additional items depending on how the UI changes
    reference_links = st.text_area(
        "Reference Links", "Enter reference links here", key="reference_links"
    )

    # Initialize session state of streamlit
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "processComplete" not in st.session_state:
        st.session_state.processComplete = None

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Ask me a question!"}
        ]

    st.sidebar.header("Upload Source")

    # Upload file or input website URL
    source_type = st.sidebar.selectbox(
        "Select Source Type", options=["pdf", "txt", "html", "website", "none"]
    )

    with st.sidebar:
        if source_type in ["pdf", "txt", "html"]:
            uploaded_files = st.file_uploader(
                "Upload your file", type=source_type, accept_multiple_files=True
            )
        elif source_type == "website":
            uploaded_files = [
                link.strip() for link in reference_links.split("\n") if link.strip()
            ]
        # TODO: Implement when a file other than the specified file comes in
        else:
            uploaded_files = None

    # If click the start button then start the chatbot
    if st.button("Start!!!") and uploaded_files is not None:
        st.title("RingChat")
        st.write("Chatbot started!")

        docs = get_text(uploaded_files, source_type)
        chunks = get_text_chunks(docs)
        vectorstore = get_vectorstore(chunks)

        llm = get_model(model)
        st.session_state.conversation = get_conversation_chain(llm, vectorstore)

        st.session_state.processComplete = True

    # TODO: Implement conversations without documents
    else:
        pass

    # upload -> start -> chat
    st.header("Chat with the Document")

    # Process and display each chat message if the process is complete
    if st.session_state.processComplete:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # User input
    user_input = st.chat_input("Ask a question:")

    if user_input:
        start = time.time()
        st.session_state.messages.append({"role": "User", "content": user_input})

        # Display user input
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            # TODO: Compare similarity and answer based on what you found if the value is low
            chain = st.session_state.conversation

            with st.spinner("Thinking..."):
                # Get the chat history for the current session
                conversational_rag_chain = RunnableWithMessageHistory(
                    chain,
                    get_session_history,
                    input_messages_key="input",
                    history_messages_key="chat_history",
                    output_messages_key="answer",
                )

                # TODO: Change configuration settings if needed
                # TODO: Using session_id to remember context
                result = conversational_rag_chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": "test"}},
                )

                response = result["answer"]

                st.markdown(response)

        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        end = time.time()
        print(f">>>>>>>>>>>>>> {end - start:.5f} sec")


def create_openai_llm() -> ChatOpenAI:
    """
    Functions for setting up OpenAI LLM

    Returns:
        ChatOpenAI: OpenAI chat model instance.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY is not set.")
    return ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name="gpt-4o-mini",
        callbacks=[StreamingStdOutCallbackHandler()],
        temperature=0,
    )


# TODO: Use databases to manage session history
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """
    Use session_id to remember previous conversations.
    Currently stored in a dict (memory).

    Args:
        session_id (str): The session ID.

    Returns:
        BaseChatMessageHistory: The chat message history for the session.
    """
    print(f"[session_id]: {session_id}")
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def get_model(model: str) -> ChatOpenAI:
    """
    Decide which model to use.

    Args:
        model (str): The model to use.

    Returns:
        ChatOpenAI: The chosen chat model instance.

    Raises:
        ValueError: If the model is not supported.
    """
    llm_creator = {
        "openai": create_openai_llm,
        # TODO: Add more models if needed
    }

    if model not in llm_creator:
        raise ValueError(f"Unsupported LLM mode: {model}")

    llm = llm_creator[model]()
    print(f"{model} model!!!")

    return llm


def save_uploaded_file(doc) -> str:
    """
    Save the uploaded file.

    Args:
        doc: The uploaded document.

    Returns:
        str: The file name of the saved document.
    """
    file_name = doc.name
    with open(file_name, "wb") as file:
        file.write(doc.getvalue())
    logger.info(f"Uploaded {file_name}")
    return file_name


def get_text(docs: Union[List, str], source_type: str) -> List:
    """
    Convert uploaded files to text.

    Args:
        docs (Union[List, str]): The documents to convert.
        source_type (str): The type of the source.

    Returns:
        List: A list of documents as text.
    """
    doc_list = []

    if source_type in ["pdf", "txt", "html"]:
        # docs can contain multiple files
        for doc in docs:
            file_name = save_uploaded_file(doc)
            documents = load_document(file_name)
            doc_list.extend(documents)
    # TODO: Decide whether to implement the website part separately or as another function
    elif source_type == "website":
        # TODO: Implement multiple webpage loading if docs contain multiple links -> implemented
        documents = load_website(docs)
        doc_list.extend(documents)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")
    return doc_list


def load_document(file_name: str) -> List:
    """
    Load and split documents using the appropriate loader based on filename.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        List: A list of documents split into parts.
    """
    if file_name.endswith(".pdf"):
        loader = PyPDFLoader(file_name)
    elif file_name.endswith(".html"):
        loader = UnstructuredHTMLLoader(file_name)
    elif file_name.endswith(".txt"):
        loader = TextLoader(file_name)
    else:
        raise ValueError(f"Unsupported file type: {file_name}")

    # TODO: Functionalize the use of the load function by TXT, HTML, and PDF
    documents = loader.load_and_split()

    return documents


# TODO: Decide whether to implement the website part separately or merge it with load_document
def load_website(link: str) -> List:
    """
    Load and parse content from a website.

    Args:
        link (str): The website link.

    Returns:
        List: A list of parsed website content.
    """
    # TODO: WebBaseLoader vs AsyncChromiumLoader
    # WebBaseLoader parses only the necessary parts from the specified webpage
    loader = WebBaseLoader(link)
    docs = loader.load()

    return docs


def tiktoken_len(text: str) -> int:
    """
    Count the number of tokens in a text.

    Args:
        text (str): The text to tokenize.

    Returns:
        int: The number of tokens in the text.
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)


def get_text_chunks(text: List[Document]) -> List[Document]:
    """
    Split a document into chunks.

    Args:
        text (str): The text to split.

    Returns:
        List: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, length_function=tiktoken_len
    )
    chunks = text_splitter.split_documents(text)
    return chunks


def get_conversation_chain(llm, vectorstore) -> Runnable:
    """
    Create a conversation chain.

    Args:
        llm: The language model to use.
        vectorstore: The vector store for document retrieval.

    Returns:
        RetrievalQAChain: The created conversation chain.
    """

    condense_question_system_template = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
        "Please answer the question in Korean."
    )

    contextualize_question_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", condense_question_system_template),
            MessagesPlaceholder("chat_history"),
            ("user", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, vectorstore.as_retriever(), contextualize_question_prompt
    )

    system_prompt = (
        "Based on the following context, answer the user's question. "
        "You are a world-class document writing expert. "
        "Feel free to ask anything. If you don't know the answer, just say you don't know. "
        "Summarize in 3 lines."
        "\n\n"
        "{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("user", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return rag_chain


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Get the embedding model.

    Returns:
        HuggingFaceEmbeddings: The embedding model.
    """
    return HuggingFaceEmbeddings(
        # TODO: Find a better model if available
        model_name="jhgan/ko-sroberta-multitask",
        model_kwargs={"device": "cpu"},  # or cuda
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vectorstore(text_chunks: List) -> Chroma:
    """
    Vectorize chunks of text and store them in a database.

    Args:
        text_chunks (List): The text chunks to vectorize.

    Returns:
        Chroma: The created vector store.
    """

    embeddings = get_embedding_model()
    db = Chroma.from_documents(text_chunks, embeddings, persist_directory="./chroma_db")
    return db


if __name__ == "__main__":
    main()
