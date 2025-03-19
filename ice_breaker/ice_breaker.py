from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent


def ice_break_with(name: str) -> str:

    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    summary_template = """
       give the linkedin information {information} about a person from I want you to create:
       1. a short summary
       2. two interesting facts about them
       """

    summary_prompt_template = PromptTemplate(
        input_variable=["information"], template=summary_template
    )
    # llm = ChatOllama(model="gemma3:1b")
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini")
    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"information": linkedin_data})
    print(res)


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name="rahul y s cit bengaluru")
