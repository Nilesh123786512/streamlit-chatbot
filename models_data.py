models_dict = {
    8: "gemini-2.5-flash-lite-preview-06-17",
    19: "gemini-2.5-flash",
    1:  "provider-3/gpt-5-nano",
    14: "provider-3/kimi-k2",
    0: "moonshotai/kimi-k2-instruct",
    4: "deepseek-r1-distill-llama-70b",
    10: "openai/gpt-oss-120b",
    20: "provider-6/horizon-beta",
    21: "provider-6/o3-medium",
    12: "xai/grok-3",
    26: "xai/grok-3-mini",
    27: "openai/gpt-4.1-mini",
    11: "gemini-2.5-pro",
    9: "provider-3/qwen-3-235b-a22b-2507",
    17: "provider-6/qwen3-coder-480b-a35b",
    7: "provider-6/o3-low",
    5: "provider-3/deepseek-v3",
    6:  "provider-3/deepseek-v3-0324",
    24: "provider-6/deepseek-r1-uncensored",
    25: "provider-1/deepseek-r1-0528",
    2: "qwen/qwen3-coder:free",
    16: "provider-6/gpt-oss-120b",
    18: "provider-6/gemini-2.5-flash-thinking",
    22: "z-ai/glm-4.5-air:free",
    23: "provider-6/gpt-4.1",
    3:  "openai/gpt-4.1",
    13: "deepseek/deepseek-chat-v3-0324:free",
    15: "meta-llama/llama-4-scout-17b-16e-instruct",

}
bot_icon_url=["icons/gemini.png",
              "icons/chatgpt.png",
              "icons/deepseek.png",
              "icons/qwen.png",
              "icons/claude.png",
              "icons/meta.png",
              "https://aimode.co/wp-content/uploads/2025/03/Kimi-AI-Logo.webp",
              "https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/logo.svg",
              "data:image/jpeg;base64,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",
              None]#"icons/default.png"]
user_icon_url="icons/user.png"

long_context_models=[0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27]

bot_icon_dict={
    "gemini":[11,8,19,18],
    "chatgpt":[3,20,21,23,7,16,10,1,27],
    "deepseek":[13,25,4,5,6,24],
    "qwen":[2,9,17],
    "claude":[],
    "meta":[15],
    "kimi":[14,0],
    "zai":[22],
    "grok":[12,26]
}
## Getting providers modelnumbers
google_model_numbers=[8,11,19]
github_model_numbers=[3,12,26,27]
openrouter_model_numbers=[2, 13, 22]
sree_model_numbers=[1, 5, 6, 7, 14, 16, 18, 20, 21, 23, 24, 25, 9, 17]

def get_icon_no_and_value(model_number):
    """
    Get the icon number and value for a given model number.

    Args:
        model_number (int): The model number.

    Returns:
        tuple: A tuple containing the icon number and value.
    """
    for i,model_type in enumerate(bot_icon_dict.keys()):
        if model_number in bot_icon_dict[model_type]:
            return i,bot_icon_url[i]
    return i,bot_icon_url[i]
    
