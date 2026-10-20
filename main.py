from dotenv import load_dotenv

load_dotenv()
# for the agents, we need a llm and tools
from langchain.agents import create_agent
from langchain.tools import tool # decorator to create tools
# class to create messages to invoke the agent
from langchain_core.messages import HumanMessage 
from langchain_openai import ChatOpenAI # class to create llm
from langchain_ollama import ChatOllama # class to create llm
#Tavily Client from SDK to call search in created custom tool
from tavily import TavilyClient # class to create tool
tavily = TavilyClient()
#Tavily's own integrated Langchain search tool that better utilize the Tavily SDK
# all we need is to initialze the instance from the TavilySearch class
from langchain_tavily import TavilySearch


#example of a custom tool
@tool #convert function to a tool for searching the web using Tavily client
def search(query:str) -> str:
    """ 
    Tool that searchs over the internet
    Args:
        query: The query to search for
    Returns:
        The result of the search
    """
    print(f"Searching the web for: {query}")
    #return "Tokyo weather is sunny"
    return tavily.search(query=query)


#llm = ChatOpenAI(model="gpt-5")
llm = ChatOllama(model="qwen3.5:4b")
#tools = [search]
tools = [TavilySearch() ]
agent = create_agent(model=llm, tools=tools)

 
def main():
    print("Hello from langchain-course!")
    #result = agent.invoke({"messages":HumanMessage(content="What is the weather in Tokyo?")})
    result = agent.invoke({"messages": HumanMessage(content="Search for 3 job postings for an AI engineer using Langchain in Milan on Linkedin and list their details.") })
    """
        Flow: 
         input query: "What is the weather in Tokyo?"
          |
         llm decides: seach tool: "current weather in Tokyo Japan?"
          |
         tool response: "Tokyo weather is sunny"
          |
         possible more decides and tool callings...
          |
         response: final answer:  "The weather in Tokyo is sunny"
    """
    print(result)


if __name__ == "__main__":
    main()
