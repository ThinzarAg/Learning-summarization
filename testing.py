import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.title("勉強お助けAIエージェント")
st.write("Gemini API テスト中...")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY が .env に設定されていません")
    st.stop()

client = genai.Client(api_key=api_key)

if st.button("テスト送信"):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="こんにちはと一言返してください",
    )
    st.write(response.text)