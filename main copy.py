from typing import List

from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
# for the agents, we need a llm and tools
from langchain.agents import create_agent
from langchain.tools import tool # decorator to create tools
# class to create messages to invoke the agent
from langchain_core.messages import HumanMessage 
from langchain_openai import ChatOpenAI # class to create llm
from langchain_ollama import Ollama # class to create llm
from langchain_tavily import TavilySearch # class to create tool

#example of a tool
@tool #convert function to a tool
def search(query:str) -> str:
    """ 
    Tool that searchs over the internet
    Args:
        query: The query to search for
    Returns:
        The result of the search
    """
    print(f"Searching the web for: {query}")
    return "Tokyo weather is sunny"



class Source(BaseModel):
    """Schema for a source used by the agent"""

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    """Schema for agent response with answer and sources"""

    answer: str = Field(description="Thr agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=list, description="List of sources used to generate the answer"
    )


#llm = ChatOpenAI(model="gpt-5")
llm = Ollama(model="qwen3.5:4b")
#tools = [TavilySearch()]
tools = [search]
agent = create_agent(model=llm, tools=tools)
#agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages":HumanMessage(content="What is the weather in Tokyo?")})

    # result = agent.invoke(
    #     {
    #         "messages": HumanMessage(
    #             content="search for 3 job postings for an ai engineer using langchain in the bay area on linkedin and list their details?"
    #         )
    #     }
    # )
    
    print(result)


if __name__ == "__main__":
    main()
