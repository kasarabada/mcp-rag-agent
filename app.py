import os
import os
from dotenv import load_dotenv
import gradio as gr

from langchain_openai import ChatOpenAI
from langchain.agents.agent import AgentExecutor
from langchain.agents import create_openai_tools_agent
from langchain import hub

from agent_tools import TOOLS
from mcp_context import MCPContext


load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

prompt = hub.pull("hwchase17/openai-tools-agent")

agent = create_openai_tools_agent(
    llm,
    TOOLS,
    prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    verbose=True
)

mcp = MCPContext()


def chat(user_input):

    context = mcp.get_context()

    full_prompt = f"{context}\nUser Query: {user_input}"

    result = agent_executor.invoke({
        "input": full_prompt
    })

    response = result["output"]

    mcp.add_turn(user_input, response)

    return response


with gr.Blocks() as demo:

    chatbot = gr.Chatbot()

    msg = gr.Textbox()

    def respond(message, chat_history):

        bot_message = chat(message)

        chat_history.append((message, bot_message))

        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch()