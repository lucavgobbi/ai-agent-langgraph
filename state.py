
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph.message import add_messages


class State(TypedDict):
    """State for the agent."""
    messages: Annotated[list, add_messages]  # List of messages in the conversation
    name: str
    birthday: str
