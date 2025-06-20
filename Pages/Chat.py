import streamlit as st
import numpy as np
import pandas as pd
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage
#from mygraph import createGraph
from Pages.mygraph import createGraph
import uuid
import os
import tempfile
from Pages.utils import get_token_count, log_chat, display_chat_history


# Streamlit UI
#setting page title and logo
st.set_page_config(page_title = "Legal Document Analyser", page_icon="ey-logo-black.png")
#adding padding using css
st.logo(image="ey-logo-black.png", size="large")
st.markdown('<style>div.block-container{padding-top:4rem;padding-left:1rem;padding-right:5rem}</style>',unsafe_allow_html=True)
col1,col2 = st.columns([1.2,10])
with col1: st.image("ey-logo-black.png", width=150)
with col2: st.title("Legal Document Analyser")
# Add a horizontal line after the header
st.markdown('<hr style="border:1px solid #aaa; margin-bottom: 1rem"/>', unsafe_allow_html=True)
st.write("")

tab1,tab2 = st.tabs(["Summarize", "Compare"])

#defining tab1 contents
with tab1:
    with st.container(border=True, key="con1") as con1:
        graph = createGraph()
        user_query = st.text_input("Ask a question to summarize or compare documents:",
                                   placeholder="Input prompt here", )
        col3, col4, col5 = st.columns([1, 1, 1.7])
        with col5:
            uploaded_files = st.file_uploader("Upload documents to compare or summarize:", ["pdf", "docx"], True,
                                              key="Attach")
        with col3:
            submit = st.button("Submit", use_container_width=True)

    if submit:
        path = r'C:\Users\GM612CD\PycharmProjects\UC_Legal Document Analyser\temp_docs'
        os.makedirs(path, exist_ok=True)

        file_paths = []
        for uploaded_file in uploaded_files:
            file_path = os.path.join(path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            file_paths.append(file_path)

        if user_query and len(file_paths) != 0:
            query = user_query + f" file_path:{file_paths}"
            st.write('User:', query)
            response = graph.invoke({'messages': HumanMessage(content=query)})

            if response:
                ai_msg = response['messages'][-1].content
                st.write('AIMessage:', ai_msg)

                # Token tracking
                from Pages.utils import get_token_count, log_chat, display_chat_history

                prompt_tokens = get_token_count(query)
                doc_tokens = sum(get_token_count(open(p, 'r', errors="ignore").read()) for p in file_paths)
                response_tokens = get_token_count(ai_msg)
                total = prompt_tokens + doc_tokens + response_tokens
                log_chat("summarize", query, ai_msg, {
                    "prompt": prompt_tokens,
                    "doc": doc_tokens,
                    "response": response_tokens,
                    "total": total
                })
        elif user_query:
            query = user_query
            st.write('User:', query)
            response = graph.invoke({'messages': HumanMessage(content=query)})

            if response:
                ai_msg = response['messages'][-1].content
                st.write('AIMessage:', ai_msg)

                prompt_tokens = get_token_count(query)
                response_tokens = get_token_count(ai_msg)
                log_chat("summarize", query, ai_msg, {
                    "prompt": prompt_tokens,
                    "doc": 0,
                    "response": response_tokens,
                    "total": prompt_tokens + response_tokens
                })
        else:
            st.warning("Please enter a query and upload files.")

    # Always show chat history at the bottom of tab1
    display_chat_history("summarize")

with tab2:
    from Pages.utils import log_chat, get_token_count, display_chat_history  # Assuming these utils exist

    with st.container(border=True, key="con2") as con2:
        graph = createGraph()
        compare_query = st.text_input("Compare the two uploaded documents:", placeholder="Enter a comparison prompt",
                                      key="compare_prompt")
        col6, col7, col8 = st.columns([1, 1, 1.7])
        with col8:
            compare_files = st.file_uploader("Upload exactly 2 documents to compare:", ["pdf", "docx"],
                                             accept_multiple_files=True, key="compare_upload")
        with col6:
            submit_compare = st.button("Compare", use_container_width=True, key="compare_button")

    if submit_compare:
        compare_path = r'C:\Users\GM612CD\PycharmProjects\UC_Legal Document Analyser\temp_docs'
        os.makedirs(compare_path, exist_ok=True)

        file_paths = []
        for uploaded_file in compare_files:
            file_path = os.path.join(compare_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            file_paths.append(file_path)

        if compare_query and len(file_paths) == 2:
            query = compare_query + f" file_path:{file_paths}"
            st.write('User:', query)

            response = graph.invoke({'messages': HumanMessage(content=query)})

            if response:
                ai_msg = response['messages'][-1].content
                st.write('AIMessage:', ai_msg)

                # Token tracking
                prompt_tokens = get_token_count(query)
                doc_tokens = sum(get_token_count(open(p, 'r', errors="ignore").read()) for p in file_paths)
                response_tokens = get_token_count(ai_msg)
                total = prompt_tokens + doc_tokens + response_tokens

                log_chat("compare", query, ai_msg, {
                    "prompt": prompt_tokens,
                    "doc": doc_tokens,
                    "response": response_tokens,
                    "total": total
                })
        elif len(file_paths) != 2:
            st.warning("Please upload exactly two documents for comparison.")
        else:
            st.warning("Please enter a prompt and upload files.")

    # Always display chat history at the end of compare tab
    display_chat_history("compare")

#creating data for chat history:
chats = {

    "Chats": ["Prompt1", "Prompt2", "Prompt3"]
}
df = pd.DataFrame(data=chats)

#sidebar
#Page Links in sidebar:
st.sidebar.title("Legal Document Analyser")
st.sidebar.page_link(page="Home.py", label="Home", use_container_width= True, icon="🏠")
st.sidebar.page_link(page="Pages/Chat.py", label="Chat", use_container_width= True, icon="💬")
st.sidebar.page_link(page="Pages/About.py", label="About", use_container_width= True, icon="❓")

#container for chat history
sbcnt = st.sidebar.container(height=300,border=True)
with sbcnt:
    sbcnt.subheader("Chat History:")
    sbcnt.dataframe(df)

#Footer Links (paste footer controls here)


st.caption("Disclaimer: This response was generated by an AI and is intended for informational purposes only. While efforts have been made to ensure accuracy, the information provided may not be complete or up-to-date. Always verify critical information independently and consult with a qualified professional if necessary. The AI does not have personal experiences or emotions and its responses are based on patterns in data.")

#CSS code for the page
csscode = """
    <style>
    .stApp {
        background-color: #2e2e38;
    }
    .stTextInput>div>div>input {
        background-color: white;
        color: black;
    }
    .stTextInput {
             padding-left:2rem
    }
    .stButton>button {
        background-color: #ffe600;
        color: black;
    }
    .stButton {
            padding: 2rem;
    }
    .st-emotion-cache-1104ytp {

            color:white;
    }
    .st-emotion-cache-wq5ihp {
            color:white
    }
    .stcon1{
            padding: 6 rem;
            }

    .stColumn st-emotion-cache-t74pzu eu6p4el2{
            padding: 4rem;
            }

    .st-emotion-cache-1uixxvy{
            color: white;
            }
    .stMarkdown {
        color: white;
    }
</style>
"""
# Custom CSS for background color
st.markdown(csscode, unsafe_allow_html=True)
