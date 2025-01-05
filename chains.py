import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_openai import  AzureChatOpenAI
from langchain.schema.output_parser import StrOutputParser

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
OPENAI_AZURE_ENDPOINT = os.getenv("OPENAI_AZURE_ENDPOINT")


generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a social media influencer friendly assistant helping to writing impressive social media posts"
            "Generate the best possible social media post on user's requested topic and context"
            "If the user provides critique or suggestions, respond with a revised version implementing all the feedback provided on your previous generated posts."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a social media content grader and improviser, generate critique and recommendations for the user's tweet"
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# formatter_prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You a social media content extractor"
#             "When a user provides you the paragraph which includes content and other suggestion, precisely extract and return the post content.",    
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

formater_prompt = """You are given unformatted content for the social media post. Format the content according to {social_media} post content.
content: {post_content}

Return ONLY the post content format according to social media mentioned.
"""

formater_prompt = PromptTemplate(input_variables=["social_media", "post_content"], template=formater_prompt)


llm = AzureChatOpenAI(temperature=0, model=OPENAI_MODEL, api_key=AZURE_OPENAI_API_KEY, api_version=OPENAI_API_VERSION, azure_endpoint=OPENAI_AZURE_ENDPOINT)
generate_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm
formater_chain = formater_prompt | llm | StrOutputParser()