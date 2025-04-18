import wave
import miniaudio
import contextlib
import os
import streamlit as st
from openai import OpenAI
import requests
import base64
from concurrent.futures import ThreadPoolExecutor
import io
import asyncio
import re
import streamlit as st
from duckduckgo_search import DDGS
import httpx

def replacer(match):
        # Check which group matched
    code_block = match.group(1)
    open_math = match.group(2)
    close_math = match.group(3)

    if code_block:
        # If it's a code block (group 1), return it unchanged
        return code_block
    elif open_math:
        # If it's the opening math delimiter (group 2), replace it with $
        return "$"
    elif close_math:
        # If it's the closing math delimiter (group 3), replace it with $
        return "$"
    else:
        # This case should not be reached with the given pattern,
        # but it's good practice to handle it.
        return match.group(0) # Return the original match if unsure

# import streamlit.components.v1 as components
# client5 = genai.Client(api_key=st.secrets['google'])

models_dict = {
    13: "deepseek/deepseek-chat-v3-0324:free",
    15: "meta-llama/llama-4-maverick:free",
    9: "deepseek/deepseek-chat:free",
    12: "openai/gpt-4.1-mini",
    17: "gemini-2.5-flash-preview-04-17",
    14: "gemini-2.5-pro-exp-03-25",
    1: "gemini-2.0-flash-thinking-exp-1219",
    3: "openai/gpt-4.1",
    2: "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
    16: "google/gemini-2.5-pro-exp-03-25:free",
    0: "qwen-qwq-32b",
    4: "deepseek-r1-distill-llama-70b",
    10: "deepseek/deepseek-r1:free",
    8: "gpt-4o-2024-05-13",
    7: "claude-3-5-sonnet-20240620",
    5: "deepseek-r1",
    6: "deepseek-v3",
    11: "gemini-2.0-flash",
}

## Declaring the clients for different purposes
client1 = OpenAI(
    base_url="https://api.sree.shop/v1",
    api_key=st.secrets["devsdocode"])
client2 = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["groq_api"])

client3 = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=st.secrets["github"])
client4 = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["open_router"])
client5 = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=st.secrets['google'])


# tavily_client = TavilyClient(api_key=st.secrets["tavily_1"])


#Tavily search if asked
async def search_tavily(query):
    #Search client
    ddgs = DDGS()
    # print(f'Got query {query}')
    try:
        query = query.copy()
        query.append({
            "role":
            "system",
            "content":
            "Based on all above queries give me a single search query enclosed in <search>content to search</search>.If the query was straight forward then don't modify just enclose it else from context give the best query.Also highlight the keywords that needs to be searched by **keyword**"
        })

        print(f"Changed query:{query}")
        # query_filtered.choices[0].message.content
        query_filtered = client2.chat.completions.create(
            model="deepseek-r1-distill-llama-70b", messages=query)
        query_filtered = re.search(r'''<search>(.*?)</search>''',  query_filtered.choices[0].message.content,
                                   re.DOTALL)
        print("Fetching query:",query_filtered.group(1))
        # response = tavily_client.search(query_filtered.group(1))
        results = ddgs.text(query_filtered.group(1), max_results=5)
        res=""
        for i,r in enumerate(results):
            res+=f'[search{i+1}]({r["href"]}):\n{r["body"]}\n'
        print(res)
        return res
    except Exception as e:
        print(f'Exception is {e}')
        return "Unable to fetch search results"

def stream_data_(stream):
    resp=""
    for chunk in stream:
        _cont=chunk.choices[0].delta.content
        if _cont is None:
            continue
        yield chunk.choices[0].delta.content
        resp+=chunk.choices[0].delta.content
    return resp
        
