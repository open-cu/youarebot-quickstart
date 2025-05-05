from uuid import uuid4

import requests
import streamlit as st

from app.models import GetMessageRequestModel

default_echo_bot_url = "http://localhost:6872"
st.set_page_config(initial_sidebar_state="collapsed")

st.markdown("# Echo bot 🚀")
st.sidebar.markdown("# Echo bot 🚀")

if "dialog_id" not in st.session_state:
    st.session_state.dialog_id = str(uuid4())

with st.sidebar:
    if st.button("Reset"):
        st.session_state.pop("messages", None)
        st.session_state.dialog_id = str(uuid4())

    echo_bot_url = st.text_input(
        "Bot url", key="echo_bot_url", value=default_echo_bot_url, disabled=True
    )

    dialog_id = st.text_input("Dialog id", key="dialog_id", disabled=True)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Type something"}]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if message := st.chat_input():
    user_msg = {"role": "user", "content": message}
    st.session_state["messages"].append(user_msg)
    st.chat_message("user").write(message)

    response = requests.post(
        echo_bot_url + "/get_message",
        json=GetMessageRequestModel(
            dialog_id=dialog_id, last_msg_text=message, last_message_id=uuid4()
        ).model_dump(),
    )

    json_response = response.json()

    response = f"{json_response['new_msg_text']}"

    assistant_msg = {"role": "assistant", "content": response}
    st.session_state["messages"].append(assistant_msg)
    st.chat_message("assistant").write(response)

    st.rerun()
