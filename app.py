import asyncio
from utils import query_openai, models_dict
import streamlit as st
import re
import time
from utils import generate_audio_total, play_audio,replacer

models_dict_reversed = {value: key for key, value in models_dict.items()}

st.set_page_config(
    page_title="My Chatbot",
    # page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
long_context_models=[1,9,10,13,11,12,14,15,16]

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
        st.session_state.conversation = [{
            "role": "system",
            "content": "You are a helpful and concise assistant. Your primary goal is to directly address the user's most recent question or statement.  Use the preceding conversation history to understand the context and provide relevant background, but always ensure your response is primarily focused on and answers the *latest user input*.  If there are any ambiguities or contradictions between past messages and the latest message, assume the latest message is the most accurate representation of the user's current intent.f you retrieve search results while responding, please provide links that you got as it is,don't hallucinate links"
        }]
    if "input" not in st.session_state:
        st.session_state.input = [{
            "role": "system",
            "content": "You are a helpful and concise assistant. Your primary goal is to directly address the user's most recent question or statement.  Use the preceding conversation history to understand the context and provide relevant background, but always ensure your response is primarily focused on and answers the *latest user input*.  If there are any ambiguities or contradictions between past messages and the latest message, assume the latest message is the most accurate representation of the user's current intent.f you retrieve search results while responding, please provide links that you got as it is,don't hallucinate links"
        }]

    with st.sidebar:
        st.session_state.temp = st.slider("Temperature",0., 2.,0.6)
        st.session_state.top_p = st.slider("Top_p",0., 1.,0.95)



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
                st.rerun()
        with col1:
            search = st.toggle("Search")
        user_message = st.chat_input("Type your message here...")

    with hist_container:
        _ind=0
        for chat in st.session_state.conversation:
            if chat["role"] == "user":
                user_msg = st.chat_message("user")
                # st.markdown("### You")
                user_msg.text(f"{chat['content']}")
            elif chat["role"] == "assistant":
                _ind+=1
                thoughts_match = re.search(r'''<think>(.*?)</think>''',
                                        chat['content'], re.DOTALL)
                main_content = re.sub(r'''<think>.*?</think>''',
                                    '',
                                    chat['content'],
                                    flags=re.DOTALL)
                # st.markdown("### Bot")
                if thoughts_match:
                    thoughts = thoughts_match.group(1)
                    thoughts = re.sub(r"\\\[\s*", "$$", thoughts)
                    thoughts = re.sub(r"\s*\\\]", "$$", thoughts)
                    thoughts = re.sub(r"\\\(\s*", "$", thoughts)
                    thoughts = re.sub(r"\s*\\\)", "$", thoughts)
                    with st.expander("Thoughts"):
                        st.write(thoughts)
                # print(main_content)
                # print(main_content)
        # main_content = re.sub(r"\\\[\s(.*?)\s\\\]", "$$\1$$", main_content)
                # main_content = re.sub(r"\\\[\s*", "$$", main_content)
                # main_content = re.sub(r"\\\(\s*", "$", main_content)
                # main_content = re.sub(r"\s*\\\)", "$", main_content)
                pattern_of_re = r"(```.*?```)|(\\\(\s*)|(\s*\\\))"
                main_content=re.sub(pattern_of_re, replacer, main_content, flags=re.DOTALL)
                bot_message= st.chat_message("assistant")
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
                            # play_audio("output.wav",col2)
                            play_audio(fil_audio_name,col2)
                    # Add regenerate button
                with colrerun:
                    model_number = models_dict_reversed.get(model)
                    if st.button("🔄", key=f"regenerate_{_ind}", help="Regenerate this response"):
                        # last_user_msg = next((msg for msg in reversed(st.session_state.conversation) if msg["role"] == "user"), None)
                        # if last_user_msg:
                        if model_number in [9,13,11,10,14]:
                            response = asyncio.run(query_openai(
                                st.session_state.conversation,
                                model_number,
                                search=search,
                                temp=st.session_state.temp,
                                top_p=st.session_state.top_p
                            ))
                            st.session_state.conversation[-1]["content"] = response
                            st.rerun()
                        else:
                            response = asyncio.run(query_openai(
                                st.session_state.input,
                                model_number,
                                search=search,
                                temp=st.session_state.temp,
                                top_p=st.session_state.top_p
                            ))
                            st.session_state.conversation[-1]["content"] = response
                            st.rerun()





    
    if user_message:
        st.session_state.conversation.append({
            "role": "user",
            "content": user_message
        })
        st.session_state.input.append({"role": "user", "content": user_message})
        with new_reply_container:

            user_msg = st.chat_message("user")
            user_msg.text(user_message)

            # bot_message.write('thinking')

            model_number = models_dict_reversed.get(model)
            # Set think flag based on model_number.
            if model_number in [2, 3, 4]:
                st.session_state.think = True
            else:
                st.session_state.think = False

            # Query the model
            # ass_message_place = st.empty()
            # with ass_message_place.container():

                # Define the CSS for the blinking effect
            if not model_number in long_context_models:
                bot_message=st.chat_message("assistant")
                blink_css = """
                <style>
                @keyframes blink {
                    0% { opacity: 1; }
                    50% { opacity: 0; }
                    100% { opacity: 1; }
                }
                .blink {
                    animation: blink 1s infinite;
                }
                </style>
                """

                # Apply the CSS
                # bot_message.markdown(blink_css, unsafe_allow_html=True)

                # Display blinking text
                # st.markdown('<p class="blink">This text will blink</p>', unsafe_allow_html=True)

                bot_message.markdown(blink_css+'<p class="blink">Thinking</p>',
                            unsafe_allow_html=True)
            # print(search)
            # print("all ready to send to AI")
            print(f'Searching is kept : {search}')
            if model_number in long_context_models:
                response =asyncio.run(query_openai(st.session_state.conversation,
                                        model_number,
                                        search=search,
                                    temp=st.session_state.temp,
                                    top_p=st.session_state.top_p)
                                    )
            else:
                response =asyncio.run(query_openai(st.session_state.input,
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

                
    

    