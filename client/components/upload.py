import streamlit as st

from utils.api import upload_pdfs_api

def render_uploader():
    st.sidebar.header("Upload Medical documents (.PDFs)")
    uploaded_files = st.sidebar.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    if st.sidebar.button("Upload DB") and uploaded_files:
        with st.spinner("Uploading and processing PDFs..."):
            response = upload_pdfs_api(uploaded_files)
            if response.status_code == 200:
                st.sidebar.success("PDFs uploaded and processed successfully!")
            else:
                st.sidebar.error("Error uploading PDFs. Please try again.")