import streamlit as st
from crew_orchestrator import CurriculumPlannerCrew
import json

st.set_page_config(page_title="Curriculum Planner", page_icon="📚", layout="wide", initial_sidebar_state="collapsed")
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.title("📚 Curriculum Planning Assistant")
st.write("Welcome! Enter your curriculum planning requirements below. Our AI system will help create a personalized curriculum plan based on your needs.")

with st.form("curriculum_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        subject = st.selectbox("Subject", ["Mathematics", "Science", "History", "Computer Science"])
        duration = st.text_input("Duration", "8 weeks")
    with col2:
        grade = st.selectbox("Grade Level", ["Grade 3", "Middle School", "High School", "Undergraduate"])
    with col3:
        styles = st.multiselect("Preferred Teaching Style", 
                              ["Interactive", "Lecture-based", "Project-based"], 
                              default=["Interactive"])
    
    goals = st.text_area("Learning Goals", placeholder="e.g., Master basic algebra concepts")
    submit = st.form_submit_button("Generate Curriculum")

if submit and subject and grade:
    user_input = {
        "subject": subject,
        "grade_level": grade,
        "duration": duration,
        "teaching_styles": styles,
        "learning_goals": goals.strip()
    }
    with st.spinner("Generating your personalized curriculum plan..."):
        crew_instance = CurriculumPlannerCrew()
        result = crew_instance.crew().kickoff(user_input)
    st.success("Curriculum Plan Generated!")
    st.markdown("### Your Personalized Curriculum Plan")
    st.markdown(result, unsafe_allow_html=True)
else:
    st.info("Please fill in the required fields to generate a curriculum plan.")