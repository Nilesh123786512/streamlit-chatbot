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
bot_icon_url="data:image/png;base64,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"
user_icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGWm7kgMH1PEsycRwkyqPcPB1b2NITpD8j2g&s"

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
    12: "openai/gpt-4.1-mini",
    11: "gemini-2.0-flash",
    13: "deepseek/deepseek-chat-v3-0324:free",
    15: "meta-llama/llama-4-maverick:free",
    9: "deepseek/deepseek-chat:free",
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
        with st.spinner("Formatting the query"):
            query = query.copy()
            query=[q for q in query if q['role'] in ['user','system']]
            query.append({
                "role":
                "system",
                "content":
                """
                Based on all above queries give me a single search query enclosed in 
                <search>content to search</search>.
                If the query was straight forward then don't modify just enclose it else from context give the best query.
                Make sure you are not response assistant rather query searcher don't respond as llm rather than give reply as a search engine query formatter.
                
                """
            })

            print(f"Changed query:{query}")
            # query_filtered.choices[0].message.content
            query_filtered = client2.chat.completions.create(
                model="deepseek-r1-distill-llama-70b", messages=query)
            print("Query filtered is :\n",query_filtered.choices[0].message.content)
            query_filtered=re.sub(r'(<think>*</think>)','',query_filtered.choices[0].message.content,flags=re.DOTALL)
            query_filtered = re.search(r'''<search>(.*?)</search>''',  query_filtered,
                                    re.DOTALL)
            print(query_filtered)
            # print("Fetching query:",query_filtered.group(1))
            # response = tavily_client.search(query_filtered.group(1))
        with st.spinner("Searching the web"):
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
    for chunker in stream:
        if len(chunker.choices) == 0:
            continue
        _cont=chunker.choices[0].delta.content
        if _cont is None:
            continue
        yield _cont
        resp+=_cont
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
            with st.chat_message("assistant",avatar=bot_icon_url):
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
            with st.chat_message("assistant",avatar=bot_icon_url):
                return st.write_stream(stream_data_(response_)) 
            # return response.text
        elif model_number in [3,12]:
            conv=conversation.copy()
            # conv=[c for c in conv if c['role'] in ['user','system']]
            response_ = client3.chat.completions.create(
                model=models_dict[model_number], messages=conv,
                temperature=temp, 
                top_p=top_p,
                stream=True)
            with st.chat_message("assistant",avatar=bot_icon_url):
                return st.write_stream(stream_data_(response_)) 
            # print(response_)
            # return response_.choices[0].message.content.strip()
            
        else:
            response = client2.chat.completions.create(
                model=models_dict[model_number], messages=conversation,
                 temperature=temp,  # Set temperature to 0.7
                top_p=top_p)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error Occured: {e}"
        # raise e


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
        # Create a list of coroutines for each text part
        audio_coroutines = [generate_audio(text_part) for text_part in split_parts]

        # Run all coroutines concurrently using asyncio.gather
        # audio_results will be a list containing the audio_data from each call,
        # in the same order as the split_parts
        print(f"Generating audio for {len(split_parts)} parts concurrently...")
        audio_results = await asyncio.gather(*audio_coroutines)
        print("All audio parts generated.")

        temp_wav_files = []

        # Now process the results sequentially (decoding and saving to WAV)
        # This part is synchronous and doesn't need to be concurrent unless it's a bottleneck
        print("Processing and converting audio parts to WAV...")
        for i, audio_data in enumerate(audio_results):
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