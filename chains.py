import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import  AzureChatOpenAI

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