import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viora AI Pro", page_icon="🤖")

st.title("🤖 Viora AI Pro")

# Buttons for Camera and Voice
col1, col2 = st.columns(2)
with col1:
    if st.button("📷 Open Camera"):
        st.warning("Camera feature ke liye device permissions allow karein.")
        picture = st.camera_input("Take a photo")
with col2:
    if st.button("🎙️ Voice Input"):
        st.warning("Voice feature active hai, bolna shuru karein...")

api_key = st.text_input("Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    try:
        # 100% working model name
        model = genai.GenerativeModel('gemini-3.6-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Apna sawal likhein..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

    except Exception as e:
        st.error(f"Error: {e}")
