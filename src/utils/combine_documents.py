def combine_documents(docs):
    """Combine retrieved documents into a single string."""
    return "\n".join([doc.page_content for doc in docs])
