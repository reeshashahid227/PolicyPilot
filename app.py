import os

import requests
import streamlit as st


# ============================================================
# Configuration
# ============================================================

API_URL = os.getenv(
    "POLICYPILOT_API_URL",
    "http://127.0.0.1:8000",
)


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="PolicyPilot",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Custom CSS
# ============================================================

st.markdown(
    """
    <style>

    /* =========================
       Main App
       ========================= */

    .stApp {
        background-color: #F8FAFC;
    }

    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 7rem;
    }


    /* =========================
       Header
       ========================= */

    .brand-container {
        text-align: center;
        padding: 10px 0 30px 0;
    }

    .brand-icon {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .main-title {
        color: #1E293B;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
    }

    .main-title span {
        color: #4F46E5;
    }

    .subtitle {
        color: #64748B;
        font-size: 17px;
        margin-top: 8px;
    }


    /* =========================
       Sidebar
       ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #EEF2FF 0%,
            #F8FAFC 100%
        );
        border-right: 1px solid #E2E8F0;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1E293B;
    }

    section[data-testid="stSidebar"] p {
        color: #475569;
    }


    /* =========================
       Sidebar Buttons
       ========================= */

    section[data-testid="stSidebar"] .stButton > button {
        background-color: #FFFFFF;
        color: #334155;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        padding: 0.65rem 0.8rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        border-color: #4F46E5;
        color: #4F46E5;
        background-color: #EEF2FF;
        transform: translateY(-1px);
    }


    /* =========================
       Chat Messages
       ========================= */

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 8px 10px;
        margin-bottom: 12px;
    }

    /* User message */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background-color: #EEF2FF;
        border: 1px solid #E0E7FF;
    }

    /* Assistant message */
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }


    /* =========================
       Chat Text
       ========================= */

    [data-testid="stChatMessage"] p {
        color: #1E293B !important;
        font-size: 16px;
        line-height: 1.65;
    }


    /* =========================
       Sources Heading
       ========================= */

    .sources-title {
        color: #4F46E5;
        font-size: 15px;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 8px;
    }


    /* =========================
       Sources Box
       ========================= */

    .source-box {
        background: #EEF2FF;
        border: 1px solid #C7D2FE;
        border-left: 4px solid #4F46E5;
        border-radius: 10px;
        padding: 10px 14px;
        margin: 7px 0;
        color: #1E293B !important;
    }

    .source-box span {
        color: #1E293B !important;
        font-size: 14px;
    }

    .source-box strong {
        color: #312E81 !important;
    }


    /* =========================
       Chat Input
       ========================= */

    [data-testid="stChatInput"] {
        border-radius: 16px;
    }

    [data-testid="stChatInput"] textarea {
        color: #1E293B !important;
        background-color: #FFFFFF !important;
    }


    /* =========================
       Footer
       ========================= */

    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 13px;
        margin-top: 35px;
        padding: 20px;
    }


    /* =========================
       Divider
       ========================= */

    hr {
        border-color: #E2E8F0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Header
# ============================================================

st.markdown(
    """
    <div class="brand-container">
        <div class="brand-icon">🏛️</div>
        <div class="main-title">
            Policy<span>Pilot</span>
        </div>
        <div class="subtitle">
            AI-powered policy assistant for intelligent,
            document-grounded answers
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.markdown("## 🏛️ PolicyPilot")

    st.write(
        "Ask questions about company policies "
        "and get answers directly from policy documents."
    )

    st.divider()

    st.markdown("### 💡 Try asking")

    example_questions = [
        "What is the remote work policy?",
        "How many annual leave days are available?",
        "What is the sick leave policy?",
        "What benefits are available to employees?",
    ]

    for question in example_questions:

        if st.button(
            question,
            use_container_width=True,
        ):
            st.session_state.pending_question = question

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []

        if "pending_question" in st.session_state:
            del st.session_state.pending_question

        st.rerun()

    st.markdown("---")

    st.caption(
        "🔎 Answers are generated from retrieved "
        "policy documents."
    )


# ============================================================
# Display Previous Messages
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            st.markdown(
                '<div class="sources-title">📚 Sources</div>',
                unsafe_allow_html=True,
            )

            for source in message["sources"]:

                if isinstance(source, dict):

                    source_name = (
                        source.get("source")
                        or source.get("document")
                        or source.get("file")
                        or source.get("title")
                        or "Policy Document"
                    )

                    page = source.get("page")

                    if page is not None:
                        source_text = (
                            f"📄 <strong>{source_name}</strong>"
                            f" — Page {page}"
                        )
                    else:
                        source_text = (
                            f"📄 <strong>{source_name}</strong>"
                        )

                else:
                    source_text = f"📄 {source}"

                st.markdown(
                    f"""
                    <div class="source-box">
                        <span>{source_text}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================
# User Input
# ============================================================

pending_question = st.session_state.pop(
    "pending_question",
    None,
)

user_question = st.chat_input(
    "Ask a question about company policies..."
)

question = user_question or pending_question


# ============================================================
# Send Question to FastAPI
# ============================================================

if question:

    # --------------------------------------------
    # Display User Message
    # --------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    # --------------------------------------------
    # Call FastAPI
    # --------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching policy documents..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/ask",
                    json={
                        "question": question
                    },
                    timeout=120,
                )

                response.raise_for_status()

                data = response.json()


                # --------------------------------
                # Answer
                # --------------------------------

                answer = data.get(
                    "answer",
                    "No answer was returned by the API.",
                )


                # --------------------------------
                # Sources
                # --------------------------------

                sources = data.get(
                    "sources",
                    [],
                )


                # --------------------------------
                # Display Answer
                # --------------------------------

                st.markdown(answer)


                # --------------------------------
                # Display Sources
                # --------------------------------

                if sources:

                    st.markdown(
                        '<div class="sources-title">'
                        '📚 Sources'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    for source in sources:

                        if isinstance(source, dict):

                            source_name = (
                                source.get("source")
                                or source.get("document")
                                or source.get("file")
                                or source.get("title")
                                or "Policy Document"
                            )

                            page = source.get("page")

                            if page is not None:
                                source_text = (
                                    f"📄 <strong>{source_name}</strong>"
                                    f" — Page {page}"
                                )
                            else:
                                source_text = (
                                    f"📄 <strong>{source_name}</strong>"
                                )

                        else:
                            source_text = f"📄 {source}"

                        st.markdown(
                            f"""
                            <div class="source-box">
                                <span>{source_text}</span>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


                # --------------------------------
                # Save Assistant Response
                # --------------------------------

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )


            # ------------------------------------
            # Error Handling
            # ------------------------------------

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to the FastAPI server."
                )

                st.info(
                    f"Make sure FastAPI is running on {API_URL}"
                )


            except requests.exceptions.Timeout:

                st.error(
                    "⏳ The request took too long. "
                    "Please try again."
                )


            except requests.exceptions.HTTPError as error:

                st.error(
                    f"❌ FastAPI returned an error: {error}"
                )


            except requests.exceptions.RequestException as error:

                st.error(
                    f"❌ Request failed: {error}"
                )


            except Exception as error:

                st.error(
                    f"❌ Unexpected error: {error}"
                )


# ============================================================
# Footer
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>PolicyPilot</strong> • AI Policy Assistant
        <br>
        Grounded answers powered by Retrieval-Augmented Generation
    </div>
    """,
    unsafe_allow_html=True,
)