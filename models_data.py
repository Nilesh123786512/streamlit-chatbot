models_dict = {
    8: "provider-4/gpt-4o",
    19: "provider-4/gpt-4.1",
    12: "openai/gpt-4.1-mini",
    11: "gemini-2.0-flash",
    9: "deepseek/deepseek-chat:free",
    17: "gemini-2.5-flash-preview-05-20",
    7: "provider-1/deepseek-ai/DeepSeek-R1",
    5: "provider-1/deepseek-ai/DeepSeek-V3",
    6: "provider-1/deepseek-ai/DeepSeek-V3-0324",
    14:"provider-4/gemini-2.5-pro-preview-05-06",
    16: "provider-4/claude-3.7-sonnet",
    18: "provider-4/claude-3.5-haiku",
    1: "gemini-2.0-flash-thinking-exp-1219",
    3: "openai/gpt-4.1",
    13: "deepseek/deepseek-chat-v3-0324:free",
    15: "meta-llama/llama-4-maverick:free",
    2: "nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
    0: "qwen-qwq-32b",
    4: "deepseek-r1-distill-llama-70b",
    10: "deepseek/deepseek-r1:free",
}
bot_icon_url=["icons/gemini.png",
              "icons/chatgpt.png",
              "icons/deepseek.png",
              None]#"icons/default.png"]
user_icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGWm7kgMH1PEsycRwkyqPcPB1b2NITpD8j2g&s"


gemini_model_numbers=[11,14,17,1]
chatgpt_model_numbers=[12,3,8,19]
deepseek_model_numbers=[13,9,4,10,5,6,7]


def get_icon_no_and_value(model_number):
    """
    Get the icon number and value for a given model number.

    Args:
        model_number (int): The model number.

    Returns:
        tuple: A tuple containing the icon number and value.
    """

    if model_number in gemini_model_numbers:
        return 0, bot_icon_url[0]
    elif model_number in chatgpt_model_numbers:
        return 1, bot_icon_url[1]
    elif model_number in deepseek_model_numbers:
        return 2, bot_icon_url[2]
    else:
        return 3, bot_icon_url[3]
