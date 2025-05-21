import streamlit as st
from streamlit import session_state as State
import requests

api_base = st.secrets["FLOW_API_BASE"]
api_key = st.secrets["FLOWISE_API_KEY"]

def query(payload):
    response = requests.post(api_base, headers={
        "Authorization": "Bearer " + api_key
    }, json=payload)
    return response.json()


async def main():

    st.title("ArcanyBot")
    st.sidebar.success("Welcome to ArcanyBot")

    st.sidebar.markdown("### Lich_su_Dang.txt")

    messages : list = State["messages"] if "messages" in State else []

    prompt = st.chat_input("What's up?")

    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        messages.append({"role": "user", "content": prompt})
        
        response = query({"question": prompt})

        usedTool = response["agentReasoning"][0]["usedTools"][0]
        if usedTool:
            st.markdown(f"** Retriever: {usedTool["tool"]} **")

        with st.chat_message("assistant"):
            st.markdown(response["text"])
            
        messages.append({"role": "assistant", "content": response["text"]})
    else:
        st.markdown("### 📝 Type a prompt to get started!")  


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

