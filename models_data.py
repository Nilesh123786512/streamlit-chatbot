models_dict = {
    8: "gemini-2.5-flash-lite-preview-06-17",
    19: "gemini-2.5-flash",
    20: "provider-6/o3-high",
    12: "openai/gpt-4.1-mini",
    11: "gemini-2.5-pro",
    9: "deepseek/deepseek-chat:free",
    17: "gemini-2.5-flash-preview-05-20",
    7: "provider-6/o3-low",
    5: "provider-3/deepseek-v3",
    6:  "provider-3/deepseek-v3-0324",
    14: "provider-6/kimi-k2",
    24: "provider-6/deepseek-r1-uncensored",
    25: "provider-1/deepseek-r1-0528",
    16: "provider-1/claude-3.7-sonnet-thinking",
    18: "provider-1/claude-sonnet-4",
    21: "provider-6/o3-medium",
    22: "provider-3/gpt-4.1-mini",
    23: "provider-6/gpt-4.1",
    1:  "gemini-2.0-flash-thinking-exp-1219",
    3:  "openai/gpt-4.1",
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
              "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS9kk110z2F3XC0xHw7MFCXwHd4dk9qFlGTnS2TRLtTCg&s",
              None]#"icons/default.png"]
user_icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGWm7kgMH1PEsycRwkyqPcPB1b2NITpD8j2g&s"


gemini_model_numbers=[11,17,1,8,19]
chatgpt_model_numbers=[12,3,20,21,22,23,7]
deepseek_model_numbers=[13,9,25,4,10,5,6,24]
claude_model_numbers=[18,16]


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
