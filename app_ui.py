import streamlit as st 
from openai import OpenAI 
from dotenv import load_dotenv 
import os 

load_dotenv() 
client = OpenAI(    
    api_key=os.getenv("GROQ_API_KEY"),   
    base_url="https://api.groq.com/openai/v1" ) 
st.title(" 🤖 My AI Assistant") 
question = st.text_input("Ask your question:") 
if st.button("Ask AI"):    
    if question:        
        response = client.chat.completions.create(            
        model="openai/gpt-oss-20b",            
        messages=[{"role": "user", "content": question}]        
        )        
        answer = response.choices[0].message.content        
        st.subheader("AI Response")        
        st.write(answer)   
        
    else:        
        st.warning("Please enter a question.")
