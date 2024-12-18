from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
import os
from pydantic import BaseModel, ValidationError
from langchain.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from sklearn.svm import SVC
from sklearn.metrics.pairwise import cosine_similarity

system_prompt = """
    You are a friendly and professional receptionist for a company that helps Indian students or individuals gain admission to universities and colleges abroad. Your main goal is to gather essential information from the user in a conversational and supportive manner. Your role involves making the user feel comfortable while asking for specific details to assist in their application process.

	Begin the conversation by welcoming the user warmly, introducing your purpose, and letting them know that a few questions will help you find the best options for them. Then, proceed to collect the following information:

	1.	Undergraduate Degree: Ask about the type of degree they completed (e.g., B.Tech, B.Sc, B.Com, etc.).
	2.	Specific Program: Inquire about the specific major or program they studied (e.g., Computer Science, Mechanical Engineering, Business).
	3.	College/University Attended: Ask for the name of the institution where they completed their undergraduate degree.
	4.	Total CGPA/Percentage: Request their final CGPA or percentage score from their undergraduate degree.
	5.	Backlogs in UG: Ask if they had any backlogs during their undergraduate studies, reassuring them that this is only for a complete understanding of their profile.
	6.	Work Experience (if any): Inquire if they have any work experience, including the total years.

    Start the conversation with a warm greeting and an offer to assist. You can ask the academic information in one go and keep 1-2 word when asking each information. After gathering each piece of information, thank the user and provide brief supportive feedback before moving to the next question. If the user seems unsure, respond empathetically and help clarify.
    Maintain a welcoming and positive tone throughout the conversation to make the user feel comfortable and supported. At the end, confirm that you’ve received all the necessary information and assure them that you’ll use it to find the best opportunities for studying abroad.

    You can gather all acedemic information in 1 go.
    After gathering all piece of information, immediately store the responses using the availabe tool.
"""


class LangState(BaseModel):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(LangState)

@tool
def update_user(degree: str, spec: str, college: str, percent: str, backlogs: str, total_exp: str) -> bool:
    """This is used for storing user information"""
    try:
        print(f'degree: {degree}, spec: {spec}, college: {college}, percent: {percent}, backlogs: {backlogs}, total_exp: {total_exp}')
    except Exception as error:
        print(error)

tools = [update_user]
llm = ChatOpenAI(api_key=os.getenv("OPEN_AI_API_KEY"), model='gpt-3.5-turbo').bind_tools(tools)


def chatbot(state: LangState) -> LangState:
    return {
        'messages': [llm.invoke(state.messages)]
    }

graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")

tool_node =ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()

def stream_graph(user_input: str, system: bool = False):
    for event in graph.stream({"messages": [("system" if system else "user", user_input)]}):
        for value in event.values():
            value["messages"][-1].pretty_print()

stream_graph(system_prompt, True)

def start_chat():
    while True:
        try:
            user_input = input("user: ")
            if user_input.lower() in ['quit', 'exit', 'q']:
                print('Goodbye!')
                break

            stream_graph(user_input)
        except:
            stream_graph('START')

class CosineKernelSVM(SVC):
    def __init__(self, **kwargs):
        super().__init__(kernel='precomputed', **kwargs)
    
    def fit(self, X, y):
        # Precompute the cosine similarity matrix
        cosine_matrix = cosine_similarity(X)
        super().fit(cosine_matrix, y)

    def predict(self, X):
        cosine_matrix = cosine_similarity(X, self.support_vectors_)
        return super().predict(cosine_matrix)
    

from pandas import read_csv
import pandas as pd

last_univ = ''

def fill_na(univ):
    global last_univ
    if pd.isna(univ):
        return last_univ
    else:
        last_univ = univ
        return univ

def scrap_program_eligibility():
    df = read_csv('/Users/dev-01/dev/Projects/dash_rat/statics/Glovera - Template For 100x - Course Info.csv')
    
    df.drop(['Unnamed: 8', 'Unnamed: 13', 'Unnamed: 18', 'Unnamed: 24', 'Unnamed: 31', 'Unnamed: 39', 'Unnamed: 43'], axis=1, inplace=True)
    
    df['University '].fillna(method='ffill', inplace=True)
    df['College'].fillna(method='ffill', inplace=True)
    df['Location'].fillna(method='ffill', inplace=True)
    df['Public/Private'].fillna(method='ffill', inplace=True)
    df['Whats Special About this location'].fillna(method='ffill', inplace=True)
    df['Whats Special about this Univ/ College'].fillna(method='ffill', inplace=True)

    df.fillna("", inplace=True)
    programs = []
    for _, row in df.iterrows():
        program = {
            'name': row['Program Name'],
            'rank': row['Ranking'],
            'eligibility': {
                'ug_bacground': row['UG Background'],
                'min_gpa_perc': row['Minimum GPA or %'],
                'backlogs': row['Backlogs'],
                'work_exp': row['Work Experience'],
                'three_year_undergrad': row['Will allow 3 years undergrad candidates?'],
                'decision_factor': row['Decision Factor']
            }
        }

        programs.append(program)
    return programs

import random
import json
from openai import OpenAI

# user_eligibilty = ChatOpenAI(api_key=os.getenv("OPEN_AI_API_KEY"), model='gpt-3.5-turbo')
openai_client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

def create_cypher_query():
    programs = scrap_program_eligibility()
    programs_string = "\n".join([json.dumps(program, indent=4) for program in programs])
    prompt = f"""
        Given the following programs, along with their eligibility rules and ranking, please generate all Cypher code that creates nodes and relationships to represent this rule in a Neo4j graph database. Use nodes for programs, eligibility criterias, and represent conditional criteria with relationships.

        <programs>
        {programs_string}
        <programs>
    """

    # Call the LLM API
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Cypher expert helping with Neo4j database structuring."},
            {"role": "user", "content": prompt}
        ]
    ).choices[0].message.content

    print(response)
    # students = []
    # for _ in range(num_students):
    #     student = {
    #         "degree": random.choices(["B.Tech", 'M.Tech', "B.Com", "BA", "BBA", "MBA", "MBBS"]),
    #         "GPA": round(random.uniform(5.0, 9.0), 1),
    #         "Backlogs": random.randint(0, 5),
    #         "Work Experience": random.randint(0, 5),
    #         "3 year degree": random.choices([True, False])
    #     }
        
    #     # Determine eligibility for each program
    #     response = openai_client.chat.completions.create(
    #         model='gpt-3.5-turbo',
    #         messages=[{'role': 'user', 'content': prompt(student)}]
    #     ).choices[0].message.content
    #     print(response)
    #     students.append(student)
    
    # return students


create_cypher_query()