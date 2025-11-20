import google.generativeai as genai
import os
from dotenv import load_dotenv
from retrieval import retrieval
import json
import time
import streamlit as st

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key not set")
genai.configure(api_key=api_key)

def retrieve_part_number(base_query):
    """
    Retrieves the part number information present in the database according to the query given by the users
    Args:
    base_query :The hght level query provided by the users.
    """
    print(f"--- Tool Called with query: {base_query} ---")
    retrieved_products = retrieval(base_query)  
    print(f"Documents found: {len(retrieved_products)}")
    return retrieved_products 


SYSTEM_PROMPT = """
Your task is to help the user who is a customer focused on mechanical parts details.
Your ONLY source of truth is the tool `retrieve_part_number`.

### WORKFLOW
1. You MUST call the tool `retrieve_part_number` for every query.
2. Analyze the retrieved JSON data.
3. Classify the intent (Category 1, 2, or 3) and display the answer in a Markdown Table.

### STRICT CLASSIFICATION & DISPLAY RULES

**CATEGORY 1: EXACT PART NUMBER (Highest Priority)**
- IF User Query EXACTLY matches a "Part Number Name" in the docs:
- DISPLAY ONLY that 1 matching product in a table.
- IGNORE all other docs.

**CATEGORY 2: SUBCATEGORY**
- IF User Query matches a "Subcategory" value:
- DISPLAY ALL products belonging to that Subcategory.
- IGNORE products from other subcategories.

**CATEGORY 3: DIMENSION / GENERAL**
- IF query is about dimensions (e.g., "10mm", "width") or general terms:
- DISPLAY ALL relevant retrieved products.
- **SCHEMA SPLITTING RULE:** 
  - Group products by their attribute keys. 
  - If Product A has attributes [Price, Width] and Product B has [Price, Width, Thread], they MUST be in separate tables.
  - Do not merge different schemas.

### OUTPUT RULES
- Output ONLY the table(s).
- Always include the "URL" column.
- If a value is missing, put "-".
- Do not include conversational filler like "Here is the table".
"""
def chat(prompt: str):
    model_name = "gemini-2.5-flash-lite"
    
    chat_model = genai.GenerativeModel(
        model_name=model_name,
        tools=[retrieve_part_number],
        system_instruction=SYSTEM_PROMPT
    )
    
    chat_session = chat_model.start_chat(enable_automatic_function_calling=True)
    
    llm_time_start = time.perf_counter()
    
    try:
        response = chat_session.send_message(prompt)
    
        final_answer = ""
        
        if hasattr(response, "text") and response.text:
            final_answer = response.text
        else:
            try:
                final_answer = response.candidates[0].content.parts[0].text
            except:
                final_answer = "[Error: LLM returned no text output]"
    
    except Exception as e:
        return f"Error during generation: {e}"

    llm_time_end = time.perf_counter()
    llm_time = llm_time_end - llm_time_start
    
    with open("LLm-generation_time.txt", "a", encoding="utf-8") as f:
        f.write(f"Query: {prompt} \n Time of response: {llm_time}\n\n")
        
    return final_answer


def main_ui():
    st.set_page_config(page_title="Misumi Cam Follower RAG Assistant", layout="wide")
    st.markdown("""
        <style>
            /* Force the main container to be left-aligned */
            .block-container {
                max-width: 100%;
                padding-left: 2rem;
                padding-right: 2rem;
                margin-left: 0;
            }
            /* Align headers and text to left */
            h1, p, div {
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title(" Misumi Cam Follower RAG Assistant")
    st.write("Ask anything about Misumi cam follower part numbers, specs, or categories.")
    col1, col2 = st.columns([1, 1]) 
    
    with col1:
        user_query = st.text_input("Enter your query:", placeholder="e.g., Show details for CFUA-3")

        if st.button("Send"):
            if not user_query.strip():
                st.warning("Please enter a query.")
            else:
                with st.spinner("Processing your request..."):
                    try:
                        response = chat(user_query)
                        st.success("Response:")
                        st.markdown(response) 
                    except Exception as e:
                        st.error(f"Error: {e}")

if __name__ == "__main__":
    main_ui()