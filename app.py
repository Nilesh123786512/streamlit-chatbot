import asyncio
from utils import query_openai
from models_data import models_dict
import streamlit as st
import re
import time
import json # Added for JSON operations
import os   # Added for path operations
from utils import generate_audio_total, play_audio,replacer
models_dict_reversed = {value: key for key, value in models_dict.items()}
from models_data import user_icon_url, bot_icon_url,get_icon_no_and_value
# --- Helper Functions for JSON ---
def ensure_history_dir_exists():
    if not os.path.exists(HISTORY_DIR):
        try:
            os.makedirs(HISTORY_DIR)
        except OSError as e:
            st.error(f"Error creating directory {HISTORY_DIR}: {e}")

def save_to_json(filename, data):
    ensure_history_dir_exists()
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        # st.sidebar.success(f"Data saved to {filename}") # Optional: uncomment for verbose feedback
    except Exception as e:
        st.sidebar.error(f"Error saving to {filename}: {e}")

def load_from_json(filename):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                return data
    except FileNotFoundError:
        # File not existing is a valid case for first run, so no error message here.
        return None
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from {filename}. File might be corrupted. Using default.")
        return None
    except Exception as e:
        st.error(f"Error loading from {filename}: {e}. Using default.")
        return None
    return None

# --- Constants for File Paths ---
HISTORY_DIR = "history"
CONVERSATION_FILE = os.path.join(HISTORY_DIR, "conversation.json")
ICONS_FILE = os.path.join(HISTORY_DIR, "icons.json")

# --- System Prompt Definitions ---
DEFAULT_SYSTEM_MESSAGE_CONTENT = "You are a helpful and concise assistant. Your primary goal is to directly address the user's most recent question or statement.  Use the preceding conversation history to understand the context and provide relevant background, but always ensure your response is primarily focused on and answers the *latest user input*.  If there are any ambiguities or contradictions between past messages and the latest message, assume the latest message is the most accurate representation of the user's current intent.if you retrieve search results while responding, please provide links that you got as it is,don't hallucinate links"
DEFAULT_SYSTEM_PROMPT = {"role": "system", "content": DEFAULT_SYSTEM_MESSAGE_CONTENT}

