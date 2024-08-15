import os
from typing import List, Union
import warnings

from langchain.chains import create_history_aware_retriever
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import Chroma
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
import tiktoken

# 특정 경고 무시
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers.tokenization_utils_base")

# TOKENIZERS_PARALLELISM 설정
os.environ["TOKENIZERS_PARALLELISM"] = "false"

store = {}

def get_text_chunks(text: List[Document]) -> List[Document]:
    """
    Split a document into chunks.

    Args:
        text (str): The text to split.

    Returns:
        List: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        # 문서가 클 경우 parameter 조정 필요
        chunk_size=1000, chunk_overlap=200, length_function=tiktoken_len
    )
    chunks = text_splitter.split_documents(text)
    return chunks

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

def get_conversation_chain(llm, vectorstore):
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

def get_langchain_answer(docs: List[Document], question: str, session_id: str):

    model = "openai"
    chunks = get_text_chunks(docs)
    vectorstore = get_vectorstore(chunks)
    
    # TODO: 유사도 
    # 임베딩 모델 가져오기
    # embedding_model = get_embedding_model()
    
    # 질문을 임베딩하여 벡터화
    # question_vector = embedding_model.embed([question])[0]
    
    # 유사도 검색
    # results = vectorstore.similarity_search_by_vector(question_vector, k=1)
    
    llm = get_model(model)
    chain = get_conversation_chain(llm, vectorstore)

    if question:
        conversational_rag_chain = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
    
        result = conversational_rag_chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}},
        )

        # 결과 출력
        print("Result:", result)

        if 'answer' in result:
            response = result['answer']
        else:
            response = "No answer found."

    return response

