import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viora AI Assistant", page_icon="🤖")

st.title("🤖 Viora AI Assistant")
st.write("Welcome! Yeh aapka apna AI app hai.")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")
save_key = st.sidebar.button("Save API Key")

if api_key:
    genai.configure(api_key=api_key)
    try:
        # Aapka pasandida model
        model = genai.GenerativeModel('gemini-pro')
        st.sidebar.success("Model: gemini-pro connected! ✅")
        
        user_input = st.text_input("Apna sawal yahan likhein:")
        if st.button("Ask AI"):
            if user_input:
                with st.spinner("AI is thinking..."):
                    response = model.generate_content(user_input)
                    st.success("AI Response:")
                    st.write(response.text)
            else:
                st.warning("Pehle kuch type karein!")
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.sidebar.info("👈 Please enter your Gemini API Key.")
