from langchain.tools import Tool
from rag_pipeline import retrieve_docs


def calculator(expression: str):

    try:
        return str(eval(expression))
    except Exception as e:
        return str(e)


retriever_tool = Tool(
    name="DocumentRetriever",
    func=retrieve_docs,
    description="Useful for answering questions from knowledge base documents"
)


calculator_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Useful for solving math expressions"
)


TOOLS = [retriever_tool, calculator_tool]