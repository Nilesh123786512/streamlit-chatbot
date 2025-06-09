# 🤖 My Chatbot: A Versatile Conversational AI 🧠

This project is a Streamlit-based chatbot application that leverages the power of various Large Language Models (LLMs) from different providers like Groq and Sree Shop, along with web search capabilities from DuckDuckGo Search. 🌐 It's designed to be a helpful and versatile assistant, ready to answer your questions, provide information, and engage in dynamic conversations. 💬

## Key Features ✨

*   **Multi-Model Support:** 🎛️ The chatbot supports a wide range of LLMs, including:
    *   `qwen-qwq-32b`
    *   `qwen-2.5-32b`
    *   `qwen-2.5-coder-32b`
    *   `deepseek-r1-distill-qwen-32b`
    *   `deepseek-r1-distill-llama-70b`
    *   `deepseek-r1`
    *   `deepseek-v3`
    *   `claude-3-5-sonnet-20240620`
    *   `gpt-4o-2024-05-13`
    *   *(and many more as defined in `models_data.py`)*
*   **Authentication:** 🔐 Secure access to the chatbot using a configurable secret code.
*   **Web Search Integration:** 🔍 Utilizes DuckDuckGo Search to perform real-time web searches, with query formatting powered by Groq models, allowing the chatbot to gather up-to-date information and provide contextually relevant responses.
*   **Dynamic Conversation:** 🗣️ Maintains conversation history to provide more accurate and context-aware answers.
*   **Save/Load Chat History:** 💾 Automatically saves and loads conversation history and bot icons to/from `history/conversation.json` and `history/icons.json` respectively, allowing you to resume chats.
*   **Audio Response Generation:** 🔊 Generate and play audio versions of the chatbot's responses, enhancing accessibility and user experience.
*   **Audio Transcription:** 🎤 Transcribe user audio input using Groq's `whisper-large-v3-turbo` model (though this feature is not directly exposed in the UI, the capability exists in `utils.py`).
*   **Regenerate Response:** 🔄 Easily regenerate the last assistant response if you're not satisfied with the initial output.
*   **Customizable Settings:** ⚙️
    *   **Temperature:** 🔥❄️ Adjust the randomness of the model's responses (0.0 = deterministic, 2.0 = highly random).
    *   **Top-p:** 📊 Control the diversity of responses (lower values = more focused).
*   **LaTeX Support:** 🧮 The chatbot can render LaTeX expressions within its responses, making it useful for mathematical and scientific discussions.
*   **Thoughts:** 💭 Some models present their intermediate "thoughts" process of how they came up with the response.
*   **New Chat Button:** 🔄 Clear the conversation history and start a fresh chat with a single click.
*   **Search toggle:** 🌐 If you want the bot to make a search about your last query, you can toggle on the search option.

## Getting Started 🚀

### Prerequisites

*   **Python 3.8+** 🐍
*   **Pip** (Python package installer) 📦
*   **API Keys:** 🔑
    *   Devs Do Code API Key
    *   Groq API Key
    *   Tavily API Key (Note: While Tavily is mentioned, the current implementation uses DuckDuckGo Search. This key is for  older implementation.)
    *   **Authentication Code:** A secret code for accessing the chatbot.

### Installation

1.  **Clone the repository:** ⬇️

    ```bash
    git clone https://github.com/Nilesh123786512/streamlit-chatbot.git
    cd streamlit-chatbot
    ```


2.  **Install dependencies:** 🛠️

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up API Keys and Authentication Code:** 🗝️

    *   **Option 1: `.streamlit/secrets.toml` (Recommended)**
        *   Create a directory named `.streamlit` in the project's root.
        *   Inside `.streamlit`, create a file named `secrets.toml`.
        *   Add your API keys and authentication code:

            ```toml
            devsdocode = "YOUR_DEVS_DO_CODE_API_KEY"
            groq_api = "YOUR_GROQ_API_KEY"
            tavily_1 = "YOUR_TAVILY_API_KEY" # May not be actively used in current search implementation
            auth_code = "YOUR_SECRET_AUTHENTICATION_CODE"
            ```
          
        * **Important** Add `.streamlit/secrets.toml` to your `.gitignore` file.
        
    *   **Option 2: Streamlit Cloud Secrets (If deploying to Streamlit Cloud)** ☁️
        *   If you're deploying to Streamlit Cloud, you can add your secrets directly in the Streamlit Cloud dashboard under `Settings > Secrets`.

4.  **Run the app:** ▶️

    ```bash
    streamlit run app.py
    ```

    This will launch the chatbot in your web browser.

## Usage 🕹️

