import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

# Page ki setting - Sirf Tab 2 wala hissa
st.set_page_config(page_title="Viora AI Generator", page_icon="🤖")

st.title("🤖 Viora AI Generator")
st.write("Welcome! Yahan aap chart analysis aur image generate karwa sakte hain.")

# API Key input
api_key = st.text_input("Apni Gemini API Key yahan enter karein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Tabs banate hain
    tab1, tab2 = st.tabs(["💬 Chart Analysis (Text)", "🖼️ Image Generator"])
    
    # --- Tab 1: Gemini Text Assistant (Pehle wala kam) ---
    with tab1:
        st.subheader("Chart Analysis Assistant")
        uploaded_file = st.file_uploader("Analysis ke liye chart upload karein (optional):", type=["jpg", "jpeg", "png"])
        
        image = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Chart", use_column_width=True)

        user_prompt = st.text_area("Apna sawal ya analysis ICT/SMC ke mutabiq likhein:")
        
        if st.button("Ask AI Analysis"):
            if user_prompt:
                with st.spinner("AI analysis kar raha hai..."):
                    model = genai.GenerativeModel('gemini-3.6-flash')
                    if image:
                        response = model.generate_content([user_prompt, image])
                    else:
                        response = model.generate_content(user_prompt)
                    st.markdown("### AI Analysis:")
                    st.write(response.text)
            else:
                st.warning("Pehle kuch likhein.")

    # --- Tab 2: Image Generator (Updated Stability) ---
    with tab2:
        st.subheader("Nayi Tasveer Generate Karein")
        st.write("Tasveer ka tafseel (prompt) English mein likhein:")
        
        # Default prompt for ICT Chart
        default_ict = "A professional forex trading chart of XAUUSD, clean candlestick pattern, white background, showing ICT concepts like Order Block, Fair Value Gap, and Liquidity Grab with precise labels"
        
        img_prompt = st.text_area("Tasveer ka prompt:", 
                                 value=default_ict,
                                 height=150,
                                 placeholder="e.g., A futuristic city at sunset with flying cars")
        
        if st.button("Generate Image"):
            if img_prompt:
                with st.spinner("Tasveer generate ho rahi hai... (kuch seconds wait karein)"):
                    # Hum Pollinations AI ki updated free API use kar rahe hain
                    safe_prompt = img_prompt.replace(" ", "%20")
                    # Model aur nologo add kiye hain
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1280&height=720&nologo=true&model=turbo"
                    
                    try:
                        response = requests.get(image_url, timeout=30) # Timeout set kiya hai
                        if response.status_code == 200:
                            gen_image = Image.open(BytesIO(response.content))
                            st.image(gen_image, caption=f"Generated: {img_prompt}", use_column_width=True)
                            
                            # Download button
                            st.download_button(
                                label="💾 Download Generated Image",
                                data=response.content,
                                file_name="viora_generated_image.jpg",
                                mime="image/jpeg"
                            )
                        else:
                            st.error(f"Tasveer generate karne mein error aaya (Code: {response.status_code}). Free API busy ho sakti hai, dobara try karein.")
                    except requests.exceptions.Timeout:
                        st.error("Error: Request timeout ho gayi. Internet connection check karein ya dobara try karein.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Pehle tasveer ka prompt likhein.")

else:
    st.info("👈 Pehle API Key enter karein.")
