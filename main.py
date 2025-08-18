from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="D:/Course/DL/Chatbot-Langchain-Streamlit/.env")
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from pprint import pprint 

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    # max_output_tokens=1024,
    timeout=None,
    max_retries=3,
)


SYSTEM_PROMPT = """ 
You are a helpful assistant. You will answer questions based on the provided documents. If you don't know the answer, say "I don't know". 
PDF Content:\n {docs}
"""

st.title("Custom Chatbot")

os.makedirs("docs", exist_ok=True)
file_uploader = st.file_uploader("Upload a file", type=["pdf"])
if file_uploader is not None:
    file_path = f"docs/{file_uploader.name}"
    with open(file_path, "wb") as f:
        f.write(file_uploader.getbuffer())
    st.session_state.file_path = file_path
    st.success(f"File saved to {file_path}")
    
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    docs = "".join([doc.page_content for doc in documents])
    st.session_state.messages.append(
        {"role": "system", "content": SYSTEM_PROMPT.format(docs=docs) if 'docs' in locals() else "No documents uploaded."}
    )

    

    




if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(docs=docs) if 'docs' in locals() else "No documents uploaded."}
    ]
    
else:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        elif message["role"] == "assistant":
            st.chat_message("assistant").write(message["content"])
    
    
user_message = st.chat_input("Enter your message:")

if user_message:
    st.chat_message("user").write(user_message)
    
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    with st.chat_message("assistant"):
        stream = llm.stream(st.session_state.messages)
        response = st.write_stream(stream)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
    

        
        
    
    