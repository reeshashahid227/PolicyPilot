import streamlit as st

from src.core.policy_engine import PolicyEngine


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PolicyPilot",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

/* =========================================================
   GLOBAL
========================================================= */

.stApp {
background: #F8FAFC !important;
color: #1E293B !important;
}

.stApp * {
box-sizing: border-box;
}


/* =========================================================
   ALL STREAMLIT TEXT
========================================================= */

.stApp p,
.stApp span,
.stApp label,
.stApp div,
.stApp li,
.stApp td,
.stApp th {
color: #1E293B;
}


/* Markdown text */

[data-testid="stMarkdownContainer"] p {
color: #1E293B !important;
}

[data-testid="stMarkdownContainer"] li {
color: #1E293B !important;
}

[data-testid="stMarkdownContainer"] strong {
color: #1E293B !important;
}

[data-testid="stMarkdownContainer"] em {
color: #475569 !important;
}


/* =========================================================
   HEADER
========================================================= */

.brand-container {
text-align: center;
padding: 20px 0 35px 0;
}

.brand-icon {
font-size: 52px !important;
color: #1E293B !important;
}

.main-title {
color: #1E293B !important;
font-size: 44px !important;
font-weight: 800 !important;
line-height: 1.2;
}

.brand-name {
color: #4F46E5 !important;
}

.subtitle {
color: #64748B !important;
font-size: 17px !important;
margin-top: 10px;
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {
background: #EEF2FF !important;
}

section[data-testid="stSidebar"] * {
color: #1E293B !important;
}

section[data-testid="stSidebar"] p {
color: #475569 !important;
}


/* Sidebar buttons */

section[data-testid="stSidebar"] .stButton button {
background: #FFFFFF !important;
color: #334155 !important;
border: 1px solid #CBD5E1 !important;
border-radius: 12px !important;
font-weight: 600 !important;
}

section[data-testid="stSidebar"] .stButton button:hover {
background: #E0E7FF !important;
color: #4338CA !important;
border-color: #6366F1 !important;
}

section[data-testid="stSidebar"] .stButton button p {
color: #1E293B !important;
}

section[data-testid="stSidebar"] .stButton button:hover p {
color: #4338CA !important;
}


/* =========================================================
   CHAT MESSAGE
========================================================= */

[data-testid="stChatMessage"] {
border-radius: 16px !important;
padding: 14px !important;
margin-bottom: 14px !important;
}


/* User */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
background: #EEF2FF !important;
border: 1px solid #C7D2FE !important;
}


/* Assistant */

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
background: #FFFFFF !important;
border: 1px solid #E2E8F0 !important;
}


/* Chat text */

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] span,
[data-testid="stChatMessage"] div {
color: #1E293B !important;
}


/* =========================================================
   CHAT INPUT
========================================================= */

[data-testid="stChatInput"] {
background: #FFFFFF !important;
}

[data-testid="stChatInput"] textarea {
background: #FFFFFF !important;
color: #1E293B !important;
caret-color: #4F46E5 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
color: #94A3B8 !important;
}


/* =========================================================
   SOURCE TITLE
========================================================= */

.sources-title {
color: #4338CA !important;
font-size: 16px !important;
font-weight: 700 !important;
margin-top: 18px;
margin-bottom: 10px;
}


/* =========================================================
   SOURCE CARD
========================================================= */

.source-card {
background: #EEF2FF !important;
border: 1px solid #C7D2FE !important;
border-left: 5px solid #4F46E5 !important;
border-radius: 10px !important;
padding: 12px 15px !important;
margin: 8px 0 !important;
color: #1E293B !important;
}

.source-card * {
color: #1E293B !important;
}


/* =========================================================
   HEADINGS
========================================================= */

h1, h2, h3, h4, h5, h6 {
color: #1E293B !important;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton button {
background: #4F46E5 !important;
color: #FFFFFF !important;
border: none !important;
border-radius: 10px !important;
font-weight: 600 !important;
}

