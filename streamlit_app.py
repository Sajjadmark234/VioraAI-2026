import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Viora AI Assistant", page_icon="🤖")

st.title("Assistant")
st.write("Welcome! Yeh aapka apna AI app hai.")

# API Key input
api_key = st.text_input("Apni Gemini API Key yahan enter karein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    st.success("API Key Connected Successfully! ✅")
    
    try:
        # Model set kiya hai
        model = genai.GenerativeModel('gemini-3.6-flash')
        
        # 📷 Yahan Image/Picture Upload ka option hai (Gallery ya Camera se)
        uploaded_file = st.file_uploader("Tasveer upload karein ya camera se lein:", type=["jpg", "jpeg", "png"])
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Sawal likhne ki jagah
        user_input = st.text_area("Apna sawal yahan likhein:")
        
        if st.button("Ask AI"):
            if user_input or uploaded_file:
                with st.spinner("AI jawab de raha hai..."):
                    # Agar tasveer aur sawal dono hain
                    if uploaded_file is not None:
                        response = model.generate_content([user_input, uploaded_file.getvalue()])
                    else:
                        response = model.generate_content(user_input)
                    
                    st.markdown("### AI Response:")
                    st.write(response.text)
            else:
                st.warning("Pehle kuch likhein ya tasveer upload karein.")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("👈 Pehle upar apni API Key enter karein.")
