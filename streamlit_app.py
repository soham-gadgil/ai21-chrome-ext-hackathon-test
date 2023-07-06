import os
import ai21
import streamlit as st
import base64
from PIL import Image
from dotenv import load_dotenv

# Load secrets
load_dotenv()

API_KEY = os.getenv("AI21_LABS_API_KEY")

ai21.api_key = API_KEY

# Load secrets
load_dotenv()
# API_KEY = os.getenv("AI21_LABS_API_KEY")
# ai21.api_key = API_KEY

# Webpage dimensions
height = 500
width = 1000

@st.cache_data()
def get_data():
    # replace with your real data loading
    return {"AI21_model_names": ["j2-light", "j2-mid", "j2-ultra"]}

@st.cache_data()
def get_promotion():
    # replace with your real promotion loading
    return {
        "url": "https://example.com",
        "title": "Example title",
        "text": "Example text",
        "image": { "url": "https://example.com/image.png", "size": 128 },
        "footer": { "text": "Example footer text", "url": "https://example.com/footer" },
        "label": { "text": "Example label text", "url": "https://example.com/label" },
    }

data = get_data()
promotion = get_promotion()

# extract the endpoint from the query string
endpoint = st.experimental_get_query_params().get("endpoint", [""])[0]

if endpoint == "config":
    # Write the data as a JSON response
    st.write(data)
elif endpoint == "p":
    # Write the promotion response
    st.write(promotion)
else:
    # rest of your Streamlit app goes here
    # replace with your current application code
    st.write("Welcome to PinExt!")

def img_to_data_url(path):
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"data:image/png;base64,{encoded_string}"


def button_markdown(button_text: str, button_link: str, logo_path: str = None):
    logo_data_url = img_to_data_url(logo_path) if logo_path else None
    button_style = f"""
        <a href='{button_link}' style='display: block; margin: 0 auto; text-align: center;'>
            <button style='background-color: #0d0d0d; border: none; width: 150px; height:45px; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 4px; cursor: pointer; border-radius: 12px;'>
    """
    if logo_data_url:
        button_style += f'<img src="{logo_data_url}" style="height: 20px; width: 20px;" />'
    button_style += f"{button_text}</button></a>"
    return button_style


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    # Load the image
    image = Image.open("./images/logo.png")
    # Resize the image
    icon_size = (128, 64)
    resized_image = image.resize(icon_size)
    # CSS styling to position the image in the top-left corner and adjust its size
    render_styling(icon_size)
    # Display the image as an icon in the top-left corner
    st.image(resized_image, use_column_width=False)
    # Rest of your Streamlit app code goes here
    render_app_contents()

    add_bg_from_local('./images/bg3.jpg')


def render_styling(icon_size):
    # CSS Styling for icon and webpage
    st.markdown(f"""
        <style>
        .icon {{
            width: {icon_size[0]}px;
            height: {icon_size[1]}px;
            position: absolute;
            top: 10px;
            left: 20px;
        }}
        </style>
        """, unsafe_allow_html=True)


def render_app_contents():
    # App Contents
    st.markdown("<h1 style='text-align: center; color: black;'>Made for all chrome users</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Simple. Effortless. Accurate.</h3>", unsafe_allow_html=True)
    
    # Create a container to hold the buttons
    col1, col2, col3, col4 = st.columns(4)
    demo_button = button_markdown("Demo", "#")
    with col2:
        st.markdown(demo_button, unsafe_allow_html=True)

    github_button = button_markdown("Github", "https://github.com/cnm13ryan/ai21-chrome-ext-hackathon-test", "./images/github-g9336db1b6_1280.png")
    with col3:
        st.markdown(github_button, unsafe_allow_html=True)
    # Rest of the content
    render_remaining_content()


def render_remaining_content():
    st.markdown("<h3 style='text-align: left; color: black;'>How does PinEx work?</h3>", unsafe_allow_html=True)
    st.markdown("<subh3 style='text-align: left; color: black;'>Simply describe the problem you're trying to solve in the chatbox, and let PinEx work its magic. PinEx will analyze your needs and match you with the most efficient Chrome extension available in the store.</subh3>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: left; color: #0d0d0d;'>DEMO</h3>", unsafe_allow_html=True)
    st.video("testvideo.mp4")
    st.markdown("<h3 style='text-align: left; color: #0d0d0d;'>FAQs</h3>", unsafe_allow_html=True)
    render_faq()


def render_faq():
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
    with st.expander("Is PinEx powered by?"):
        st.markdown("<p class='expander-content'>PinEx is a Chrome extension built using TypeScript and powered by ChatGPT.</p>", unsafe_allow_html=True)
    with st.expander("Is PinEx free to use?"):
        st.markdown("<p class='expander-content'>PinEx is completely free to use.</p>", unsafe_allow_html=True)
    demo()

def demo():
    PROMPT = "Provide a list of the top 10 Chrome extensions that would be best suited to help users solve their problem.\nDescription of problem: {description}\nList: "

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
if __name__ == "__main__":
    main()
