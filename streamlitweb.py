import os

import ai21
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load secrets
load_dotenv()

API_KEY = os.getenv("AI21_LABS_API_KEY")

ai21.api_key = API_KEY
#Webpage
height = 500
width = 1000

def main():
 # Load the image
    image = Image.open("logo-removebg.png")

    # Resize the image
    icon_size = (128, 64)
    resized_image = image.resize(icon_size)

    # CSS styling to position the image in the top-left corner and adjust its size
    st.markdown(
        """
        <style>
        .icon {
            width: """ + str(icon_size[0]) + """px;
            height: """ + str(icon_size[1]) + """px;
            position: absolute;
            top: 10px;
            left: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Display the image as an icon in the top-left corner
    st.image(resized_image, use_column_width=False)
    # Rest of your Streamlit app code goes here
    st.markdown("<h1 style='text-align: center; color: black;'>Made for all chrome users</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Simple. Effortless. Accurate.</h5>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        .stButton>button {
            display: block;
            margin: 0 auto;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Create a container to hold the buttons
    col1, col2, col3, col4 = st.columns(4)
    with col2:
        st.button("👆 Download")
    
    with col3:
        st.button("👆 Github")
    st.markdown("<h3 style='text-align: left; color: black;'>How does PinEx work?</h3>", unsafe_allow_html=True)
    st.markdown("<subh3 style='text-align: left; color: black;'>Simply describe the problem you're trying to solve in the chatbox, and let PinEx work its magic. PinEx will analyze your needs and match you with the most efficient Chrome extension available in the store.</subh3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left; color: black;'>DEMO</h3>", unsafe_allow_html=True)
    st.video("testvideo.mp4")
    st.markdown("<h3 style='text-align: left; color: black;'>FAQs</h3>", unsafe_allow_html=True)
    
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

    with st.expander("class='expander-header'>Is PinEx powered by?"):
        st.markdown("<p class='expander-header'>PinEx is a Chrome extension built using TypeScript and powered by ChatGPT.</p>", unsafe_allow_html=True)
    with st.expander("Is PinEx free to use?"):
        st.markdown("<p class='expander-header'>Is PinEx free to use?</p>", unsafe_allow_html=True)
        st.write("PinEx extension is completely free to use.")
if __name__ == "__main__":
    main()
    
import base64
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
add_bg_from_local('bg3.jpg') 