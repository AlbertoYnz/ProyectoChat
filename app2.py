import streamlit as st
import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

VECTOR_STORE_ID = "vs_6913baba995c81918b7f38c033955571"

st.set_page_config(page_title="ALBot", page_icon="😎")

st.markdown("""
<style>
body {
    background-color: #f2f6fc;
}
</style>
""", unsafe_allow_html=True)

st.title("ALBot - UP")
st.caption("Resuelve dudas de todo tipo")

st.divider()

if st.button("🗑️ Borrar conversacion"):
    st.session_state.messages = []
    st.return()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Escribe tu pregunta sobre la universidad...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner("Buscando información..."):
        response = client.responses.create(
            model="gpt-5-mini",
            input=user_input,
            tools=[{
                "type": "file_search",
                "vector_store_ids": [VECTOR_STORE_ID],
                "max_num_results": 3
            }]
        )

        messages = [m for m in response.output if m.type == "message"]
        if messages:
            reply = messages[0].content[0].text
        else:
            reply = "No se encontró información relevante."

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)


    











