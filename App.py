import streamlit as st

st.set_page_config(page_title="AI Governance Simulator", layout="centered")

st.title("🎓 AI Governance Simulator")
st.caption("Decision support for academic leaders navigating AI use")

# Role selection
role = st.selectbox(
    "Select your role",
    ["Dean (Professional School)", "Program Director", "Academic Integrity Officer"]
)

# Scenario presets
scenario_option = st.selectbox(
    "Choose a scenario or write your own",
    [
        "Graduate student used AI to generate a policy analysis assignment",
        "Student used AI for a take-home exam",
        "Student used AI to assist with research synthesis",
        "Custom scenario"
    ]
)

# Custom input
custom_scenario = ""
if scenario_option == "Custom scenario":
    custom_scenario = st.text_area("Enter your scenario")

scenario = custom_scenario if custom_scenario else scenario_option

if st.button("Run Simulation"):

    st.success("Simulation Active")

    # Tabs for high-caliber feel
    tab1, tab2, tab3, tab4 = st.tabs([
        "Situation", "Tensions", "Decision Framework", "Action Plan"
    ])

    with tab1:
        st.subheader("📍 Situation Summary")
        st.write(f"**Role:** {role}")
        st.write(f"**Scenario:** {scenario}")

    with tab2:
        st.subheader("⚖️ Core Tensions")
        st.markdown("""
        - Academic integrity vs legitimate AI support  
        - Skill development vs task completion  
        - Consistency across students vs individual context  
        - Institutional standards vs evolving technology  
        """)

    with tab3:
        st.subheader("🧠 Decision Framework")

        st.markdown("### Key Questions")
        st.markdown("""
        - What is the **learning objective** of this assignment?  
        - Does AI use **support or replace** that objective?  
        - What level of AI use is **acceptable in this program**?  
        - Would this decision be **consistent across all students**?  
        """)

        st.markdown("### Guardrails")
        st.markdown("""
        - Allow AI when it supports analysis and understanding  
        - Do not allow AI when it replaces core assessment skills  
        - Evaluate based on **learning goals, not tools used**  
        """)

    with tab4:
        st.subheader("🚀 Recommended Action")

        st.markdown("""
        - Clarify assignment expectations with faculty  
        - Determine if AI use replaced core competencies  
        - Provide student guidance rather than immediate punishment  
        - Update program-level AI guidelines if needed  
        """)

        st.info("This tool does not make decisions — it structures professional judgment.")
