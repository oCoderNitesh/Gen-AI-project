import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from knowledge_assistant import search_knowledge
import os


load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


st.title("📚 Knowledge-Based AI Assistant")

st.write("Ask questions from the provided knowledge base.")


question = st.text_input("Ask your question:")


if st.button("Ask AI"):

    if question:

        relevant_knowledge = search_knowledge(question)

        context = "\n\n".join(relevant_knowledge)


        prompt = f"""
You are a knowledge-based AI assistant.

Answer the user's question using ONLY the information
provided in the knowledge base.

If the answer is not available in the knowledge base,
say:

"I don't have that information in my knowledge base."

Knowledge Base:
{context}

User Question:
{question}
"""


        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        answer = response.choices[0].message.content


        st.subheader("AI Response")
        st.write(answer)


    else:

        st.warning("Please enter a question.")

