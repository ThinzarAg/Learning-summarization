import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

st.title("勉強お助けAIエージェント")
st.write("Gemini API テスト中...")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY が .env に設定されていません")
    st.stop()

client = genai.Client(api_key=api_key)

uploaded_pdf = st.file_uploader(
    "要約するPDFファイルを選択してください",
    type=["pdf"],
)

if uploaded_pdf is not None:
    pdf_bytes = uploaded_pdf.getvalue()
    file_size_mb = len(pdf_bytes) / (1024 * 1024)

    st.write(f"ファイル: {uploaded_pdf.name}")
    st.write(f"サイズ: {file_size_mb:.2f} MB")

    if file_size_mb > 20:
        st.error("PDFファイルは20 MB以下にしてください。")
    elif st.button("PDFを要約する", type="primary"):
        prompt = """
        このPDFを日本語で要約してください。
        次の形式で、学生が理解しやすいように説明してください。

        1. 文書の概要
        2. 重要なポイント
        3. 覚えておくべき用語
        4. 短いまとめ
        """

        try:
            with st.spinner("GeminiがPDFを分析しています..."):
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[
                        types.Part.from_bytes(
                            data=pdf_bytes,
                            mime_type="application/pdf",
                        ),
                        prompt,
                    ],
                )
            st.subheader("要約結果")
            st.write(response.text)
        except Exception as error:
            st.error(f"PDFの処理中にエラーが発生しました: {error}")
