import streamlit as st
import requests

# Define FastAPI server URL (adjust this according to where your FastAPI server is running)
API_URL = "http://127.0.0.1:8000"  # Local server URL, update if deployed

# Apply some custom styling using Streamlit's markdown
st.markdown("""
    <style>
        .title {
            text-align: center;
            color: #9d1e50;
            font-size: 40px;
            font-weight: bold;
        }
        .message {
            text-align: center;
            color: #16a085;
            font-size: 18px;
            font-style: italic;
        }
        .button {
            background-color: #3498db;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .input-field {
            margin-top: 20px;
        }
        .query-response {
            margin-top: 20px;
            padding: 15px;
            background-color: #ecf0f1;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            color: black;  /* Change text color to black for better readability */
        }
        .sidebar .sidebar-content {
            background-color: #34495e;
            padding: 20px;
            border-radius: 8px;
        }
        .sidebar .sidebar-content .stTextInput input {
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
        }
        .sidebar .sidebar-content .stButton button {
            background-color: #3498db;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI for uploading file and querying
st.markdown('<div class="title">📄 Document Query Assistant</div>', unsafe_allow_html=True)

# Sidebar for document upload
with st.sidebar:
    uploaded_file = st.file_uploader("Upload a document (PDF or DOCX)", type=["pdf", "docx"], key="file_uploader")

    if uploaded_file:
        if st.button("Upload Document", key="upload_button", help="Click to upload the document"):
            files = {"file": uploaded_file}
            response = requests.post(f"{API_URL}/upload-file/", files=files)

            if response.status_code == 200:
                namespace_name = response.json()
                st.session_state.namespace_name = namespace_name  # Store namespace in session state
                st.success("File uploaded successfully!")
            else:
                st.error(f"Error: {response.text}")

# Query input field with custom styling
query = st.text_input("Enter your query:", key="query_input", help="Type your query related to the uploaded document.", label_visibility="collapsed", placeholder="What do you want to know?", max_chars=500)

if query and "namespace_name" in st.session_state:
    # Send query to FastAPI server for response using the stored namespace
    query_data = {"query": query, "namespace_name": st.session_state.namespace_name}
    response = requests.post(f"{API_URL}/query/", json=query_data)

    if response.status_code == 200:
        result = response.json()
        st.markdown(f'<div class="query-response"><b>Response:</b><br>{result["response"]}</div>', unsafe_allow_html=True)
    else:
        st.error(f"Error: {response.text}")

elif query:
    st.warning("Please upload a document first to get a namespace.")
