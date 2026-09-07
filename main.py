
import streamlit as st
from langchain_ollama import ChatOllama


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

.chat-title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    margin-bottom: 5px;
}

.chat-subtitle {
    text-align: center;
    color: #888;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="chat-title">🤖 AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="chat-subtitle">Powered by Llama 3.2 + Ollama</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

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

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.markdown("### About")

    st.write(
        "This chatbot uses a local Llama 3.2 model "
        "through Ollama. No OpenAI API credits are required."
    )


# =========================================================
# CREATE MODEL
# =========================================================

model = ChatOllama(
    model="llama3.2",
    temperature=temperature
)


# =========================================================
# CHAT MEMORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY PREVIOUS MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================

user_message = st.chat_input(
    "💬 Ask me anything..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_message:

    # Add user message to memory
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    # Display user message
    with st.chat_message("user"):

        st.markdown(user_message)


    # =====================================================
    # GENERATE AI RESPONSE
    # =====================================================

    with st.chat_message("assistant"):

        with st.spinner("🤔 Thinking..."):

            try:

                # Send conversation history to model
                response = model.invoke(
                    st.session_state.messages
                )

                answer = response.content

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"❌ Error while generating response:\n\n{e}"
                )