.stButton button p {
color: #FFFFFF !important;
}

.stButton button:hover {
background: #4338CA !important;
}


/* =========================================================
   FOOTER
========================================================= */

.footer-box {
background: #FFFFFF !important;
border: 1px solid #E2E8F0 !important;
border-radius: 14px !important;
padding: 22px !important;
margin-top: 45px !important;
text-align: center !important;
color: #64748B !important;
}

.footer-box * {
color: #64748B !important;
}

.footer-box strong {
color: #1E293B !important;
}


/* =========================================================
   DIVIDER
========================================================= */

hr {
border-color: #E2E8F0 !important;
}


/* =========================================================
   ALERTS / INFO
========================================================= */

[data-testid="stAlert"] p {
color: #1E293B !important;
}


/* =========================================================
   SPINNER
========================================================= */

[data-testid="stSpinner"] {
color: #4F46E5 !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="brand-container">
<div class="brand-icon">🏛️</div>
<div class="main-title">Policy<span class="brand-name">Pilot</span></div>
<div class="subtitle">AI-powered policy assistant for intelligent, document-grounded answers</div>
</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# POLICY ENGINE
# ============================================================

@st.cache_resource
def load_policy_engine():
    return PolicyEngine()


try:
    engine = load_policy_engine()

except Exception as error:

    st.error("❌ PolicyPilot could not initialize.")

    st.code(
        f"{type(error).__name__}: {error}"
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🏛️ PolicyPilot")

    st.write(
        "Ask questions about company policies "
        "and get answers directly from policy documents."
    )

    st.divider()

    st.markdown("### 💡 Try asking")

    examples = [
        "What is the remote work policy?",
        "How many annual leave days are available?",
        "What is the sick leave policy?",
        "What benefits are available to employees?",
    ]

    for example in examples:

        if st.button(
            example,
            use_container_width=True,
        ):

            st.session_state.pending_question = example

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True,
    ):

        st.session_state.messages = []

        if "pending_question" in st.session_state:
            del st.session_state.pending_question

        st.rerun()

    st.divider()

    st.caption(
        "🔎 Answers are generated from retrieved "
        "policy documents."
    )


# ============================================================
# SOURCE DISPLAY
# ============================================================

def display_sources(sources):

    if not sources:
        return

    st.markdown(
        '<div class="sources-title">📚 Sources</div>',
        unsafe_allow_html=True,
    )

    for source in sources:

        if isinstance(source, dict):

            name = (
                source.get("source")
                or source.get("document")
                or source.get("file")
                or source.get("title")
                or "Policy Document"
            )

            page = source.get("page")

            if page is not None:
                source_text = f"📄 {name} — Page {page}"
            else:
                source_text = f"📄 {name}"

        else:

            source_text = f"📄 {source}"

        st.markdown(
            f'<div class="source-card">{source_text}</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# PREVIOUS CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and message.get("sources")
        ):

            display_sources(
                message["sources"]
            )


# ============================================================
# INPUT
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
# PROCESS QUESTION
# ============================================================

if question:

    # User

    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )


    # Assistant

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Searching policy documents..."
        ):

            try:

                result = engine.ask(
                    question
                )

                if isinstance(result, dict):

                    answer = result.get(
                        "answer",
                        "No answer was returned.",
                    )

                    sources = result.get(
                        "sources",
                        [],
                    )

                else:

                    answer = str(result)
                    sources = []


                # Answer

                st.markdown(answer)


                # Sources

                display_sources(
                    sources
                )


                # Save

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )


            except Exception as error:

                st.error(
                    "❌ PolicyPilot could not process "
                    "your question."
                )

                st.code(
                    f"{type(error).__name__}: {error}"
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer-box">
<strong>PolicyPilot</strong> • AI Policy Assistant
<br><br>
Grounded answers powered by Retrieval-Augmented Generation
</div>
""",
    unsafe_allow_html=True,
)
