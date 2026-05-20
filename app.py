import os
import time
from dotenv import load_dotenv

import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* Title Styling */
.main-title {
    font-size: 3rem;
    font-weight: 700;
    text-align: center;
    color: white;
    margin-bottom: 0.5rem;
    animation: fadeIn 1.2s ease-in;
}

/* Subtitle */
.sub-text {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    animation: fadeIn 2s ease-in;
}

/* Response Box */
.response-box {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
    animation: slideUp 0.5s ease-in-out;
}

/* Input Box */
.stTextInput > div > div > input {
    background-color: #0f172a;
    color: white;
    border-radius: 12px;
    border: 1px solid #475569;
    padding: 12px;
}

/* Button */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    font-weight: bold;
    border: none;
    padding: 12px;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 0px 12px rgba(124,58,237,0.7);
}

/* Watermark */
.watermark {
    position: fixed;
    bottom: 15px;
    right: 20px;
    color: rgba(255,255,255,0.35);
    font-size: 14px;
    font-weight: 600;
    z-index: 9999;
    user-select: none;
    pointer-events: none;
    letter-spacing: 1px;
}

/* Animations */
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0px);
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- ENV VARIABLES ----------------
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# LangSmith
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🤖 AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-text">Ask anything.</div>',
    unsafe_allow_html=True
)

# ---------------- PROMPT TEMPLATE ----------------
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional AI assistant. "
            "Give concise, accurate, and helpful answers."
        ),
        ("user", "Question: {question}")
    ]
)

# ---------------- MODEL ----------------
llm = ChatOpenAI(
    model="gpt-5.5",
    temperature=0.2
)

# ---------------- OUTPUT PARSER ----------------
output_parser = StrOutputParser()

# ---------------- CHAIN ----------------
chain = prompt | llm | output_parser

# ---------------- INPUT AREA ----------------
input_text = st.text_input(
    "💬 Enter your question:",
    placeholder="Ask me anything..."
)

generate = st.button("🚀 Generate Response")

# ---------------- RESPONSE ----------------
if generate and input_text:

    with st.spinner("Thinking..."):

        response = chain.invoke(
            {"question": input_text}
        )

        time.sleep(0.5)

    st.markdown(
        f"""
        <div class="response-box"
             style="border-left: 5px solid #8b5cf6;
                    margin-top:20px;">
            <b>🤖 AI Response:</b><br><br>
            {response}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- WATERMARK ----------------
st.markdown(
    """
    <div class="watermark">
        Developed by KK
    </div>
    """,
    unsafe_allow_html=True
)