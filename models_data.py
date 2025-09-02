models_dict = {
    8: "gemini-2.5-flash-lite-preview-06-17",
    19: "gemini-2.5-flash",
    0: "moonshotai/kimi-k2-instruct",
    1:  "provider-3/gpt-5-nano",
    21: "provider-3/deepseek-v3.1",
    14: "provider-1/deepseek-v3.1",
    10: "openai/gpt-oss-120b",
    16: "provider-1/glm-4.5",
    23: "provider-1/glm-4.5-fp8",
    15: "provider-6/gpt-4o",
    20: "meta-llama/llama-4-scout-17b-16e-instruct",
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
    18: "provider-6/gemini-2.5-flash-thinking",
    22: "z-ai/glm-4.5-air:free",
    3:  "openai/gpt-4.1",
    13: "deepseek/deepseek-chat-v3-0324:free",
    4:  "deepseek-r1-distill-llama-70b",

}
bot_icon_url=["icons/gemini.png",
              "icons/chatgpt.png",
              "icons/deepseek.png",
              "icons/qwen.png",
              "icons/claude.png",
              "icons/meta.png",
              "https://aimode.co/wp-content/uploads/2025/03/Kimi-AI-Logo.webp",
              "https://raw.githubusercontent.com/zai-org/GLM-4.5/refs/heads/main/resources/logo.svg",
              "https://pbs.twimg.com/profile_images/1893219113717342208/Vgg2hEPa_400x400.jpg",
               None]#"icons/default.png"]
user_icon_url="icons/user.png"

long_context_models=[0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27]

bot_icon_dict={
    "gemini":[11,8,19,18],
    "chatgpt":[3,7,10,1,27,15],
    "deepseek":[13,21,25,4,5,6,24],
    "qwen":[2,9,17],
    "claude":[],
    "meta":[20],
    "kimi":[14,0],
    "zai":[22,16,23],
    "grok":[12,26]
}
## Getting providers modelnumbers
google_model_numbers=[8,11,19]
github_model_numbers=[3,12,26,27]
openrouter_model_numbers=[2, 13, 22]
sree_model_numbers=[1, 5, 6, 7, 14, 15, 16, 18,  21, 23, 24, 25, 9, 17]

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
    
