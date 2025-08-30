__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerpApiGoogleSearchTool
import os
import streamlit as st

os.environ["SERPAPI_API_KEY"] = st.secrets.get("serpapi_key",'')
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from crewai import LLM
import json

# Gemini LLM setup (replace with your API key)
import streamlit as st
GEMINI_API_KEY = st.secrets.get('gemini_api_key','')

service_account_info = st.secrets['gcp']['service_account']

vertex_ai_json = json.dumps(dict(service_account_info))

os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = "True"
genai.configure(api_key=GEMINI_API_KEY)

gemini_llm = LLM(
    model='vertex_ai/gemini-2.5-pro',
    api_key=GEMINI_API_KEY,
    temperature=0.0 , # Lower temperature for more consistent results.
    vertex_credentials=vertex_ai_json
)

serp_api_tool = SerpApiGoogleSearchTool()

@CrewBase
class CurriculumPlannerCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    @agent
    def orchestrator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator'],
            verbose=True,
            llm=gemini_llm
        )
    
    @agent
    def curriculum_identifier_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['curriculum_identifier'],
            verbose=True,
            llm=gemini_llm,
            tools=[serp_api_tool]
        )
    
    @agent
    def curriculum_personalizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['curriculum_personalizer'],
            verbose=True,
            llm=gemini_llm
        )

    @agent
    def curriculum_communicator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['curriculum_communicator'],
            verbose=True,
            llm=gemini_llm
        )

    @task
    def identify_curriculum_structure(self) -> Task:
        return Task(
            config=self.tasks_config['curriculum_structure'],
            agent=self.curriculum_identifier_agent(),
        )
    
    @task
    def personalize_curriculum(self) -> Task:
        return Task(
            config=self.tasks_config['curriculum_personalization'],
            agent=self.curriculum_personalizer_agent(),
        )
    
    @task
    def communicate_curriculum(self) -> Task:
        return Task(
            config=self.tasks_config['curriculum_communication'],
            agent=self.curriculum_communicator_agent(),
        )

    @task
    def finalize_curriculum(self) -> Task:
        return Task(
            config=self.tasks_config['curriculum_finalization'],
            agent=self.orchestrator_agent(),
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Curriculum Planning Crew"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )