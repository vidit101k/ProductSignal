
import streamlit as st
from google import genai
from google.genai import types


MODEL_NAME = "gemini-3.5-flash-lite"


def generate_ai_response(prompt):
    api_key = st.secrets["GEMINI_API_KEY"]

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=30000,
            retry_options=types.HttpRetryOptions(
                attempts=1,
                http_status_codes=[]
            )
        )
    )

    response = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        timeout=30
    )

    return response.output_text
