from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate

# SDK 
from langchain_openai import ChatOpenAI
from langchain_google_genai import GoogleGenerativeAI
from langchain_ollama import ChatOllama

load_dotenv()


def main():
    print("Hello from langchain-course!")
    # print(os.environ.get("GOOGLE_API_KEY"))
    information = """
    Elon Musk is a software engineer, entrepreneur, and investor.
    """
    summary_template = """
    given the information {information} about a person I want you to create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    # tempreture 0-1 determines the creativity and randomness of the model
    # lower tempreture（0-0.3） means more predictable and deterministic output
    # good for summarizing information and coding tasks
    # higher tempreture（0.8-1） means more creative and random output
    # good for generating creative content and poetry and fiction writing
    
    # llm = ChatOpenAI(temperature=0, model="gpt-5")
    # llm = GoogleGenerativeAI(
    #     model="gemini-2.5-flash", api_key=os.environ.get("GOOGLE_API_KEY")
    # )
    llm = ChatOllama(temperature=0, model="qwen3.5:4b", reasoning=False)

    # LECL - LangChain Expression Language
    # | is the PIPE operator in LECL 
    # it is used to composing two components together, 
    # like chaining the prompt template and the model together
    # by connecting the output of the first component to the input of the second component
    # to populate the prompt template with the information and then pass it to the model
    chain = summary_prompt_template | llm

    # chain is the runnable object, it is the final object that we can invoke to get the response
    # input is the dictionary of the input variables
    response = chain.invoke(input={"information": information})

    #print(response) # for google models
    print(response.content)

if __name__ == "__main__":
    main()