1.  **Authenticate:** Enter the secret code to gain access to the chatbot. 🔐
2.  **Select a Model:** Choose from the dropdown menu to change the underlying LLM. ⬇️
3.  **Adjust Settings:** Use the sliders in the sidebar to fine-tune the `Temperature` and `Top_p` parameters. ⚙️
4.  **Chat:** Type your messages in the chat input box and press Enter. 💬
5.  **Save Chat:** Click the "Save Chat" button in the sidebar to save your current conversation history. 💾
6.  **Generate Audio:** Click the "🔊" button next to an assistant's response to generate and play its audio. 🗣️
7.  **Regenerate Response:** Click the "🔄" button next to an assistant's response to get a new response for the last query. 🔄
8.  **New Chat:** Click the "New Chat" button to reset the conversation history. 🔄
9.  **Search**: Toggle the search option if you want the bot to search for the topic. 🌐

## Project Structure 🏗️

*   `app.py`: The main Streamlit application code, handling the UI, user input, model interaction, and chat history management. 🖥️
*   `utils.py`: Contains utility functions for web search, audio generation/transcription, and interacting with LLM APIs. 🛠️
*   `models_data.py`: Defines the available LLM models, their mapping to providers, and icon associations. 📊
*   `providers.py`: Manages the API clients for different LLM providers (e.g., Groq, Google). 🔌
*   `requirements.txt`: Lists all Python dependencies required for the project. 📚
*   `.streamlit/secrets.toml`: (Optional) Stores sensitive API keys and authentication code. 🤫
*   `history/`: Directory for saving and loading conversation history (`conversation.json`) and bot icons (`icons.json`). 📜
*   `audio/`: Directory for storing generated audio files. 🔊
*   `icons/`: Directory for storing bot icon images. 🖼️
*   `README.md`: This file, providing comprehensive project documentation. 📄
*   `.gitignore`: Tells Git which files to ignore. 🙈

## Updating Models and `models_data.py` 🛠️

The chatbot's supported models and their associated icons are managed in the `models_data.py` file. Follow these instructions to update or add new models:

### 1. Modifying `models_dict`

The `models_dict` dictionary maps an integer `model_number` to a string `model_name`. To add a new model or update an existing one:

*   **Add a new model:** Choose a unique integer as the key and assign the model's string identifier as its value.
    ```python
    models_dict = {
        # ... existing models
        99: "new-provider/new-model-name",
    }
    ```
*   **Update an existing model:** Change the `model_name` associated with an existing `model_number`.

### 2. Assigning Models to Provider Lists

After adding a new model to `models_dict`, you must assign its `model_number` to the appropriate provider list (e.g., `gemini_model_numbers`, `chatgpt_model_numbers`, `deepseek_model_numbers`, `claude_model_numbers`). This ensures the correct icon is displayed for the model.

For example, if `model_number` 99 is a new Gemini model:

```python
gemini_model_numbers = [11, 14, 17, 1, 99] # Add 99 to the list
```

If you are adding a model from a new provider, you will need to create a new list for that provider.

### 3. Updating `bot_icon_url` (if needed)

The `bot_icon_url` list contains paths to the icons used for different model providers. If you introduce a new provider and have a corresponding icon, add its path to this list.

```python
bot_icon_url = [
    "icons/gemini.png",
    "icons/chatgpt.png",
    "icons/deepseek.png",
    "https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/claude-ai-icon.png",
    None,
    "icons/new_provider_icon.png" # Add new icon path
]
```

### 4. Updating `get_icon_no_and_value` (if needed)

If you've added a new provider list and a corresponding icon, you'll need to update the `get_icon_no_and_value` function to handle the new provider. Add a new `elif` condition to check if the `model_number` belongs to your new provider list and return the appropriate icon index and URL.

```python
def get_icon_no_and_value(model_number):
    # ... existing conditions
    elif model_number in new_provider_model_numbers: # Assuming new_provider_model_numbers is your new list
        return 5, bot_icon_url[5] # Use the index corresponding to your new icon in bot_icon_url
    else:
        return 4, bot_icon_url[4] # Default or None icon
```

## Contributing 🤝

If you'd like to contribute to this project, please feel free to fork the repository and submit pull requests. 🙌

## License 📜

This project is open-source and available under the [MIT License](LICENSE) (Replace `[MIT License]` and add a `LICENSE` file if applicable).

## Contact ✉️

*   [Nikilesh]
*   [nikileshthotamsettyhrank@gmail.com]
*   [Nilesh123786512]

---
**Disclaimer:** ⚠️ Please be aware of the terms of service and potential costs associated with using the Groq, a4f, and Tavily APIs.
# streamlit-chatbot
