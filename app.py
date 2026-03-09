import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import date, datetime

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="AI Study Planner")

st.title("📚 AI Study Planner")
st.write("Generate a smart study schedule for your exams.")

# Inputs
exam_date = st.date_input("Select Exam Date")

subjects = st.text_area(
    "Enter Subjects (comma separated)",
    placeholder="math, physics, chemistry"
)

hours = st.number_input(
    "Study hours available per day",
    min_value=1,
    max_value=12,
    value=4
)

if st.button("Generate Study Plan"):

    today = date.today()

    if isinstance(exam_date, datetime):
        exam_date = exam_date.date()

    days_left = (exam_date - today).days

    if days_left <= 0:
        st.error("Exam date must be in the future")
    else:

        st.info(f"Days remaining: {days_left}")

        prompt = f"""
Create a structured study plan.

Exam in {days_left} days
Subjects: {subjects}
Study hours per day: {hours}

Return the plan EXACTLY in this format:

SUBJECT PRIORITY
(list subjects from hardest to easiest)

DAILY STUDY SCHEDULE
(day-by-day plan)

WEEKLY REVISION STRATEGY
(how revision happens each week)

FINAL REVISION PLAN
(strategy for the final week before exam)
"""

        with st.spinner("Generating your study plan..."):

            try:

                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert academic study planner."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=500
                )

                plan = response.choices[0].message.content

                st.subheader("📅 Your AI Study Plan")
                st.markdown(plan)

            except Exception as e:
                st.error(f"Error: {e}")