import streamlit as st
from agent import run_agent
st.title("🤖 AI Agent")
st.write("Ask the AI Agent to perform a calculation.")
question = st.text_input("Your question:")
if st.button("Ask Agent"):
    if question:
        with st.spinner("Agent is thinking..."):
            answer = run_agent(question)
            st.subheader("Agent Response")
    st.write(answer)
else:
    st.warning("Please enter a question.")
  
    
