import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="Viora AI Pro", page_icon="🤖")

st.title("🤖 Viora AI Pro")

# 1. API Key Section
api_key = st.text_input("Gemini API Key:", type="password")

# 2. Camera aur Save Section (Chat se upar)
if api_key:
    # Hum ek expander bana rahe hain taake camera ki jagah alag ho
    with st.expander("📷 Tasveer Lein aur Save Karein", expanded=False):
        camera_photo = st.camera_input("Apne device ka camera use karein")
        
        if camera_photo is not None:
            # Tasveer screen par dikhayein
            st.image(camera_photo, caption="Li gayi tasveer")
            
            # Download/Save Button - Yeh zaruri hai taake tasveer gallery mein jaye
            btn = st.download_button(
                label="💾 Download/Save Tasveer",
                data=camera_photo,
                file_name="viora_captured_photo.jpg",
                mime="image/jpeg"
            )

# 3. Chat Section
else:
    st.info("👈 Pehle API Key enter karein.")

if api_key:
    genai.configure(api_key=api_key)
    try:
        # Model set karein
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
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
