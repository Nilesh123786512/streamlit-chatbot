models_dict = {
    8: "provider-3/gpt-4o",
    19: "provider-3/gpt-4.1",
    20: "provider-1/gpt-4.1-2025-04-14",
    12: "openai/gpt-4.1-mini",
    11: "gemini-2.0-flash",
    9: "deepseek/deepseek-chat:free",
    17: "gemini-2.5-flash-preview-05-20",
    7: "provider-3/deepseek-r1-0528",
    5: "provider-3/deepseek-v3",
    6: "provider-3/deepseek-v3-0324",
    14:"provider-3/gemini-2.5-pro-preview-06-05",
    24:"provider-3/gemini-2.5-pro-preview-05-06",
    25:"provider-3/o4-mini",
    16: "provider-3/claude-3.7-sonnet",
    18: "provider-3/claude-3.5-haiku",
    21: "provider-2/gpt-4o",
    22: "provider-2/gpt-4.1",
    23: "provider-2/claude-opus-4",
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
              "https://uxwing.com/wp-content/themes/uxwing/download/brands-and-social-media/claude-ai-icon.png",
              None]#"icons/default.png"]
user_icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGWm7kgMH1PEsycRwkyqPcPB1b2NITpD8j2g&s"


gemini_model_numbers=[11,14,17,1,24]
chatgpt_model_numbers=[12,3,8,19,20,21,22,25]
deepseek_model_numbers=[13,9,4,10,5,6,7]
claude_model_numbers=[16,18,23]


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
    elif model_number in claude_model_numbers:
        return 3, bot_icon_url[3]
    else:
        return 4, bot_icon_url[4]
