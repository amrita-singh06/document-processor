import streamlit as st
import requests

UPLOAD_API = "http://localhost:9000/upload/"
INGEST_API = "http://localhost:9000/ingest-url/"
QUERY_API = "http://localhost:9000/query/"  # you need to implement backend query API

st.set_page_config(page_title="Document Analyzer", layout="wide")

# ---------------------
# Initialize session state
if "documents" not in st.session_state:
    st.session_state.documents = []  # list of dicts: {"id": ..., "file_name": ...}

# ---------------------
# Sidebar Navigation
page = st.sidebar.selectbox("Navigation", ["Home", "Query Documents"])

# ---------------------
# Home Page: Upload or URL
if page == "Home":
    st.title("📄 Welcome to Document Analyzer")

    option = st.selectbox("Choose an option:", ["Select Option","Upload Document", "Paste URL"])

    # Upload document
    if option == "Upload Document":
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

        if uploaded_file:
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            with st.spinner("📤 Uploading and processing..."):
                response = requests.post(UPLOAD_API, files=files)

            if response.status_code == 200:
                data = response.json()
                st.success(f"✅ Uploaded: {data.get('file_name', 'Unknown')}")
                st.write(f"📌 Document ID: {data.get('document_id', 'N/A')}")
                # Save in session
                st.session_state.documents.append({"id": data.get('document_id'), "file_name": data.get('file_name')})
            else:
                st.error("❌ Upload failed.")

    # Paste URL
    elif option == "Paste URL":
        pdf_url = st.text_input("Enter PDF URL")

        if st.button("Fetch & Process"):
            if pdf_url.strip():
                with st.spinner("🌐 Downloading and processing..."):
                    response = requests.post(INGEST_API, params={"pdf_url": pdf_url})

                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Processed from URL: {data.get('file_name', 'Unknown')}")
                    st.write(f"📌 Document ID: {data.get('document_id', 'N/A')}")
                    st.write(f"📑 Chunks stored: {data.get('chunks_stored', 'N/A')}")
                    # Save in session
                    st.session_state.documents.append({"id": data.get('document_id'), "file_name": data.get('file_name')})
                else:
                    st.error("❌ URL processing failed.")
            else:
                st.warning("⚠️ Please enter a valid PDF URL.")

# ---------------------
# Query Page: Ask questions to documents
elif page == "Query Documents":
    st.title("📝 Query Your Documents")

    if not st.session_state.documents:
        st.info("No documents available. Please upload or ingest a document first.")
    else:
        # Select document
        doc = st.selectbox("Select a document to query:", st.session_state.documents, format_func=lambda x: x["file_name"])

        user_question = st.text_input("Ask a question about the document:")

        if st.button("Submit Question") and user_question.strip():
            with st.spinner("🤖 Processing your query..."):
                # Send question + doc_id to backend query API
                payload = {"document_id": doc["id"], "question": user_question}
                try:
                    response = requests.post(QUERY_API, json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "No answer returned")
                        st.success("✅ Answer:")
                        st.write(answer)
                    else:
                        st.error("❌ Query failed.")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
