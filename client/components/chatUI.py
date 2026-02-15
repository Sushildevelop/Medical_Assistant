import streamlit as st
from utils.api import ask_question


def render_chat():
    st.subheader("Chat with your assistant")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    #render existing chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    #input for new message
    user_input =st.chat_input("Type your question ....")
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        response=ask_question(user_input)
        if response.status_code == 200:
            answer=response.json().get("response")
            st.chat_message("assistant").markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            sources=response.json().get("sources", [])
            if sources:
                st.markdown("Documents used for this answer:")
                for src in sources:
                    st.markdown(f"- {src}")
        else:
            st.error("Error getting response from the server.")
        