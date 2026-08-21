import streamlit as st
import google.generativeai as genai

# Page ki setting
st.set_page_config(page_title="Viora AI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Viora AI Assistant")
st.write("Welcome! Yeh aapka apna chat app hai jo purani baatein yaad rakhta hai.")

# API Key enter karne ki jagah
api_key = st.text_input("Apni Gemini API Key yahan enter karein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    try:
        # Naya aur working model set kiya hai
        model = genai.GenerativeModel('gemini-3.6-flash')
        
        # Chat history ko yaad rakhne ke liye session state
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Purani sari chat screen par dikhane ke liye loop
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Neeche chat input box (jo ek se zyada sawal chalne dega)
        if prompt := st.chat_input("Yahan apna agla sawal likhein..."):
            
            # User ka message screen par dikhayein aur save karein
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # AI ka jawab generate karne ke liye
            with st.chat_message("assistant"):
                with st.spinner("AI soch raha hai..."):
                    response = model.generate_content(prompt)
                    ai_reply = response.text
                    st.markdown(ai_reply)
            
            # AI ka jawab bhi history mein save karein
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Pehle upar apni Gemini API Key enter karein taake chat shuru ho sake.")
