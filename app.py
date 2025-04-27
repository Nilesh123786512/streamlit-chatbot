import asyncio
from utils import query_openai, models_dict
import streamlit as st
import re
import time
from utils import generate_audio_total, play_audio,replacer
bot_icon_url="data:image/png;base64,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"
user_icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGWm7kgMH1PEsycRwkyqPcPB1b2NITpD8j2g&s"
models_dict_reversed = {value: key for key, value in models_dict.items()}

st.set_page_config(
    page_title="My Chatbot",
    # page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)
long_context_models=[1,2,3,9,10,11,12,13,14,15,16,17]

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
                user_msg = st.chat_message("user",avatar=user_icon_url)
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
                bot_message= st.chat_message("assistant",avatar=bot_icon_url)
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

                
    

    