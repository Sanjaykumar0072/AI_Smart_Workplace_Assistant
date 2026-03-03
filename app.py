import streamlit as st
from ai_engine import ask_ai
from document_utils import read_file

# -----------------------------
# CSS Style Import
# -----------------------------
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="AI Workplace Assistant", layout="centered")

load_css("style.css")
# -----------------------------
# Initialize Session State
# -----------------------------
if "conversations" not in st.session_state:
    st.session_state.conversations = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"

if "document_text" not in st.session_state:
    st.session_state.document_text = None

if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = None


# -----------------------------
# SIDEBAR (Popover Menu Version)
# -----------------------------
st.sidebar.title("💬 Chats")

if "rename_mode" not in st.session_state:
    st.session_state.rename_mode = None

# ➕ New Chat
if st.sidebar.button("New Chat", use_container_width=True):
    new_chat_name = f"Chat {len(st.session_state.conversations) + 1}"
    st.session_state.conversations[new_chat_name] = []
    st.session_state.current_chat = new_chat_name
    st.session_state.document_text = None
    st.rerun()

st.sidebar.markdown("---")


def save_rename(old_name):
    new_name = st.session_state.get(f"rename_input_{old_name}", "").strip()

    if new_name and new_name not in st.session_state.conversations:
        st.session_state.conversations[new_name] = \
            st.session_state.conversations.pop(old_name)

        if st.session_state.current_chat == old_name:
            st.session_state.current_chat = new_name

    st.session_state.rename_mode = None


for chat_name in list(st.session_state.conversations.keys()):

    col1, col2 = st.sidebar.columns([5, 1])

    # -------------------
    # Select Chat Button
    # -------------------
    if col1.button(chat_name, key=f"select_{chat_name}", use_container_width=True):
        st.session_state.current_chat = chat_name
        st.session_state.rename_mode = None
        st.rerun()

    # -------------------
    # Popover Menu
    # -------------------
    with col2:
        with st.popover("⋯"):

            if st.button("✏ Rename", key=f"rename_{chat_name}", use_container_width=True):
                st.session_state.rename_mode = chat_name

            if st.button("🗑 Delete", key=f"delete_{chat_name}", use_container_width=True):

                if len(st.session_state.conversations) > 1:
                    del st.session_state.conversations[chat_name]

                    if st.session_state.current_chat == chat_name:
                        st.session_state.current_chat = list(
                            st.session_state.conversations.keys()
                        )[0]

                st.rerun()

    # -------------------
    # Inline Rename Input
    # -------------------
    if st.session_state.rename_mode == chat_name:
        st.sidebar.text_input(
            "",
            value=chat_name,
            key=f"rename_input_{chat_name}",
            label_visibility="collapsed",
            on_change=save_rename,
            args=(chat_name,)
        )

# -----------------------------
# MAIN TITLE
# -----------------------------
st.title("🤖 AI-Powered Smart Workplace Assistant")

# -----------------------------
# Display Chat History
# -----------------------------
messages = st.session_state.conversations[st.session_state.current_chat]

for message in messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# Sticky Chat Input (File Supported - FIXED)
# -----------------------------
chat_value = st.chat_input(
    "Type your message...",
    accept_file=True,
    file_type=None #Accept all type of files
)

user_input = None
uploaded_file = None

if chat_value:

    # ✅ Correct property in 1.54
    user_input = chat_value.text

    # ✅ File extraction
    if chat_value.files:
        uploaded_file = chat_value.files[0]


# -----------------------------
# Handle File Upload
# -----------------------------
if uploaded_file:
    st.session_state.document_text = read_file(uploaded_file)
    st.toast("📄 Document uploaded successfully")


# -----------------------------
# Handle User Message
# -----------------------------
if user_input:

    messages = st.session_state.conversations[st.session_state.current_chat]
    messages.append({"role": "user", "content": user_input})

    if st.session_state.document_text:
        prompt = f"""
        You are a workplace assistant.

        Use the following document to respond.

        Document:
        {st.session_state.document_text}

        User Request:
        {user_input}
        """
    else:
        prompt = f"""
        You are a professional workplace assistant.

        If the input is long text, summarize it in bullet points.
        Otherwise answer clearly.

        User Input:
        {user_input}
        """

    response = ask_ai(prompt)

    messages.append({"role": "assistant", "content": response})

    st.rerun()