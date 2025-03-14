import asyncio
from utils import query_openai, models_dict
import streamlit as st
import re
import time
models_dict_reversed = {value: key for key, value in models_dict.items()}

st.set_page_config(
    page_title="My Chatbot",
    # page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
# --- Secret Code ---
SECRET_CODE = st.secrets["auth_code"]# Replace with your desired secret code

# --- Session State ---


# --- Authentication Function ---
def authenticate(code):
    if code == SECRET_CODE:
        st.session_state.authenticated = True
    else:
        st.error("Incorrect code. Please try again.")


# --- Login Page ---
if not st.session_state.authenticated:
    st.title("🔐 Chatbot Access")
    st.write("Please enter the secret code to access the chatbot.")

    code_input = st.text_input("Secret Code", type="password")
    if st.button("Submit"):
        authenticate(code_input)
        st.rerun()
if st.session_state.authenticated:
    st.title("🤖 My Chatbot")
    # Initialize session state for conversation if not already present
    if "conversation" not in st.session_state:
        st.session_state.conversation = [{
            "role": "system",
            "content": "You are a helpful assistant."
        }]
    if "input" not in st.session_state:
        st.session_state.input = [{
            "role": "system",
            "content": "You are a helpful and concise assistant. Your primary goal is to directly address the user's most recent question or statement.  Use the preceding conversation history to understand the context and provide relevant background, but always ensure your response is primarily focused on and answers the *latest user input*.  If there are any ambiguities or contradictions between past messages and the latest message, assume the latest message is the most accurate representation of the user's current intent."
        }]

    with st.sidebar:
        st.session_state.temp = st.slider("Temperature",0., 2.,0.75)
        st.session_state.top_p = st.slider("Top_p",0., 1.,0.95)
        
        
        # st.title("Example: Controlling sidebar programmatically")
    # Model selection dropdown
    # model = st.selectbox("Select a model:", list(models_dict.values()))
    st.title("My Chatbot")


    hist_container = st.container()
    with hist_container:
        for chat in st.session_state.conversation:

            if chat["role"] == "user":
                user_msg = st.chat_message("user")
                # st.markdown("### You")
                user_msg.text(f"{chat['content']}")
            elif chat["role"] == "assistant":
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
                main_content = re.sub(r"\\\(\s*", "$", main_content)
                main_content = re.sub(r"\s*\\\)", "$", main_content)
                bot_message= st.chat_message("assistant")
                # main_content = re.sub(r"\s*\\\]", "$$", main_content)
                latex_blocks = re.findall(r"\\\[(.*?)\\\]", main_content, re.DOTALL)

                # Split text around LaTeX expressions
                split_text = re.split(r"\\\[(.*?)\\\]", main_content, flags=re.DOTALL)

                # Render content correctly
                for i in range(len(split_text)):
                    bot_message.markdown(split_text[i])  # Render text normally
                    if i < len(latex_blocks):  
                        bot_message.latex(latex_blocks[i].strip()) 
                # print(main_content)
                # bot_message.markdown(main_content)



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

    if user_message:
        st.session_state.conversation.append({
            "role": "user",
            "content": user_message
        })
        st.session_state.input.append({"role": "user", "content": user_message})
        with new_reply_container:
            # Append user message only if it exists.
            # st.markdown("### You"
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
            ass_message_place = st.empty()
            with ass_message_place.container():

                # Define the CSS for the blinking effect
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
                st.markdown(blink_css, unsafe_allow_html=True)

                # Display blinking text
                # st.markdown('<p class="blink">This text will blink</p>', unsafe_allow_html=True)

                st.markdown('<p class="blink">Thinking</p>',
                            unsafe_allow_html=True)

            # print("all ready to send to AI")
            response =asyncio.run(query_openai(st.session_state.input,
                                    model_number,
                                    search=search,
                                temp=st.session_state.temp,
                                top_p=st.session_state.top_p)
                                )
            # if response[1] is not None:
            #     st.session_state.input.append({
            #         "role": "system",
            #         "content": f"The search results provided for context {response[1]}"
            # })
            st.session_state.conversation.append({
                "role": "assistant",
                "content": response
            })
            st.rerun()