NEW_CHAT_SYSTEM_MESSAGE_CONTENT = "You are a helpful assistant."
NEW_CHAT_SYSTEM_PROMPT = {"role": "system", "content": NEW_CHAT_SYSTEM_MESSAGE_CONTENT}
st.set_page_config(
    page_title="My Chatbot",
    # page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
long_context_models=[1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,23]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
# --- Secret Code ---
SECRET_CODE = st.secrets["auth_code"]# Replace with your desired secret code

# --- Session State ---


# --- Authentication Function ---
def authenticate(code):
    if code == SECRET_CODE:
        st.session_state.authenticated = True
        return True
    else:
        st.error("Incorrect code. Please try again.")
        return False

# --- Login Page ---
if not st.session_state.authenticated:
    st.title("🔐 Chatbot Access")
    st.write("Please enter the secret code to access the chatbot.")

    code_input = st.text_input("Secret Code", type="password")
    if st.button("Submit"):
        if authenticate(code_input):
            st.rerun()
if st.session_state.authenticated:
    st.title("🤖 My Chatbot")

    # Initialize session state for conversation if not already present
    if "conversation" not in st.session_state:
        loaded_conversation = load_from_json(CONVERSATION_FILE)
        if loaded_conversation and isinstance(loaded_conversation, list) and len(loaded_conversation) > 0:
            st.session_state.conversation = loaded_conversation
        else:
            st.session_state.conversation = [DEFAULT_SYSTEM_PROMPT.copy()]

    if "input" not in st.session_state:
        # 'input' uses the same default system message initially.
        # It will be reset with NEW_CHAT_SYSTEM_PROMPT if "New Chat" is clicked.
        st.session_state.input = [conv for conv in st.session_state.conversation if conv["role"] in ["system", "user"]]

    if "icon_numbers" not in st.session_state:
        loaded_icons = load_from_json(ICONS_FILE)
        if loaded_icons and isinstance(loaded_icons, list):
            st.session_state.icon_numbers = loaded_icons
        else:
            st.session_state.icon_numbers = []

    with st.sidebar:
        st.session_state.temp = st.slider("Temperature", 0., 2., 0.6)
        st.session_state.top_p = st.slider("Top_p", 0., 1., 0.95)

        if st.button("Save Chat"):
            save_to_json(CONVERSATION_FILE, st.session_state.conversation)
            save_to_json(ICONS_FILE, st.session_state.icon_numbers)
            st.sidebar.success("Chat saved!")
    hist_container = st.container()
    new_reply_container = st.container()
    main_container = st.container()
    with main_container:
        # Use columns only for the selectbox (chat input stays outside)
        col1, col3, _, col2 = st.columns(
            [1, 2, 1, 1],
            vertical_alignment="bottom"
        )  # Underscore ignores the second column

        with col3:
            model = st.selectbox("Select a Model", list(models_dict.values()))
        with col2:
            # "New Chat" button on the right
            if st.button("New Chat"):
                st.session_state.conversation = [{
                    "role":
                    "system",
                    "content":
                    "You are a helpful assistant."
                }]
                st.session_state.input = [{
                    "role": "system",
                    "content": "You are a helpful assistant."
                }]
                st.session_state.icon_numbers = []
                st.rerun()
        with col1:
            search = st.toggle("Search")
        user_message = st.chat_input("Type your message here...")

    with hist_container:
        _ind=0
        for chat in st.session_state.conversation:
            if chat["role"] == "user":
                user_msg = st.chat_message("user",avatar=user_icon_url)
                user_msg.text(f"{chat['content']}")
            elif chat["role"] == "assistant":
                _ind+=1
                thoughts_match = re.search(r'''<think>(.*?)</think>''',
                                        chat['content'], re.DOTALL)
                main_content = re.sub(r'''<think>.*?</think>''',
                                    '',
                                    chat['content'],
                                    flags=re.DOTALL)
                if thoughts_match:
                    thoughts = thoughts_match.group(1)
                    thoughts = re.sub(r"\\\[\s*", "$$", thoughts)
                    thoughts = re.sub(r"\s*\\\]", "$$", thoughts)
                    thoughts = re.sub(r"\\\(\s*", "$", thoughts)
                    thoughts = re.sub(r"\s*\\\)", "$", thoughts)
                    with st.expander("Thoughts"):
                        st.write(thoughts)
                # main_content = re.sub(r"\\\[\s*", "$$", main_content)
                # main_content = re.sub(r"\\\(\s*", "$", main_content)
                # main_content = re.sub(r"\s*\\\)", "$", main_content)
                pattern_of_re = r"(```.*?```)|(\\\(\s*)|(\s*\\\))"
                main_content=re.sub(pattern_of_re, replacer, main_content, flags=re.DOTALL)
                # Bot icons are stored according to index of assistant messages and using them now
                ic_url=bot_icon_url[st.session_state.icon_numbers[_ind-1]]
                bot_message= st.chat_message("assistant",avatar=ic_url)
                # main_content = re.sub(r"\s*\\\]", "$$", main_content)
                latex_blocks = re.findall(r"\\\[(.*?)\\\]", main_content, re.DOTALL)
                # Split text around LaTeX expressions
                split_text = re.split(r"\\\[(.*?)\\\]", main_content, flags=re.DOTALL)
                split_text=[_tex for _tex in split_text if _tex not in latex_blocks]
                col1,colrerun,_,col2=st.columns([0.10,0.12,0.7,0.7])
                # Render content correctly
                for i in range(len(split_text)):
                    bot_message.markdown(split_text[i])  # Render text normally
                    if i < len(latex_blocks):  
                        bot_message.latex(latex_blocks[i].strip())
                
                with col1:
                    if st.button("🔊", key=f"audio_button_{_ind}"):
                        str=" ".join(split_text)
                        fil_audio_name=asyncio.run(generate_audio_total(str))
                        with col2:
                            play_audio(fil_audio_name,col2)
                    # Add regenerate button
                with colrerun:
                    model_number = models_dict_reversed.get(model)
                    if st.button("🔄", key=f"regenerate_{_ind}", help="Regenerate this response"):
                        #removing the last  bot message
                        st.session_state.conversation.pop()
                        st.session_state.icon_numbers.pop()
                        if model_number in long_context_models:
                            response = asyncio.run(query_openai(
                                st.session_state.conversation,
                                model_number,
                                search=search,
                                temp=st.session_state.temp,
                                top_p=st.session_state.top_p
                            ))
                            # Adding the new response to the conversation
                            st.session_state.conversation.append({
                                "role": "assistant",
                                "content": response
                            })
                            st.rerun()
                        else:
                            response = asyncio.run(query_openai(
                                st.session_state.input,
                                model_number,
                                search=search,
                                temp=st.session_state.temp,
                                top_p=st.session_state.top_p
                            ))
                            # Adding the new response to the conversation
                            st.session_state.conversation.append({
                                "role": "assistant",
                                "content": response
                            })
                            st.rerun()





    
    if user_message:
        st.session_state.conversation.append({
            "role": "user",
            "content": user_message
        })
        st.session_state.input.append({"role": "user", "content": user_message})
        with new_reply_container:

            user_msg = st.chat_message("user",avatar=user_icon_url)
            user_msg.text(user_message)

            # bot_message.write('thinking')

            model_number = models_dict_reversed.get(model)
            # Set think flag based on model_number.
            if model_number in [2, 3, 4]:
                st.session_state.think = True
            else:
                st.session_state.think = False


            
            if model_number in long_context_models:
                _conv=st.session_state.conversation
            else:
                _conv=st.session_state.input
            response =asyncio.run(query_openai(_conv,
                                    model_number,
                                    search=search,
                                temp=st.session_state.temp,
                                top_p=st.session_state.top_p)
                                )

            st.session_state.conversation.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
