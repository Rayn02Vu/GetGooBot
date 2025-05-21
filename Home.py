import streamlit as st
from streamlit import session_state as State
from langchain_openai.chat_models import ChatOpenAI

api_key = st.secrets["CONO_API_KEY"]
api_base = st.secrets["CONO_API_BASE"]

llm = ChatOpenAI(
    model_name = "cono-3-exp",
    api_key=api_key, 
    base_url=api_base
)

async def main():
    
    st.title("ArcanyBot")
    st.sidebar.success("Welcome to ArcanyBot")
    
    if "messages" not in State:
        State.messages = []
    
    message_first = {
        "role": "system",
        "content": """Bạn hãy đóng vai trợ lý AI thân thiện trả lời chính xác, hãy giúp đỡ nhiều nhất có thể nhé! 
        Lưu ý: hãy trả lời một ngôn ngữ thống nhất, không trả lời lẫn lộn các ngôn ngữ. Ưu tiên trả lời rõ ràng bằng Tiếng Việt.
        """
    }
    State.messages.append(message_first)
    
    prompt = st.chat_input("Prompt here...")
    
    if len(State.messages) > 5:
        State.messages = [State.messages[0]] + State.messages[-5:]
        
    for msg in State.messages:
        if msg["role"] == "system":
            continue
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt:
        with st.chat_message("user"):
            st.markdown(prompt)
        State.messages.append({"role": "user", "content": prompt})
        
        response = llm.invoke(State.messages)
        
        with st.chat_message("assistant"):
            st.markdown(response.content)
            
        State.messages.append({"role": "assistant", "content": response.content})
    else:
        st.markdown("### 📝 Type a prompt to get started!")  


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())