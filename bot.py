import streamlit as st
import openai

st.header("Chat bot")

openai.api_key = st.secrets["OPEN_API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask your question:")
if prompt :
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages = [{
                "role": m["role"],
                "content": m["content"],
            } for m in st.session_state["messages"]],
            stream = True,
        ):
            full_response += response["choices"][0].delta.get("content", "")
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)

    st.session_state["messages"].append({"role": "assistant", "content": full_response})

st.sidebar.button("Clear history", on_click=lambda: st.session_state["messages"].clear())
