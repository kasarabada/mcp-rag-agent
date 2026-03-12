import os
import pickle
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

INDEX_FILE = "faiss_index.pkl"


def load_documents(folder="docs"):

    texts = []

    for file in os.listdir(folder):

        if file.endswith(".txt"):

            with open(os.path.join(folder, file), "r", encoding="utf-8") as f:
                texts.append(f.read())

    return texts


def build_vector_store():

    texts = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = []
    print("---------------------------")
    for text in texts:
        print(text)
        chunks.extend(splitter.split_text(text))

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    print("Embeddings OK")
    vector_store = FAISS.from_texts(chunks, embeddings)

    with open(INDEX_FILE, "wb") as f:
        pickle.dump(vector_store, f)

    return vector_store


def load_vector_store():

    if os.path.exists(INDEX_FILE):

        with open(INDEX_FILE, "rb") as f:
            return pickle.load(f)

    return build_vector_store()