import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Know Your Candidate – Political AI Assistant", layout="wide")

st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
    color: #FFFFFF;
}
.stTextInput > div > div > input {
    background-color: #31333F;
    color: #FFFFFF;
}
.stTextInput > label {
    color: #FFFFFF;
}
div.stButton > button {
    display: block;
    width: 100%;
    padding: 1rem;
    margin: 0.5rem 0;
    border: 1px solid #565656;
    border-radius: 0.5rem;
    background-color: #21252B;
    color: #FFFFFF;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
}
div.stButton > button:hover {
    border-color: #888888;
    background-color: #2C3038;
}
div.stButton > button:disabled {
    background-color: #2C3038;
    color: #AAAAAA;
    cursor: not-allowed;
}
</style>
""", unsafe_allow_html=True)

st.title("🇺🇸 Know Your Candidate – Political AI Assistant")
st.markdown("Stay informed. Instantly learn about **U.S. politicians** – their **promises**, **voting records**, **speeches**, and more with one click.")

name = st.text_input("👤 Enter a politician's name (e.g., 'AOC', 'Donald Trump')")

if name:
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    selected_feature = None
    label = None

    with col1:
        if st.button("📜 Promises / Manifestos"):
            selected_feature = "promises"
            label = "Campaign Promises"
    with col2:
        if st.button("📊 Voting Records & Bills"):
            selected_feature = "voting"
            label = "Voting Records & Bills"
    with col3:
        if st.button("📰 News & Fact Checks"):
            selected_feature = "news"
            label = "News & Fact Checks"

    with col4:
        if st.button("🎤 Analyze Speeches"):
            selected_feature = "speeches"
            label = "Speech Analysis"
    with col5:
        st.button("🔀 Compare Candidates (Coming Soon)", disabled=True)
    with col6:
        if st.button("👶 Explain Like I'm 5"):
            selected_feature = "eli5"
            label = "ELI5 Summary"

    if selected_feature:
        query_map = {
            "promises": f"What are the 2024 campaign promises made by {name}?",
            "voting": f"Summarize {name}'s voting record and political stance based on bills supported or opposed.",
            "news": f"What are the latest verified news headlines or fact checks related to {name}?",
            "speeches": f"Analyze the political speeches made by {name}. What themes or issues are often addressed?",
            "eli5": f"Explain {name}'s politics in very simple terms, like I'm 5 years old."
        }

        query = query_map[selected_feature]

        st.markdown("---")
        st.subheader(f"🔍 {label} for {name}")

        with st.spinner("Thinking like a political analyst..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant specialized in American politics."},
                        {"role": "user", "content": query}
                    ]
                )
                st.markdown(response.choices[0].message.content.strip())
            except Exception as e:
                st.error(f"⚠️ GPT error: {e}")
else:
    st.info("👆 Please enter a politician’s name to get started.")

st.warning("🚧 This app is still under active development. Features may change or expand soon!")
