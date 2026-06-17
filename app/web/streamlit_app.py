from uuid import uuid4

import requests
import streamlit as st

from app.models import GetMessageRequestModel, IncomingMessage

default_echo_bot_url = "http://localhost:6872"
st.set_page_config(initial_sidebar_state="expanded")

st.markdown("# Echo bot 🚀")
st.sidebar.markdown("# Echo bot 🚀")

if "dialog_id" not in st.session_state:
    st.session_state.dialog_id = str(uuid4())

# Running metrics, kept across reruns. We know the true sender of every message
# (user = human, the echoed reply = bot), so we can score the classifier live.
if "metrics" not in st.session_state:
    st.session_state["metrics"] = {"n": 0, "sum": 0.0, "correct": 0}

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Type something", "prob": None}
    ]


def classify(text: str, participant_index: int):
    """Ask /predict for the bot-probability of one message. None on failure."""
    try:
        resp = requests.post(
            st.session_state.echo_bot_url + "/predict",
            json=IncomingMessage(
                text=text,
                dialog_id=st.session_state.dialog_id,
                id=uuid4(),
                participant_index=participant_index,
            ).model_dump(),
            timeout=30,
        )
        resp.raise_for_status()
        return float(resp.json()["is_bot_probability"])
    except Exception as exc:  # keep the chat usable even if the model is down
        st.warning(f"/predict failed: {exc}")
        return None


def record_metric(role: str, prob: float | None) -> None:
    if prob is None:
        return
    m = st.session_state["metrics"]
    m["n"] += 1
    m["sum"] += prob
    # user messages should score < 0.5 (human), the echoed bot reply >= 0.5 (bot)
    expected_bot = role == "assistant"
    if (prob >= 0.5) == expected_bot:
        m["correct"] += 1


with st.sidebar:
    if st.button("Reset"):
        st.session_state.pop("messages", None)
        st.session_state["metrics"] = {"n": 0, "sum": 0.0, "correct": 0}
        st.session_state.dialog_id = str(uuid4())
        st.rerun()

    st.text_input("Bot url", key="echo_bot_url", value=default_echo_bot_url, disabled=True)
    st.text_input("Dialog id", key="dialog_id", disabled=True)

    st.markdown("### Metrics")
    m = st.session_state["metrics"]
    if m["n"]:
        st.metric("Messages classified", m["n"])
        st.metric("Avg bot probability", f"{m['sum'] / m['n']:.2f}")
        st.metric("Accuracy @0.5 (known roles)", f"{m['correct'] / m['n']:.0%}")
    else:
        st.caption("Send a message to start collecting metrics.")


def render(msg: dict) -> None:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("prob") is not None:
            marker = "🤖" if msg["prob"] >= 0.5 else "🧍"
            st.caption(f"{marker} bot probability: {msg['prob']:.2f}")


for msg in st.session_state["messages"]:
    render(msg)

if message := st.chat_input():
    # 1. classify the user's message
    user_prob = classify(message, participant_index=0)
    st.session_state["messages"].append(
        {"role": "user", "content": message, "prob": user_prob}
    )
    record_metric("user", user_prob)

    # 2. get the bot's reply (the echo bot returns the same text)
    reply = requests.post(
        st.session_state.echo_bot_url + "/get_message",
        json=GetMessageRequestModel(
            dialog_id=st.session_state.dialog_id,
            last_msg_text=message,
            last_message_id=uuid4(),
        ).model_dump(),
    ).json()["new_msg_text"]

    # 3. the reply equals the user's message, so it has the same probability -
    #    reuse it instead of calling /predict again, and count it as a bot sample.
    bot_prob = user_prob
    st.session_state["messages"].append(
        {"role": "assistant", "content": reply, "prob": bot_prob}
    )
    record_metric("assistant", bot_prob)

    st.rerun()
