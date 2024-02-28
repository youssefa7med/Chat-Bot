import streamlit as st
import requests
import openai
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Chat Bot",initial_sidebar_state = 'collapsed',page_icon='🤖')

def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

animation = load_lottieurl('https://lottie.host/2beb66cb-6095-45fe-9f80-155888df4164/2XziOiTtfH.json')
st_lottie(animation,speed = .99,quality = 'high',height = 700,width = 700)

css_code = """
body {
  background-color: #f0f0f0; /* Light gray background */
}

/* Add more CSS styles as needed */
"""

# Display the markdown content with CSS injection
st.markdown(f"""<style>{css_code}</style>""", unsafe_allow_html=True)

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

st.sidebar.header("🤖 AI Now Is Talking !")
st.sidebar.success("✅ AI is now at your service .")
st.sidebar.write("📖 AI Model Build Only For You !")
st.sidebar.button("Clear Chat History", on_click=lambda: st.session_state["messages"].clear())
