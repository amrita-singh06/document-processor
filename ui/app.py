import streamlit as st
import requests

API_URL = "http://localhost:8000/upload/"

st.title("📄 Document Uploader")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
    with st.spinner("Uploading and processing..."):
        response = requests.post(API_URL, files=files)

    if response.status_code == 200:
        data = response.json()
        st.success(f"Uploaded: {data['file_name']}")
        st.write(f"Document ID: {data['document_id']}")
    else:
        st.error("Upload failed.")
