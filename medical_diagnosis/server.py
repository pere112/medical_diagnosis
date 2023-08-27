import streamlit as st
import requests
import openai 
import './openai'


def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]

def main():
    st.title("OpenAI Chat Assistant")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Say something to get started!"}]

    with st.form("chat_input", clear_on_submit=True):
        a, b = st.columns([4, 1])

        user_prompt = a.text_input(
            label="Your message:",
            placeholder="Type something...",
            label_visibility="collapsed",
        )

        b.form_submit_button("Send", use_container_width=True)

    for msg in st.session_state.messages:
        st.write(msg["content"])

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # Make API call to OpenAI for chat completion
        openai_url = "http://127.0.0.1:5000/v1/chat_completions.create"
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_OPENAI_API_KEY"
        }
        payload = {
            "model": "text-ada-002",
            "messages": [{"role": "user", "content": user_prompt}],
        }
        response = requests.post(openai_url, json=payload, headers=headers)
        if response.status_code == 200:
            assistant_response = response.json()["choices"][0]["message"]["content"]
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        else:
            st.write("Error: Unable to get response from OpenAI")

    if len(st.session_state.messages) > 1:
        st.button('Clear Chat', on_click=clear_chat)

if __name__ == '__main__':
    main()
