import os
import ai21
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
import base64

# Load secrets
load_dotenv()

API_KEY = os.getenv("AI21_LABS_API_KEY")
ai21.api_key = API_KEY

# Webpage dimensions
height = 500
width = 1000

def button_markdown(button_text, button_link, col):
    button_code = f"""
        <a href='{button_link}' style='display: block; margin: 0 auto; text-align: center;vertical-align: center; '>
            <button style='background-color: #0d0d0d; border: none; width: 150px; height:45px; color: white; padding: 15px 32px; text-align: center; vertical-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 4px; cursor: pointer; border-radius: 12px;'>
                {button_text}
            </button>
        </a>
        """
    col.markdown(button_code, unsafe_allow_html=True)

def load_and_display_image(image_path, icon_size=(128, 64)):
    # Load the image
    image = Image.open(image_path)

    # Resize the image
    resized_image = image.resize(icon_size)

    # Display the image
    st.image(resized_image, use_column_width=False)

def display_markdown_text(text, align='center', color='black', tag='h1'):
    st.markdown(f"<{tag} style='text-align: {align}; color: {color};'>{text}</{tag}>", unsafe_allow_html=True)

def expander_content(expander_text, content):
    with st.expander(expander_text):
        st.markdown(f"<p class='expander-header'>{content}</p>", unsafe_allow_html=True)

def main():
    load_and_display_image("./images/logo-removebg.png")

    display_markdown_text('Made for all chrome users')
    display_markdown_text('Simple. Effortless. Accurate.', tag='h3')

    # Create a container to hold the buttons
    col1, col2, col3, col4 = st.columns(4)
    button_markdown("👆 Demo", '#', col2)
    button_markdown("👆 Github", 'https://github.com/cnm13ryan/ai21-chrome-ext-hackathon-test', col3)

    display_markdown_text('How does PinEx work?', align='left', tag='h3')
    display_markdown_text('Simply describe the problem you\'re trying to solve in the chatbox, and let PinEx work its magic. PinEx will analyze your needs and match you with the most efficient Chrome extension available in the store.', align='left', color='black', tag='subh3')

    display_markdown_text('DEMO', align='left', color='#0d0d0d', tag='h3')
    st.video("testvideo.mp4")
    
    display_markdown_text('FAQs', align='left', color='#0d0d0d', tag='h3')

    expander_style = """
        <style>
        .expander-header {
            font-size: 20px;
            font-weight: bold;
            color: red;
        }
        .expander-content {
            font-size: 16px;
        }
        </style>
    """
    st.markdown(expander_style, unsafe_allow_html=True)

    expander_content("Is PinEx powered by?", "PinEx is a Chrome extension built using TypeScript and powered by ChatGPT.")
    expander_content("Is PinEx free to use?", "PinEx extension is completely free to use.")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
    add_bg_from_local('./images/bg3.jpg') 
