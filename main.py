import re
import os
from dotenv import load_dotenv
import ai21
import streamlit as st
from googlesearch import search

load_dotenv()
AI21_API_KEY = os.getenv("AI21_LABS_API_KEY")
ai21.api_key = AI21_API_KEY

# Initialize session state
if "output" not in st.session_state:
    st.session_state["output"] = ""

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
    for link in search(f'Chrome extension {name}', tld="com", num=10, stop=10, pause=1):
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
        ext_desc = execute_lmm_call("j2-grande-instruct", prompt, 0.5, 1, 256, 10)
        ext_link = search_links(name)
        results.append([name, ext_desc, ext_link])

    st.session_state["output"] = results

problem_desc = st.text_area("Enter your description of your problem here", height=100)
st.button("Suggest", on_click=generate_extension_list, args=[problem_desc])
st.write(f"Answer: {st.session_state.output}")
