import re
import os
from dotenv import load_dotenv
import ai21
import streamlit as st
from googlesearch import search
import base64
from PIL import Image
from requests import exceptions as req_exceptions

load_dotenv()


# Initialize session state
if "output" not in st.session_state:
    st.session_state["output"] = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_and_validate_api_key():
    AI21_API_KEY = st.text_input("Please enter your AI21 Labs API Key", type="password")
    
    # Check if API Key is provided
    if not AI21_API_KEY:
        st.error("API Key is required to run the demo.")
        st.markdown(
            """
            You can register for an API key [here](https://studio.ai21.com/account/api-key).
            """
        )
        return False

    # Set the API key for use in ai21 library
    ai21.api_key = AI21_API_KEY
    
    # Run a test API call to check if the key is valid
    try:
        ai21.Completion.execute(model="j2-light", prompt="Test", temperature=0.5, min_tokens=1, max_tokens=10, num_results=1)
        return True

    except Exception as e:
        if "401 Client Error" in str(e) or '403 Forbidden' in str(e): # 403 Forbidden can also indicate an invalid key
            st.error("The provided API Key is not valid.")
        else:
            st.error(f"An error occurred: {e}")
        return False

def execute_lmm_call(model: str, prompt: str, temperature: float, min_tokens: int, max_tokens: int, num_results: int) -> str:
    response = ai21.Completion.execute(
        model=model,
        prompt=prompt,
        temperature=temperature,
        min_tokens=min_tokens,
        max_tokens=max_tokens,
        num_results=num_results,
    )
    return response.completions[0].data.text

def generate_prompt(format: str, description: str) -> str:
    return format.format(description=description)

def search_links(name: str) -> str:
    # Format the name to fit within a Google search URL
    name_formatted = name.replace(' ', '+')
    # Generate the Google search URL
    link = f'https://www.google.com/search?q=Chrome+extension+{name_formatted}+web+store'
    return link


def extract_extensions_from_answer(answer: str) -> list:
    ext_names = re.split('\d+. ', answer)
    ext_names = [name[:-1] if name.endswith(' ') else name for name in ext_names if len(name) > 1]
    return list(dict.fromkeys(ext_names))

def generate_extension_list(problem_desc: str) -> None:
    prompt_format = "Provide a list of the top 10 Chrome extensions that would be best suited to help users solve their problem.\nDescription of problem: {description}\n List: "
    prompt = generate_prompt(prompt_format, problem_desc)
    answer = execute_lmm_call("j2-grande-instruct", prompt, 0.5, 1, 256, 10)
    extension_names = extract_extensions_from_answer(answer)

    results = []
    for name in extension_names:
        prompt = f"Describe the chrome extension that has the following name.\nName: {name}\n Answer: "
        ext_desc = execute_lmm_call("j2-light", prompt, 0.5, 1, 256, 10)
        ext_link = search_links(name)
        results.append([name, ext_desc, ext_link])

    return results

def demo():
    # Retrieve and validate API key
    if not get_and_validate_api_key():
        return

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if problem_desc := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(problem_desc)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": problem_desc})

        # Generate extension list
        extension_list = generate_extension_list(problem_desc)

        for result in extension_list:
            name, ext_desc, ext_link = result
            response = f"Extension name: {name}\nDescription: {ext_desc}\nLink: {ext_link}"
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})


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
    render_styling()
    render_logo()
    render_app_contents()
    add_background()

def render_styling():
    # CSS Styling for icon and webpage
    icon_size = (128, 64)
    st.markdown(f"""
        <style>
        .icon {{
            width: {icon_size[0]}px;
            height: {icon_size[1]}px;
            position: absolute;
            top: 10px;
            left: 20px;
        }}
        body {{
            background-color: #ffffff; /* Fallback color */
            background-color: rgba(255, 255, 255, 0.5); /* White with 50% opacity */
        }}
        h1, h3, p {{
            color: #000000; /* Fallback color */
            color: rgba(0, 0, 0, 0.9); /* Black with 90% opacity */
        }}
        </style>
        """, unsafe_allow_html=True)

def render_logo():
    # Load and resize the logo image
    image = Image.open("./images/logo.png")
    icon_size = (128, 64)
    resized_image = image.resize(icon_size)
    # Display the image as an icon in the top-left corner
    st.image(resized_image, use_column_width=False, output_format="PNG")

def render_app_contents():
    # App Contents
    st.markdown("<h1 style='text-align: center; color: black;'>Made for all chrome users</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: black;'>Simple. Effortless. Accurate.</h3>", unsafe_allow_html=True)

    render_remaining_content()

    # Add chatbot demo section
    st.markdown("<h3 style='text-align: left; color: #0d0d0d;'>PinEx DEMO (chat bot)</h3>", unsafe_allow_html=True)
    demo() # Call the chatbot function here

def render_remaining_content():
    st.markdown("<h3 style='text-align: left; color: black;'>How does PinEx work?</h3>", unsafe_allow_html=True)
    st.markdown("<subh3 style='text-align: left; color: black;'>Describe the problem you're trying to solve in the chatbox, and let PinEx do its work to fetch you the most relevant Chrome extension available in the store.</subh3>", unsafe_allow_html=True)
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
    with st.expander("What technology is PinEx powered by?"):
        st.markdown("<p class='expander-content'>PinEx is built using Streamlit and powered by J2-Light from AI21 Labs.</p>", unsafe_allow_html=True)
    with st.expander("Is PinExt free to use?"):
        st.markdown("<p class='expander-content'>PinEx is completely free to use.</p>", unsafe_allow_html=True)

def add_background():
    # bg_image = Image.open('./images/bg3.jpg')
    # st.image(bg_image, use_column_width=True)
    add_bg_from_local('./images/bg3.jpg')

if __name__ == "__main__":
    main()
