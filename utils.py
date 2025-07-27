import wave
import miniaudio
import contextlib
import os
import streamlit as st
import asyncio
import re
import streamlit as st
from duckduckgo_search import DDGS
import httpx
from models_data import models_dict,get_icon_no_and_value
from providers import client_groq,google_model_numbers,get_client

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
            query_filtered = client_groq.chat.completions.create(
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
        
async def query_openai(conversation,
                       model_number=1,
                       search=False,
                       temp=0.5,
                       top_p=0.95,
                       role="Helpful Assistant",
                       system_prompt="Try to respond in a freindly manner.Also try to be concise and to the point.",
                       name="Niklesh"):
    """
    Send the conversation history to the OpenAI Chat API and return the assistant's response.
    """
    print(f'File:Utils,Got search in utils :{search}')
    respo = None
    if search:
        respo = await search_tavily(conversation)
        print(f'response is provided by tavily {respo}')
        conversation.append({
            "role":
            "user",
            "content":
            f"Additional context from recent search results: {respo}"
        })
    try:
        conv=conversation.copy()
        conv.append({
                "role":
                "user",
                "content":
                f"""
                System Instructions:
                Act as {role} and {system_prompt}.
                Adress the user with the name {name}.
    """
            })
        if model_number in google_model_numbers:
            conv.append({
                "role":
                "system",
                "content":
                """
                Instructions for output:
                1)Give the maths expressions(if exists) in perfect latex that is rendered perfectly in markdown.Don't give latex as seperate code block.Don't say that i am giving in latex rendering to user.
    """
            })
        # Getting the correct client for given request
        client,isStream=get_client(model_number)
        #Where icn_no refers to the number in the list `bot_icon_url`
        icn_no,icn_url=get_icon_no_and_value(model_number)
        st.session_state.icon_numbers.append(icn_no)
        with st.spinner(text="Thinking...."):
            response_ = client.chat.completions.create(
                model=models_dict[model_number],
                stream=isStream,
                messages=conv,
                temperature=temp,  
                top_p=top_p)
        if isStream:
            with st.chat_message("assistant",avatar=icn_url):
                return st.write_stream(stream_data_(response_)) 
        return response_.choices[0].message.content.strip()
    except Exception as e:
        return f"Error occured :{e}"



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
        response = client_groq.audio.transcriptions.create(
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