from vector_store import load_vector_store

vector_store = load_vector_store()


def retrieve_docs(query, k=3):

    docs = vector_store.similarity_search(query, k=k)

    return "\n\n".join([doc.page_content for doc in docs])