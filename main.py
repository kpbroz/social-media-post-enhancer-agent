from typing import List, Sequence


from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

from chains import generate_chain, reflection_chain, formater_chain

REFLECT = "reflect"
GENERATE = "generate"
FORMATER = "formater"


def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})


def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflection_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

def formater_node(messages: Sequence[BaseMessage]) -> str:
    print(type(messages), len(messages))
    res = messages[-1]
    return formater_chain.invoke({"messages": HumanMessage(content=res)})

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


if __name__ == "__main__":
    print("Hello bvc!")
    post_content = input("Please enter the content and context of the social media post you want generate: ")
    social_media = input("Enter the social media platform: ")
    inputs = HumanMessage(content=post_content)
    
    inputs = HumanMessage(content=f"""{inputs}""")
    response = graph.invoke(inputs)
    print(response)

