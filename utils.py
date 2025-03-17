import os
from openai import OpenAI
# from tavily import TavilyClient
import asyncio
import re
import streamlit as st
from duckduckgo_search import DDGS


models_dict = {
    0: "qwen-qwq-32b",
    1: "qwen-2.5-32b",
    2: "qwen-2.5-coder-32b",
    3: "deepseek-r1-distill-qwen-32b",
    4: "deepseek-r1-distill-llama-70b",
    5: "deepseek-r1",
    6: "deepseek-v3",
    7: "claude-3-5-sonnet-20240620",
    8: "gpt-4o-2024-05-13",
    9: "deepseek/deepseek-chat:free",
    10: "deepseek/deepseek-r1:free",
}

## Declaring the clients for different purposes
client1 = OpenAI(
    base_url="https://api.sree.shop/v1",
    api_key=st.secrets["devsdocode"])
client2 = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["groq_api"])

client3 = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    # base_url="https://api.sree.shop/v1",
    api_key=st.secrets["groq_api2"])
client4 = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["open_router"])

#Search client
ddgs = DDGS()
# tavily_client = TavilyClient(api_key=st.secrets["tavily_1"])


#Tavily search if asked
async def search_tavily(query):
    # print(f'Got query {query}')
    try:
        query = query.copy()
        query.append({
            "role":
            "system",
            "content":
            "Based on all above queries give me a single search query enclosed in <search>content to search</search>.If the query was straight forward then don't modify just enclose it else from context give the best query.Also highlight the keywords that needs to be searched by **keyword**"
        })

        # print(f"Changed query:{query}")
        # query_filtered.choices[0].message.content
        query_filtered = client3.chat.completions.create(
            model="llama3-70b-8192", messages=query)
        query_filtered = re.search(r'''<search>(.*?)</search>''',  query_filtered.choices[0].message.content,
                                   re.DOTALL)
        # print("Fetching query:",query_filtered.group(1))
        # response = tavily_client.search(query_filtered.group(1))
        results = ddgs.text(query_filtered.group(1), max_results=5)
        res=""
        for i,r in enumerate(results):
            res+=f'[search{i+1}]({r["href"]}):\n{r["body"]}\n'
        return res
    except Exception as e:
        print(f'Exception is {e}')
        return "Unable to fetch search results"


# openai.api_key = "your_openai_api_key"  # Replace with your actual OpenAI API key
async def query_openai(conversation,
                       model_number=1,
                       search=False,
                       temp=0.5,
                       top_p=0.95):
    """
    Send the conversation history to the OpenAI Chat API and return the assistant's response.
    """
    respo = None
    if search:
        # print(conversation[-1]['content'])
        respo = await search_tavily(conversation)
        # print(f'response is provided by tavily {respo}')
        conversation.append({
            "role":
            "system",
            "content":
            f"Additional context from recent search results: {respo}"
        })
    try:
        if model_number in [5, 6, 7, 8]:
            print(f"Conversation :{conversation}")
            response = client1.chat.completions.create(
                model=models_dict[model_number],
                messages=conversation,
                temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
            # print(f"Response is {response.choices[0].message.content}")
        elif model_number in [9, 10]:
            response = client4.chat.completions.create(
                model=models_dict[model_number], messages=conversation,
                 temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
        else:
            response = client2.chat.completions.create(
                model=models_dict[model_number], messages=conversation,
                 temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise e
        return f"Error: {e}"








