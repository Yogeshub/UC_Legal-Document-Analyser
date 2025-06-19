import streamlit as st

st.set_page_config(page_title="Legal Document Analyser", page_icon="ey-logo-black.png")

st.logo(image="ey-logo-black.png", size="large")
st.title("Welcome to Legal Document Analyser")

st.markdown("""
This application allows you to:
- Summarize uploaded legal documents (PDF or DOCX).
- Compare two legal documents for differences.
- Interact via chat with your documents using AI.

Use the sidebar to navigate between pages.
""")

# st.image("legal-doc.jpg", caption="Secure & Smart Legal AI", use_container_width=True)

col3,col4,col5 = st.columns([2.8,1,3])
with col4:
    st.page_link(page="Pages/chat1.py", label="Begin", use_container_width=True)

st.sidebar.page_link("Home1.py", label="Home", icon="🏠")
st.sidebar.page_link("Pages/chat1.py", label="Chat", icon="💬")
st.sidebar.page_link("Pages/About.py", label="About", icon="❓")
