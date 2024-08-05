from fastapi import FastAPI

app = FastAPI()

# import os

# from dotenv import load_dotenv
# from fastapi import FastAPI, Request
# from langchain_openai import OpenAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain.prompts import PromptTemplate


# app = FastAPI()

# # OpenAI API key settings
# load_dotenv()
# llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # Prompt template for creating text
# prompt_template = PromptTemplate(
#     input_variables=["question"],
#     template="Please answer the following questions: {question}"
# )

# # Create LLMChain
# prompt = PromptTemplate.from_template(prompt_template.template)
# llm_chain = prompt | llm | StrOutputParser()

# @app.post("/ask")
# async def ask_question(request: Request):
#     user_input = await request.json()
#     question = user_input.get("question")

#     if question:
#         response = llm_chain.invoke(question)
#         return {"answer": response}
#     else:
#         return {"error": "Please enter your question"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)