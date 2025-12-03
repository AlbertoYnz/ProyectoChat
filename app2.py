import streamlit as st
import os
from openai import OpenAI

VECTOR_STORE_ID = "vs_6913baba995c81918b7f38c033955571"

st.set_page_config(page_title="ALBot")

st.markdown("""
<style>
body {
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("ALBot - UP")
st.caption("Resuelve dudas de todo tipo")

uploaded_file = st.file_uploader("Sube un archivo (PDF o TXT)", type=["pdf", "txt"])
file_text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        from pypdf import PdfReader
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            file_text += (page.extract_text() or "") + "\n"

    elif uploaded_file.type == "text/plain":
        file_text = uploaded_file.read().decode("utf-8")

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Pregunta lo que quieras")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    full_prompt = user_input
    if file_text:
        full_prompt = f"Basado en el siguiente archivo:\n{file_text}\n\nPregunta: {user_input}"

    with st.spinner("Pensando..."):
        response = client.responses.create(
            model="gpt-5-mini",
            input=full_prompt
        )

        messages = [m for m in response.output if m.type == "message"]
        if messages:
            reply = messages[0].content[0].text
        else:
            reply = "No se encontró información relevante."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)


st.divider()

if st.button("🗑️ Borrar conversacion"):
    st.session_state.messages = []
    
















