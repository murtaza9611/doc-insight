# app/core/config.py

# from pydantic_settings import BaseSettings
# from dotenv import load_dotenv
# import os

# load_dotenv()





# class Settings(BaseSettings):
#     """
#     This Settings class is designed to load and manage environment variables for an
#     application using Pydantic's BaseSettings and python-dotenv

#     write all your env variables here so you can access them easily.

#     """

#     OPENAI_API_KEY : str = os.environ.get("OPENAI_API_KEY")
#     PINECONE_API_KEY : str = os.environ.get("PINECONE_API_KEY")


#     class Config:
#         env_file = ".env"

# settings = Settings()





import streamlit as st
from pydantic import BaseModel

class Settings(BaseModel):
    """
    This Settings class is designed to load and manage configuration variables
    from Streamlit Cloud's st.secrets.
    """

    # Define your environment variables
    OPENAI_API_KEY: str = st.secrets["OPENAI_API_KEY"]
    PINECONE_API_KEY: str = st.secrets["PINECONE_API_KEY"]

# Create an instance of the settings
settings = Settings()