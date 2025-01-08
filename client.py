import os
import time
import logging
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
from services.instagram_service import fetch_data
from services.db_service import (
    connect_to_database,
    create_or_get_collection,
    upload_csv_to_vector_collection,
)
from services.search_service import vector_search
from errors.runtime_error import RuntimeError
from errors.value_error import ValueError

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_data(instagram_id: str):
    collection_name = os.environ.get("ASTRA_DB_COLLECTION_NAME")
    if not collection_name:
        raise ValueError("ASTRA_DB_COLLECTION_NAME environment variable is not set.")

    try:
        database = connect_to_database()
        collection = create_or_get_collection(database, collection_name)
        csv = fetch_data(instagram_id)
        upload_csv_to_vector_collection(collection, csv, "vectorize")
    except Exception as e:
        raise RuntimeError(f"An error occurred during data upload: {str(e)}") from e

def process_query(query: str):
    if not query or not isinstance(query, str):
        raise ValueError("The query must be a non-empty string.")

    try:
        response = vector_search(query)
        message = response["outputs"][0]["outputs"][0]["results"]["message"]["data"][
            "text"
        ]

        if not message:
            raise RuntimeError(
                "The response format is invalid or does not contain the expected 'message' field."
            )

        return response, message
    except KeyError as e:
        raise RuntimeError(f"Missing expected key in the response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"An error occurred during vector search: {str(e)}") from e

def main():
    load_dotenv()
    st.set_page_config(page_title="InstaIQ", page_icon="🤖", layout="wide")

    st.markdown(
        """
        <style>
        .navbar {
            position: sticky;
            top: 0;
            z-index: 1000;
            padding: 10px;
            text-align: center;
        }
        .heading {
          margin-top: -7rem;
        }
        .main-container {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        .message {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 50%;
            margin: 1rem auto;
        }
        .stTextInput {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 50%;
            margin: 0 auto;
        }
        .stTextInput input {
            width: 100%;
        }
        .chat-container {
            height: 80vh;
            overflow-y: auto;
            width: 80%;
        }
        .stButton > button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 6px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            text-align: center;
        }

        .stButton > button:hover {
            background-color: #45a049;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            border-top: 1px solid #ddd;
            background-color: white;
            z-index: 1000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="main-container">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="navbar heading">
            <h1 style="color: #4CAF50;">🤖 Instagram Analytics Chatbot </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "instagram_processed" not in st.session_state:
        st.session_state.instagram_processed = False

    if not st.session_state.instagram_processed:
        st.markdown(
            """
            <h3 style="text-align: center; color: #333; margin-top: 2rem">Enter your Instagram profile ID below to begin! 🌟</h3>
            """,
            unsafe_allow_html=True,
        )

        instagram_id = st.text_input("Instagram ID", placeholder="e.g., user_12345", key="instagram_id", label_visibility="hidden")

        if instagram_id:
            st.markdown(f'<div class="message">Processing your data... please wait!</div>', unsafe_allow_html=True)

            try:
                process_data(instagram_id)
                st.success(f"Data for Instagram ID {instagram_id} has been successfully processed!")
                st.session_state.instagram_processed = True  
                st.rerun()
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

    if st.session_state.instagram_processed:
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me anything about your profile 🤖"}]

        chat_placeholder = st.empty()
        chat_placeholder.markdown('<div class="chat-container">', unsafe_allow_html=True)

        with chat_placeholder.container():
            for idx, msg in enumerate(st.session_state.messages):
                if msg["role"] == "assistant":
                    message(msg["content"], is_user=False, key=f"assistant-{time.time()}-{idx}")
                else:
                    message(msg["content"], is_user=True, key=f"user-{time.time()}-{idx}")
        
        st.markdown('<div style="height: 10vh;"></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([9, 1]) 

        with col1:
            query = st.chat_input("Ask a query about the data...")

        with col2:
            if st.button("Give new ID", key="give_new_id"):
                st.session_state.instagram_processed = False
                st.rerun()

        if query:
            st.session_state.messages.append({"role": "user", "content": query})

            with st.spinner("Bot is thinking..."):
                try:
                    response, extracted_message = process_query(query)
                    st.session_state.messages.append({"role": "assistant", "content": extracted_message})
                    chat_placeholder.empty()
                    with chat_placeholder.container():
                        for idx, msg in enumerate(st.session_state.messages):
                            if msg["role"] == "assistant":
                                message(msg["content"], is_user=False, key=f"assistant-{time.time()}-{idx}")
                            else:
                                message(msg["content"], is_user=True, key=f"user-{time.time()}-{idx}")
                except Exception as e:
                    error_msg = f"❌ An error occurred: {str(e)}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    chat_placeholder.empty()
                    with chat_placeholder.container():
                        for idx, msg in enumerate(st.session_state.messages):
                            if msg["role"] == "assistant":
                                message(msg["content"], is_user=False, key=f"assistant-{time.time()}-{idx}")
                            else:
                                message(msg["content"], is_user=True, key=f"user-{time.time()}-{idx}")
        elif query == "":
            st.warning("⚠️ Please provide a Query.")

    st.markdown(
        """
        <div class="footer">
           Developed by <b>Team Genz-AI</b> ❤️
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
