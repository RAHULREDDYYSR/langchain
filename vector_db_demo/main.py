import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


if __name__ == "__main__":
    print("Retrieving..")

    embedding = OpenAIEmbeddings()
    llm = ChatOpenAI(model="gpt-4o-mini")

    query = "what is pinecone in machine learning"
    chain = PromptTemplate.from_template(template=query) | llm
    # print(chain.invoke(input={}))

    vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], embedding=embedding
    )
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm,retrieval_qa_chat_prompt)
    retrival_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )
    result = retrival_chain.invoke(input={"input":query})
    print(result['answer'])

