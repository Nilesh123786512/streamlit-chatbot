import os
from openai import OpenAI
import requests
import base64
from concurrent.futures import ThreadPoolExecutor
# from tavily import TavilyClient
import asyncio
import re
import streamlit as st
from duckduckgo_search import DDGS

# client5 = genai.Client(api_key=st.secrets['google'])

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
    11: "gemini-2.0-flash",
    12: "gemini-2.0-pro-exp-02-05",
    
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
client5 = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=st.secrets['google'])

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
        elif model_number in [11,12]:
            response = client5.chat.completions.create(
                model=models_dict[model_number], messages=conversation,
                 temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
            # return response.text

        else:
            response = client2.chat.completions.create(
                model=models_dict[model_number], messages=conversation,
                 temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise e
        return f"Error: {e}"


def generate_audio(text):
    # Replace this URL with your actual API endpoint
    api_url = "https://openfm.onrender.com/api/generate"
    text= {
    "input": text,
    "voice": "shimmer",
    "vibe": "null",
    "customPrompt": "Voice Affect:Fast, Mystical and dreamy\nTone: Soft and enchanting\nPacing: FastnEmotion: Whimsical and magical\nPronunciation: Smooth and ethereal\nPauses: Strategic pauses for effect"
}
    headers = {
    'Content-Type': 'application/json'
}
    response = requests.post(api_url, headers=headers, json=text)

    if response.status_code == 200:
        # print("Sound file downloaded successfully.")
        return response.content
    else:
        print(f"Error: {response.status_code}")

def transcribe_audio(audio_data):
    """Transcribe audio using Groq's whisper-large-v3-turbo"""
    try:
        # Create transcription request with raw bytes
        print("Got input Transcribing......")
        response = client3.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=("audio.wav", audio_data, "audio/wav"),
            response_format="text"
        )
        print(f'Transcribed Sucessfully . response:{response}')
        return response
    except Exception as e:
        print(f"Transcription error: {e}")
        return None

def play_audio(audio_data,col2):
    if audio_data:
        # Convert audio data to base64
        b64 = base64.b64encode(audio_data).decode()
        audio_html = f"""
        <audio controls>
            <source src="data:audio/wav;base64,{b64}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        """
        with col2:
            st.components.v1.html(audio_html, height=100)
