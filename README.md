import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viora AI Assistant", page_icon="🤖")

st.title("🤖 Viora AI Assistant")
st.write("Welcome! Yeh aapka apna AI app hai.")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    user_input = st.text_input("Apna sawal yahan likhein:")

    if st.button("Ask AI"):
        if user_input:
            with st.spinner("AI is thinking..."):
                try:
                    response = model.generate_content(user_input)
                    st.success("AI Response:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.warning("Pehle kuch type karein!")
else:
    st.sidebar.warning("Pehle apni API Key enter karein!")
    st.info("👈 Left side (Sidebar) mein apni Gemini API Key enter karein taake app chal sake.")
