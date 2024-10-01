from langchain.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
    LLMChain,
)
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.llm.message_task import store


def get_rag_chain(document_text: str):
    try:
        llm = ChatOpenAI(model="gpt-4o-mini", streaming=True)

        embeddings = OpenAIEmbeddings()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        split_texts = text_splitter.split_text(document_text)

        vectorstore = Chroma.from_texts(texts=split_texts, embedding=embeddings)

        retriever = vectorstore.as_retriever()

        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
            "Please answer the question in Korean."
        )
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("user", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Please write your answer in as much detail as possible."
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
        rag_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        return rag_chain

    except Exception as e:
        raise RuntimeError(f"Error generating rag chain: {e}")


def get_session_history(session_id: int) -> ChatMessageHistory:
    if session_id not in store or "chat_history" not in store[session_id]:
        store[session_id] = {
            "document_text": "",
            "chat_history": ChatMessageHistory(),
        }
    print(store[session_id]["chat_history"])
    return store[session_id]["chat_history"]


def get_langchain_response(user_message: str, chat_room_id: int):
    try:
        if chat_room_id not in store:
            raise RuntimeError(
                f"No data available for chat room {chat_room_id}"
            )

        document_text = store[chat_room_id]["document_text"]
        rag_chain = get_rag_chain(document_text)

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        answer_chain = conversational_rag_chain.pick("answer")
        return answer_chain.stream(
            {"input": user_message},
            config={"configurable": {"session_id": chat_room_id}},
        )

    except Exception as e:
        raise RuntimeError(f"Error generating answer: {e}")


def summarize_content(content: str) -> str:
    try:
        llm = ChatOpenAI(model="gpt-4o-mini")

        prompt = PromptTemplate(
            template="Summarize into English keywords, focusing on the important content. This summary should be embedded for similarity search, so there should be no unnecessary content, especially don't write 'keywords'.:\n\n{content}",
            input_variables=["content"],
        )

        summarize_chain = LLMChain(prompt=prompt, llm=llm)

        summary = summarize_chain.run(content=content)
        return summary

    except Exception as e:
        raise RuntimeError(f"Error summarizing content: {e}")
