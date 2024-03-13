import streamlit as st
from pathlib import Path
import openai, os, requests
from openai import AzureOpenAI

endpoint = os.environ.get("AOAIEndpoint")
api_key = os.environ.get("AOAIKey")
deployment = os.environ.get("AOAIDeploymentId")

client = AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.title('Personalized Python Tutor')

st.markdown("""Welcome to this e-learning course on Python programming! This course is designed for learners of all levels. Whether you're just starting out or want to master advanced concepts, our adaptive system will tailor lessons and quizzes to your needs.""")

tab1, tab2, tab3 = st.tabs(["Beginner", "Intermediate", "Advance"])

with tab1:
   st.header("Beginner")
   st.markdown(read_markdown_file("basic_python.md"))

with tab2:
   st.header("Intermediate")
   st.markdown(read_markdown_file("intermediate_python.md"))

with tab3:
   st.header("Advance")
   st.markdown(read_markdown_file("advanced_python.md"))


# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages= [{"role": "assistant", "content" : """Hi! I am your Python Programming instructor. To get started, please share your level of experience with the Python. Choose from the following options: Beginner, Intermediate, or Advanced."""}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("Ask something!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            completion = client.chat.completions.create(
                model = deployment,
                messages = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            extra_body={
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": os.environ["SearchEndpoint"],
                        "key": os.environ["SearchKey"],
                        "indexName": os.environ["SearchIndex"],
                        "queryType": "vector",
                        "semanticConfiguration": "default",
                        "inScope": True,
                        "filter": None,
                        "strictness": 3,
                        "topNDocuments": 5,
                        "embeddingDeploymentName": "embedding-model",
                        "roleInformation": """You are a dynamic Python programming instructor. Your role is to assess user's knowledge and provide a tailored learning experience. Based on the user’s response, you will take a quiz on a specific Python topic suitable for their level. If the user answers correctly, increase the difficulty of subsequent questions. If incorrect, provide hints, then either simplify the question or present a similar one at the same level. Your responses should evolve based on the user's experience level and their performance on the quizzes."""
                        }
                }
                ] 
                },
                n = 1,
                temperature=0,
                top_p=1,
                max_tokens=200,
                stop=[],
                stream=False
            )
            #conversation.append({"role": "assistant", "content": completion.choices[0].message.content})

            response = completion.choices[0].message.content
            st.markdown(response)
    
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
