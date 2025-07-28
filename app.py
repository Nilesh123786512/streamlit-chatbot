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
DEFAULT_SYSTEM_MESSAGE_CONTENT = "You are a helpful and concise assistant."
DEFAULT_SYSTEM_PROMPT = {"role": "system", "content": DEFAULT_SYSTEM_MESSAGE_CONTENT}

NEW_CHAT_SYSTEM_MESSAGE_CONTENT = "You are a helpful assistant."
NEW_CHAT_SYSTEM_PROMPT = {"role": "system", "content": NEW_CHAT_SYSTEM_MESSAGE_CONTENT}
st_page_icon="data:image/png;base64,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"
st.set_page_config(
    page_title="My Chatbot",
    layout="wide",
    page_icon="icons/default.png",
    initial_sidebar_state="expanded",
)
long_context_models=[1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,23, 24, 25]

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
    st.markdown(f"""
        <div style="display: flex; gap: 20px; align-items: center; justify-content: center;  " >
            <div>
                <img src="{st_page_icon}" width="60" style="border-radius: 15px; " >
            </div>
            <div>
                <h1>My Chatbot</h1>
            </div>
        </div>
        <hr>
        """, unsafe_allow_html=True)
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
        st.session_state.username=st.text_input(label="Name chatbot need to adress you ",value="Nikilesh")
        st.session_state.role=st.text_input(label="Role for your chatbot",value="Helpful Assistant")
        st.session_state.system_prompt=st.text_input(label="System prompt you need to give",value="Try to be concise.User is an undergraduate student.He is so intrested in learning about AI and ML. ")
        st.session_state.temp = st.slider("Temperature", 0., 2., 0.6)
        st.session_state.top_p = st.slider("Top_p", 0., 1., 0.95)
        st.session_state.reasoning_effort=st.selectbox(label="Reasoning effort",options=["low", "medium", "high","none","default",None],index=2)
        if st.button("New Chat",key="new_chat_button_SIDEBAR"):
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
                
                st_did_rerun=False
                with col1:
                    if st.button("🔊", key=f"audio_button_{_ind}"):
                        str=" ".join(split_text)
                        fil_audio_name=asyncio.run(generate_audio_total(str))
                        with col2:
                            play_audio(fil_audio_name,col2)
                    # Add regenerate button
                with colrerun:
                    if st.button("🔄", key=f"regenerate_{_ind}", help="Regenerate this response"):
                        st_did_rerun=True
                if st_did_rerun:
                        model_number = models_dict_reversed.get(model)
                        #removing the last  bot message
                        st.session_state.conversation.pop()
                        st.session_state.icon_numbers.pop()
                        if model_number in long_context_models:
                            _conv=st.session_state.conversation
                        else:
                            _conv=st.session_state.input

                        response = asyncio.run(query_openai(
                            _conv,
                            model_number,
                            search=search,
                            temp=st.session_state.temp,
                            top_p=st.session_state.top_p,
                            role=st.session_state.role,
                            system_prompt=st.session_state.system_prompt,
                            name=st.session_state.username,
                            reasoning_effort=st.session_state.reasoning_effort
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
                                top_p=st.session_state.top_p,
                                role=st.session_state.role,
                                system_prompt=st.session_state.system_prompt,
                                name=st.session_state.username,
                                reasoning_effort=st.session_state.reasoning_effort),
                                )

            st.session_state.conversation.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()
