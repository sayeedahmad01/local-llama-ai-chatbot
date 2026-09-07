import streamlit as st
from utils.chatbot import create_model, get_response


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Powered by Llama 3.2 + Ollama</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### 🤖 About")

    st.write(
        """
        This is a local AI chatbot built with:

        - Streamlit
        - LangChain
        - Ollama
        - Llama 3.2

        No OpenAI API credits are required.
        """
    )


# ============================================================
# CHAT MODEL
# ============================================================

try:

    model = create_model(
        temperature=temperature
    )

except Exception as e:

    st.error(
        "Unable to initialize the AI model."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# INITIALIZE CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

user_message = st.chat_input(
    "💬 Ask me anything..."
)


# ============================================================
# PROCESS MESSAGE
# ============================================================

if user_message:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_message)


    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                answer = get_response(
                    model,
                    st.session_state.messages
                )

                st.markdown(answer)

                # Save assistant response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ Error generating response:\n\n{e}"
                )