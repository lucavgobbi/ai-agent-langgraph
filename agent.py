#!/usr/bin/env python3
"""
Basic AI Agent using LangGraph and Azure OpenAI

This example demonstrates a simple AI agent that can:
1. Receive user input
2. Process it using Azure OpenAI
3. Generate responses
4. Maintain conversation state

The agent uses LangGraph to define a simple conversation flow.
"""

import os
from dotenv import load_dotenv

from langchain.schema.runnable import RunnableConfig

from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from llm import get_llm
from state import State
import datetime

from tools import get_tools

# Load environment variables
load_dotenv(override=True)

tools = get_tools()
llm = get_llm(tools)

def chatbot_node(state: State):
    message = llm.invoke(state["messages"])
    # Because we will be interrupting during tool execution,
    # we disable parallel tool calling to avoid repeating any
    # tool invocations when we resume.
    assert len(message.tool_calls) <= 1 # type: ignore
    return {"messages": [message]}

def main():
    memory = MemorySaver()
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot_node)

    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")
    graph = graph_builder.compile(checkpointer=memory)

    thread_id = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break
            elif user_input.lower() == "graph":
                print("Graph structure:")
                print(graph.get_graph().draw_mermaid())
                continue
            elif user_input.lower() == "state":
                print("Current state:")
                print(graph.get_state(config))
                continue
            else:
                # The config is the **second positional argument** to stream() or invoke()!
                events = graph.stream(
                    {"messages": [{"role": "user", "content": user_input}]}, # type: ignore
                    config,
                    stream_mode="values",
                )
                for event in events:
                    event["messages"][-1].pretty_print()
        except Exception as e:
            # fallback if input() is not available
            print("An error occurred. Please try again. Error:", e)
            break

if __name__ == "__main__":
    main()
