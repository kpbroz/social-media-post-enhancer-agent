from typing import List, Sequence


from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import generate_chain, reflection_chain, formater_chain

REFLECT = "reflect"
GENERATE = "generate"
FORMATER = "formater"
MEDIA = "Facebook"


def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflection_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

def formater_node(messages: Sequence[BaseMessage]) -> str:
    res_content = messages[-1].content  # Extract the content of the last message
    return formater_chain.invoke(input = {"post_content": {res_content}, "social_media": {MEDIA}})


builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)
builder.add_node(FORMATER, formater_node)
builder.set_entry_point(GENERATE)

def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return FORMATER
    
    return REFLECT


builder.add_conditional_edges(GENERATE, should_continue)
builder.add_edge(REFLECT, GENERATE)
builder.add_edge(FORMATER, END)
graph = builder.compile()

graph.get_graph().draw_mermaid_png(output_file_path="graph.png")


def get_post_content(post_content, media):
    print("Hello bvc!")
    # post_content = input("Please enter the content and context of the social media post you want generate: ")
    # MEDIA = input("Enter the social media platform: ")
    # inputs = HumanMessage(content=post_content)
    MEDIA = media
    
    inputs = HumanMessage(content=f"""{post_content}""")
    response = graph.invoke(inputs)
    return response[-1].content

