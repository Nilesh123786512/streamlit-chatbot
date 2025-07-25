models_dict = {
    8: "gemini-2.5-flash-lite-preview-06-17",
    19: "gemini-2.5-flash",
    20: "provider-6/o3-high",
    12: "openai/gpt-4.1-mini",
    11: "gemini-2.5-pro",
    9: "provider-3/qwen-3-235b-a22b-2507",
    17: "provider-6/qwen3-coder-480b-a35b",
    7: "provider-6/o3-low",
    5: "provider-3/deepseek-v3",
    6:  "provider-3/deepseek-v3-0324",
    14: "provider-6/kimi-k2",
    24: "provider-6/deepseek-r1-uncensored",
    25: "provider-1/deepseek-r1-0528",
    2: "qwen/qwen3-coder:free",
    16: "provider-1/gemini-2.5-pro",
    18: "provider-6/gemini-2.5-flash-thinking",
    21: "provider-6/o3-medium",
    22: "provider-6/gpt-4o-mini-search-preview",
    23: "provider-6/gpt-4.1",
    1:  "gemini-2.0-flash-thinking-exp-1219",
    3:  "openai/gpt-4.1",
    13: "deepseek/deepseek-chat-v3-0324:free",
    15: "meta-llama/llama-4-maverick:free",
    0: "qwen-qwq-32b",
    4: "deepseek-r1-distill-llama-70b",
    10: "deepseek/deepseek-r1:free",

}
bot_icon_url=["icons/gemini.png",
              "icons/chatgpt.png",
              "icons/deepseek.png",
              "https://registry.npmmirror.com/@lobehub/icons-static-png/1.56.0/files/dark/qwen-color.png",
              None]#"icons/default.png"]
user_icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRGWm7kgMH1PEsycRwkyqPcPB1b2NITpD8j2g&s"


gemini_model_numbers=[11,1,8,19,16,18]
chatgpt_model_numbers=[12,3,20,21,22,23,7]
deepseek_model_numbers=[13,25,4,10,5,6,24]
qwen_model_numbers=[2,9,17]

## Getting providers modelnumbers
google_model_numbers=[1,8,11,19]
github_model_numbers=[3,12]
openrouter_model_numbers=[2, 10, 13, 15]
sree_model_numbers=[5, 6, 7, 14, 16, 18, 20, 21, 22, 23, 24, 25, 9, 17]

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
    elif model_number in qwen_model_numbers:
        return 3, bot_icon_url[3]
    else:
        return 4, bot_icon_url[4]
