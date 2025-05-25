from openai import OpenAI
import streamlit as st
from models_data import models_dict

client_sree = OpenAI(
    base_url="https://api.a4f.co/v1",
    api_key=st.secrets["devsdocode"])
client_groq = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=st.secrets["groq_api"])
client_github = OpenAI(
    base_url="https://models.github.ai/inference",
    api_key=st.secrets["github"])
client_openrouter = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=st.secrets["open_router"])
client_google = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta",
    api_key=st.secrets['google'])

## Getting providers modelnumbers
google_model_numbers=[1,11,17]
github_model_numbers=[3,12]
openrouter_model_numbers=[2,9, 10,13,15]
sree_model_numbers=[5, 6, 7, 8, 14, 16, 18]



def get_client(model_number):
    '''
    Takes the model number as input and returns the client and stream.
    '''
    if model_number in sree_model_numbers:
        return client_sree,True
    elif model_number in openrouter_model_numbers:
        return client_openrouter,True
    elif model_number in google_model_numbers:
        return client_google,True
    elif model_number in github_model_numbers:
        return client_github,True
    else:
        return client_groq,False


