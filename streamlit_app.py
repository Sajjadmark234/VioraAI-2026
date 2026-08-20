import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viora AI Assistant", page_icon="🤖")

st.title("🤖 Viora AI Assistant")
st.write("Welcome! Yeh aapka apna AI app hai.")

api_key = st.text_input("Apni Gemini API Key yahan enter karein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    try:
        # Error message ke mutabiq naya model
        model = genai.GenerativeModel('gemini-3.6-flash')
        st.success("API Key Connected Successfully! ✅")
        
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
    st.info("👈 Pehle upar apni Gemini API Key enter karein taake app khul sake.")
