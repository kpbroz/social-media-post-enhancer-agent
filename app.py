import streamlit as st
import requests

# Backend API URLs
generate_API_URL = "http://localhost:8000/generate-content/"


# Set up the main header
st.title("Social Media Post Enhancer Agent")

# Input field for post content and context
post_content = st.text_area("Enter the post content and context:", height=200)

# Dropdown for selecting the social media platform
platform = st.selectbox(
    "Select the social media platform:",
    ["Twitter", "Facebook", "Instagram", "Reddit"]
)

# Button to generate the post
if st.button("Generate Post"):
    generated_post = ""
    if post_content.strip() and platform.strip():
        try:
            response = requests.post(generate_API_URL, json={"post_content": post_content, "platform": platform})
            if response.status_code == 200:
                generated_post = response.json().get("response", "No response")
                st.success("Post generated!")
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            
    else:
        st.warning("Please enter a question before clicking 'Get Answer'.")
    
    
    # Display the generated post
    st.text_area("Generated Post:", value=generated_post, height=200, key="output_area")
    
#     # Button to copy the generated post
#     st.button("Copy to Clipboard", on_click=st.experimental_set_query_params, args=(('text', generated_post),))

# # Instruction for the copy functionality (as Streamlit currently has no built-in clipboard copy)
# st.info("To copy the generated post, use the copy button or manually copy the content from the output area.")
