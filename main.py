import re
import os

import ai21
import streamlit as st
from dotenv import load_dotenv
from googlesearch import search

# Load secrets
load_dotenv()

API_KEY = os.getenv("AI21_LABS_API_KEY")

ai21.api_key = API_KEY

if "output" not in st.session_state:
    st.session_state["output"] = ""

def lmm_call(prompt):
    response = ai21.Completion.execute(
        model="j2-grande-instruct",
        prompt=prompt,
        temperature=0.5,
        minTokens=1,
        maxTokens=256,
        numResults=10,
    )

    answer = response.completions[0].data.text
    return answer


def give_ext(inp):

    if not len(inp):
        return None

    PROMPT_FORMAT = "Provide a list of the top 10 Chrome extensions that would be best suited to help users solve their problem.\nDescription of problem: {description}\n List: "
    prompt = PROMPT_FORMAT.format(description=inp)

    answer = lmm_call(prompt)
    lines = answer.split('\n')

    ext_names = []

    # If LLM gives answer on 1 line
    if len(lines) == 1:
        # Split by number fullstop and space, then remove space from all except last entry
        lines = re.split('\d+. ', lines[0])
        for line in lines:
            if len(line) > 1:
                last_char = line[-1:]
                if last_char == ' ':
                    ext_names.append(line[:-1])
                else:
                    ext_names.append(line)
    else:
        # For each line LLM gives, split number from app name and and read in ext name
        ext_names = []
        for suggestion in [line.split('. ') for line in lines]:
            if len(suggestion) == 2:
                ext_names.append(suggestion[1])

        ext_names = list(dict.fromkeys(ext_names))

    results = []
    for name in ext_names:
        prompt = f"Describe the chrome extension that has the following name.\nName: {name}\n Answer: "
        ext_desc = lmm_call(prompt)

        ext_link = None
        for answer in search(f'Chrome extension {name}', tld="com", num=10, stop=10, pause=1):
            ext_link = answer
            break

        results.append([name, ext_desc, ext_link])

    for result in results:
        print(result)
        print("--- --- ---")

inp = st.text_area("Enter your description of your problem here", height=100)
st.button("Suggest", on_click=give_ext, args=[inp])
st.write(f"Answer: {st.session_state.output}")