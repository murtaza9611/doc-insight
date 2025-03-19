import streamlit as st
import asyncio
from src.services.workflows.file_processing import handling_documents
from src.services.vectordb.pinecone_service import PineconeService
from src.services.llm.llm_service import LLMService
from src.schemas.endpoints.schema import QueryRequest

# Apply custom styling using Streamlit's markdown
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
            # Read file contents
            contents = uploaded_file.read()
            file_name = uploaded_file.name
            file_extension = file_name.split(".")[-1].lower()

            # Await handling_documents to properly get the result
            extracted_text = asyncio.run(handling_documents(contents, file_extension, file_name))

            # Now, use the Pinecone service to create a namespace and insert documents
            pinecone_service = PineconeService()
            pinecone_service.create_namespace()

            # Insert the extracted documents into Pinecone
            namespace_name = pinecone_service.insert_data(extracted_text)

            # Store the namespace in session state
            st.session_state.namespace_name = namespace_name
            st.success("File uploaded and indexed successfully!")

# Query input field with custom styling
query = st.text_input("Enter your query:", key="query_input", help="Type your query related to the uploaded document.", label_visibility="collapsed", placeholder="What do you want to know?", max_chars=500)

if query and "namespace_name" in st.session_state:
    # Call the query processing function directly using `LLMService` and `PineconeService`
    query_data = QueryRequest(query=query, namespace_name=st.session_state.namespace_name)

    # Get the retriever using Pinecone
    pinecone_service = PineconeService()
    retriever = pinecone_service.get_retriever(query_data.namespace_name)

    # Use `LLMService` to get the chain and process the query
    llm_service = LLMService()
    chain = llm_service.get_chain(query_data.query, retriever)

    # Generate the response using the chain
    response = chain.invoke({'query': query_data.query}).content

    # Display the response
    st.markdown(f'<div class="query-response"><b>Response:</b><br>{response}</div>', unsafe_allow_html=True)

elif query:
    st.warning("Please upload a document first to get a namespace.")
