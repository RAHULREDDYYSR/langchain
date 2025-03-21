import os

from dotenv import load_dotenv
load_dotenv()
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

if __name__=="__main__":
    print("ingestion..")
    file_path = "C:/Users/rahul/work_space/Lang_chain/vector_db_demo/mediumblog1.txt"
    loader = TextLoader(file_path, encoding="utf-8")
    document = loader.load()

    print("splitting..")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    embedding = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))

    print("ingesting..")
    PineconeVectorStore.from_documents(texts, embedding, index_name=os.environ['INDEX_NAME'])
    print("finish.")