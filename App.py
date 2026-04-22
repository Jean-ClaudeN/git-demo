import streamlit as st

st.set_page_config(page_title="AI Strategy Navigator", layout="centered")

st.title("AI Strategy Navigator")
st.caption("Interactive support for school leaders making AI decisions")

role = st.selectbox(
    "Choose a role",
    ["K-12 Special Education Coordinator", "Principal", "District Administrator"]
)

scenario = st.text_area(
    "Enter a real scenario",
    "A student with an IEP used AI to generate a writing assignment."
)

if st.button("Analyze Scenario"):
    st.success("Scenario analyzed")

    st.subheader("Situation Summary")
    st.write(f"**Role:** {role}")
    st.write(f"**Scenario:** {scenario}")

    st.subheader("Key Tensions")
    st.markdown("""
    - Accessibility vs academic fairness  
    - Support vs skill replacement  
    - Individual accommodation vs system consistency  
    """)

    st.subheader("Decision Questions")
    st.markdown("""
    - What is the learning objective of this assignment?  
    - Does AI support the task or replace the skill being assessed?  
    - Is this use aligned with student accommodations or school expectations?  
    - Would this decision remain fair if applied consistently?  
    """)

    st.subheader("Guardrails")
    st.markdown("""
    - Allow AI when it supports access to learning  
    - Do not allow AI when it replaces the core skill being measured  
    - Review decisions in context, not as one-size-fits-all rules  
    """)

    st.subheader("Recommended Next Step")
    st.info("Clarify with the teacher what skill the assignment is actually assessing.")

    st.subheader("Why this matters")
    st.write(
        "This tool does not make the decision for the administrator. "
        "It structures the thinking needed to make a responsible one."
    )
