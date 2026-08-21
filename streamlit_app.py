import streamlit as st
import google.generativeai as genai
from PIL import Image
import requests
from io import BytesIO

# Page ki setting
st.set_page_config(page_title="Viora AI Generator", page_icon="🤖")

st.title("🤖 Viora AI Generator")
st.write("Welcome! Yahan aap chart analysis aur image generate karwa sakte hain.")

# API Key input
api_key = st.text_input("Apni Gemini API Key yahan enter karein:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # Tabs banate hain
    tab1, tab2 = st.tabs(["💬 Chart Analysis (Text)", "🖼️ Image Generator"])
    
    # --- Tab 1: Gemini Text Assistant ---
    with tab1:
        st.subheader("Chart Analysis Assistant")
        uploaded_file = st.file_uploader("Analysis ke liye chart upload karein:", type=["jpg", "jpeg", "png"])
        
        image = None
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Chart")

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

    # --- Tab 2: Image Generator (Behtar version) ---
    with tab2:
        st.subheader("Nayi ICT Chart Tasveer Generate Karein")
        st.write("Yahan detail mein likhein ke chart par kya dikhana hai.")
        
        # Default prompt ICT ke liye
        default_ict_prompt = "A professional forex trading chart, cleancandlestick pattern, showing ICT concepts: Fair Value Gap (FVG) marked as a blue shaded box, Order Block highlighted in light grey, Liquidity Grab with a red arrow, Break of Structure (BOS) labeled, white background, high detail"
        
        img_prompt = st.text_area("Tasveer ka tafseel (prompt) likhein:", 
                                 value=default_ict_prompt,
                                 height=150)
        
        if st.button("Generate ICT Image"):
            if img_prompt:
                with st.spinner("Tasveer generate ho rahi hai..."):
                    # Hum Pollinations AI ki free API use kar rahe hain
                    safe_prompt = img_prompt.replace(" ", "%20")
                    # Style aur quality parameters add kiye hain
                    image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1280&height=720&nologo=true&model=realism"
                    
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            gen_image = Image.open(BytesIO(response.content))
                            st.image(gen_image, caption=f"Generated: {img_prompt}", use_column_width=True)
                            
                            # Download button
                            st.download_button(
                                label="💾 Download Generated ICT Image",
                                data=response.content,
                                file_name="viora_ict_chart.jpg",
                                mime="image/jpeg"
                            )
                        else:
                            st.error("Tasveer generate karne mein error aaya.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Pehle prompt likhein.")

else:
    st.info("👈 Pehle API Key enter karein.")