# openai.api_key = "your_openai_api_key"  # Replace with your actual OpenAI API key
async def query_openai(conversation,
                       model_number=1,
                       search=False,
                       temp=0.5,
                       top_p=0.95):
    """
    Send the conversation history to the OpenAI Chat API and return the assistant's response.
    """
    print(f'File:Utils,Got search in utils :{search}')
    respo = None
    if search:
        # print(conversation[-1]['content'])
        # print(f'File:Utils,Got search in utils :{search}')
        respo = await search_tavily(conversation)
        print(f'response is provided by tavily {respo}')
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
                stream=False,
                messages=conversation,
                temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
            # print(f"Response is {response.choices[0].message.content}")
        elif model_number in [2,9, 10,13,15,16]:
            with st.spinner(text="Thinking..."):
                response_ = client4.chat.completions.create(
                    model=models_dict[model_number], messages=conversation,
                    temperature=temp,  # Set temperature to 0.7
                    top_p=top_p,
                    stream=True)
            # response=""
            with st.chat_message("assistant"):
                return st.write_stream(stream_data_(response_)) 
            

        elif model_number in [1,11,14,17]:
            conv=conversation.copy()
            conv.append({
            "role":
            "system",
            "content":
            """
            Instructions for output:
            1)Give the maths expressions(if exists) in perfect latex that is rendered perfectly in markdown.Don't give latex as seperate code block.Don't say that i am giving in latex rendering to user.
"""
        })
            with st.spinner(text="Thinking...."):
                response_ = client5.chat.completions.create(
                    model=models_dict[model_number], messages=conv,
                    temperature=temp,  # Set temperature to 0.7
                    top_p=top_p,
                    stream=True)
            with st.chat_message("assistant"):
                return st.write_stream(stream_data_(response_)) 
            # return response.text
        elif model_number in [3,12]:
            conv=conversation.copy()
            conv=[c for c in conv if c['role'] in ['user','system']]
            response_ = client3.chat.completions.create(
                model=models_dict[model_number], messages=conv,
                temperature=temp, 
                top_p=top_p,
                stream=False)
            print(response_)
            return response_.choices[0].message.content.strip()
            
        else:
            response = client2.chat.completions.create(
                model=models_dict[model_number], messages=conversation,
                 temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise e
        return f"Error: {e}"


# async def generate_audio(text):
#     # Replace this URL with your actual API endpoint
#     api_url = "https://openfm.onrender.com/api/generate"
#     text= {
#     "input": text,
#     "voice": "shimmer",
#     "vibe": "null",
#     "customPrompt": "Voice Affect:Fast, Mystical and dreamy\nTone: Soft and enchanting\nPacing: FastnEmotion: Whimsical and magical\nPronunciation: Smooth and ethereal\nPauses: Strategic pauses for effect"
# }
#     headers = {
#     'Content-Type': 'application/json'
# }
#     response =await requests.post(api_url, headers=headers, json=text)

#     if response.status_code == 200:
#         # print("Sound file downloaded successfully.")
#         return response.content
#     else:
#         print(f"Error: {response.status_code}")
async def generate_audio(text):
    """
    Fetches TTS audio data asynchronously from an external API.
    """
    api_url = "https://openfm.onrender.com/api/generate"
    
    payload = {
        "input": text,
        "voice": "shimmer",
        "vibe": "null",
        "customPrompt": "Voice Affect:Fast, Mystical and dreamy\n"
                        "Tone: Soft and enchanting.Also keep the ups and down's in the tone\n"
                        "Pacing:Be Fast\n"
                        "Emotion: Whimsical and magical\n"
                        "Pronunciation: Smooth and ethereal\n"
                        "Pauses: Strategic pauses for effect"
    }

    headers = {
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.content  # Return raw audio bytes
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None  # Handle failure case


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

def play_audio(file_path,col2):
    # if audio_data:
    #     # Convert audio data to base64
    #     b64 = base64.b64encode(audio_data).decode()
    #     audio_html = f"""
    #     <audio controls>
    #         <source src="data:audio/wav;base64,{b64}" type="audio/wav">
    #         Your browser does not support the audio element.
    #     </audio>
    #     """
    #     with col2:
    #         st.components.v1.html(audio_html, height=100)
    with col2:
        if file_path.endswith(".wav"):
            st.audio(file_path, format="audio/wav")
        else:
            st.audio(file_path, format="audio/mp3")
        # st.audio(file_path, format="audio/wav")  # Directly play the MP3 file
def split_text(text, max_length=980):
    sentences = re.split(r'(?<=[.!?])\s+', text)  # Split by sentence-ending punctuation
    parts = []
    current_part = ""

    for sentence in sentences:
        if len(current_part) + len(sentence) + 1 <= max_length:  # +1 for space
            current_part += " " + sentence if current_part else sentence
        else:
            parts.append(current_part.strip())  # Store the current part
            current_part = sentence  # Start a new part

    if current_part:
        parts.append(current_part.strip())  # Add the last part

    return parts




# async def generate_audio_total(text,output_filename="output.mp3"):
#     if len(text)<980:
#         return await generate_audio(text)
#     else:
#         split_parts=split_text(text)
#         combined_audio = AudioSegment.empty()
        
#         for text in split_parts:
#             # Fetch raw audio content asynchronously
#             audio_data = await generate_audio(text)
            
#             # Load the audio into a BytesIO buffer
#             mp3_fp = io.BytesIO(audio_data)
#             mp3_fp.seek(0)  # Reset pointer
            
#             # Load the audio with pydub
#             segment = AudioSegment.from_file(mp3_fp, format="mp3")
#             combined_audio += segment
            
#             mp3_fp.close()  # Close the in-memory buffer
#         if os.path.exists(output_filename):
#             os.remove(output_filename)
#         # Save to a file
#         combined_audio.export(output_filename, format="mp3")
#         print(f"Final audio saved as: {output_filename}")

async def generate_audio_total(text, output_filename="output.wav"):
    if len(text) < 980:
        audio_data= await generate_audio(text)
        output_filename='output.mp3'
        with open(output_filename, "wb") as mp3_fp:
            mp3_fp.write(audio_data)
        return output_filename
    else:
        split_parts = split_text(text)
        temp_wav_files = []
    
        for i, text_part in enumerate(split_parts):
            audio_data = await generate_audio(text_part)  # Get audio content
            mp3_filename = f"temp_part_{i}.mp3"
            with open(mp3_filename, "wb") as mp3_fp:
                mp3_fp.write(audio_data)
            mp3_fp.close()
            wav_filename = f"temp_part_{i}.wav"
            with open(mp3_filename, "rb") as f:
                mp3_data = f.read()
            decoded_audio= miniaudio.decode(mp3_data)
            pcm_data, sample_rate, num_channels=decoded_audio.samples,decoded_audio.sample_rate,decoded_audio.nchannels
            # pcm_data, sample_rate, num_channels = miniaudio.decode(audio_data)
    
            # Write PCM data into a WAV file using the wave module.
            # Here, we assume the PCM data is 16-bit.
            with wave.open(wav_filename, 'wb') as wav_file:
                wav_file.setnchannels(num_channels)
                wav_file.setsampwidth(2)  # 2 bytes for 16-bit audio
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(pcm_data)
            os.remove(mp3_filename)
            
            
            temp_wav_files.append(wav_filename)

            mp3_fp.close()

        # Merge WAV files
        with wave.open(output_filename, "wb") as output_wav:
            with contextlib.closing(wave.open(temp_wav_files[0], "rb")) as first_wav:
                output_wav.setparams(first_wav.getparams())

                for wav_file in temp_wav_files:
                    with contextlib.closing(wave.open(wav_file, "rb")) as w:
                        output_wav.writeframes(w.readframes(w.getnframes()))

        # Cleanup temporary WAV files
        for temp_file in temp_wav_files:
            os.remove(temp_file)

        print(f"Final audio saved as: {output_filename}")

        return output_filename
        # return final_mp3