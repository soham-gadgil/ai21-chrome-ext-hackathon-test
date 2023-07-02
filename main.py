import os

import ai21
import streamlit as st
from dotenv import load_dotenv

# Load secrets
load_dotenv()

API_KEY = os.getenv("AI21_LABS_API_KEY")

ai21.api_key = API_KEY

PROMPT = "Provide a list of the top 10 Chrome extensions that would be best suited to help users solve their problem.\nDescription of problem: {description}\n List: "

# Initialization
if "output" not in st.session_state:
    st.session_state["output"] = "Output:"


def give_ext(inp):
    if not len(inp):
        return None

    prompt = PROMPT.format(description=inp)

    response = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        temperature=0.5,
        minTokens=1,
        maxTokens=600,
        numResults=10,
    )

    st.session_state["output"] = response.completions[0].data.text


st.title("Chrome Extension Recommender")

st.write(
    "This is a simple **Streamlit** app that gives the name of the best Chrome Extension based on given description of a problem"
)


inp = st.text_area("Enter your description of your problem here", height=100)
st.button("Suggest", on_click=give_ext(inp))
st.write(f"Answer: {st.session_state.output}")

