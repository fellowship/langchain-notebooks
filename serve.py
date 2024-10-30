from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes
from fastapi import FastAPI
import os
system_template = "{system prompt}:"
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system",system_template),
        ('user', '{text}')
    ]
)

# print(prompt_template.invoke({'language':'urdu', 'text':'hello'}))

model = ChatGroq(api_key="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")
parser = StrOutputParser()

chain = prompt_template | model | parser

app = FastAPI(
    title = "Langchain Server",
    version = "1.0",
    description = "A simple API server using LangChain's Runnable interfaces"
)

add_routes(
    app,
    chain,
    path="/chain"
)

from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8000/chain/")
remote_chain.invoke({"system prompt": "Translate the following to Urdu:", "text": "hi"})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host='localhost', port='8000')