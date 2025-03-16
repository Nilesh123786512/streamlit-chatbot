# 🤖 My Chatbot: A Versatile Conversational AI 🧠

This project is a Streamlit-based chatbot application that leverages the power of various Large Language Models (LLMs) from different providers like Groq and Sree Shop, along with web search capabilities from Tavily. 🌐  It's designed to be a helpful and versatile assistant, ready to answer your questions, provide information, and engage in dynamic conversations. 💬

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
*   **Web Search Integration:** 🔍  Utilizes the Tavily API to perform real-time web searches, allowing the chatbot to gather up-to-date information and provide contextually relevant responses.
*   **Dynamic Conversation:** 🗣️ Maintains conversation history to provide more accurate and context-aware answers.
*   **Customizable Settings:** ⚙️
    *   **Temperature:** 🔥❄️ Adjust the randomness of the model's responses (0.0 = deterministic, 2.0 = highly random).
    *   **Top-p:** 📊 Control the diversity of responses (lower values = more focused).
*   **LaTeX Support:** 🧮 The chatbot can render LaTeX expressions within its responses, making it useful for mathematical and scientific discussions.
*   **Thoughts:** 💭 Some models present their intermediate "thoughts" process of how they came up with the response.
*   **New Chat Button:** 🔄 Clear the conversation history and start a fresh chat with a single click.
*   **Search toggle:** 🌐 if you want the bot to make a search about your last query, you can toggle on the search option.

## Getting Started 🚀

### Prerequisites

*   **Python 3.8+** 🐍
*   **Pip** (Python package installer) 📦
*   **API Keys:** 🔑
    *   Devs Do Code API Key
    *   Groq API Key
    *   Tavily API Key

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

3.  **Set up API Keys:** 🗝️

    *   **Option 1: `.streamlit/secrets.toml` (Recommended)**
        *   Create a directory named `.streamlit` in the project's root.
        *   Inside `.streamlit`, create a file named `secrets.toml`.
        *   Add your API keys:

            ```toml
            devsdocode = "YOUR_DEVS_DO_CODE_API_KEY"
            groq_api = "YOUR_GROQ_API_KEY"
            tavily_1 = "YOUR_TAVILY_API_KEY"
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

1.  **Select a Model:** Choose from the dropdown menu to change the underlying LLM. ⬇️
2.  **Adjust Settings:** Use the sliders in the sidebar to fine-tune the `Temperature` and `Top_p` parameters. ⚙️
3.  **Chat:** Type your messages in the chat input box and press Enter. 💬
4.  **New Chat:** Click the "New Chat" button to reset the conversation history. 🔄
5.  **Search**: Toggle the search option if you want the bot to search for the topic. 🌐

## Project Structure 🏗️

*   `app.py`: The main Streamlit application code, handling the UI, user input, and model interaction. 🖥️
*   `utils.py`: Contains utility functions for interacting with the OpenAI and Tavily APIs, including model selection, web search, and response formatting. 🛠️
*   `requirements.txt`: Lists all Python dependencies required for the project. 📚
*   `.streamlit/secrets.toml`: (Optional) Stores sensitive API keys. 🤫
*   `README.md`: This file, providing project documentation. 📄
*   `.gitignore`: tells git what file to ignore. 🙈

## Contributing 🤝

If you'd like to contribute to this project, please feel free to fork the repository and submit pull requests. 🙌

## License 📜

This project is open-source and available under the [MIT License](LICENSE) (Replace `[MIT License]` and add a `LICENSE` file if applicable).

## Contact ✉️

*   [Nikilesh]
*   [nikileshthotamsettyhrank@gmail.com]
*   [Nilesh123786512]

---
**Disclaimer:** ⚠️ Please be aware of the terms of service and potential costs associated with using the Groq, Sree Shop, and Tavily APIs.
# streamlit-chatbot