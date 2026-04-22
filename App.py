import streamlit as st

st.set_page_config(
    page_title="AI Strategy Navigator",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# Scenario library
# -----------------------------
SCENARIOS = {
    "Student used AI for essay writing": {
        "role": "Dean of a Professional School",
        "category": "Academic Integrity",
        "risk": "High",
        "scenario": "A graduate student in a professional program used generative AI to draft a substantial portion of a take-home ethics essay.",
        "tensions": [
            "Academic integrity vs legitimate AI assistance",
            "Skill development vs task completion",
            "Consistency of enforcement vs case-by-case judgment",
            "Professional standards vs evolving technology norms"
        ],
        "questions": [
            "What was the learning objective of the essay?",
            "Was the assignment assessing original reasoning, writing skill, or content knowledge?",
            "Did AI support brainstorming, or replace the student's analytical work?",
            "Was AI use disclosed?",
            "Would the same response be fair and consistent across similar cases?"
        ],
        "guardrails": [
            "Allow AI for brainstorming, outlining, or feedback when disclosed",
            "Do not allow AI to replace the core intellectual work being assessed",
            "Require transparency when AI meaningfully contributed to the assignment",
            "Use sanctions and coaching proportionate to the level of replacement"
        ],
        "next_step": "Meet with faculty to clarify the assignment’s core learning objective and compare the submitted work against that objective before determining a response."
    },
    "AI used in IEP accommodations": {
        "role": "Special Education Coordinator",
        "category": "Accessibility",
        "risk": "Medium",
        "scenario": "A student with documented accommodations used AI to generate written responses in a class where written communication is part of the grade.",
        "tensions": [
            "Accessibility vs unfair advantage",
            "Accommodation vs skill substitution",
            "Individual support vs consistency across students",
            "Inclusion vs validity of assessment"
        ],
        "questions": [
            "What skill is actually being assessed?",
            "Does AI provide access, or does it replace the assessed skill?",
            "Is this aligned with the student's formal accommodations?",
            "Are there alternative supports that preserve the learning objective?",
            "How would this be explained to instructors and peers as fair?"
        ],
        "guardrails": [
            "Permit AI when it removes barriers without replacing the core skill",
            "Review accommodation alignment before allowing generative output",
            "Document rationale for exceptions or supports",
            "Revisit the assessment design if accessibility and validity are in conflict"
        ],
        "next_step": "Consult the instructor and accommodation documentation to determine whether AI use preserved access or replaced the target skill."
    },
    "Teacher uses AI to create test questions": {
        "role": "Principal",
        "category": "Assessment",
        "risk": "Medium",
        "scenario": "A faculty member uses AI to generate quiz questions and answer keys for a core course.",
        "tensions": [
            "Efficiency vs quality control",
            "Innovation vs reliability",
            "Teacher autonomy vs institutional standards",
            "Speed vs accuracy and bias review"
        ],
        "questions": [
            "Were the questions reviewed for alignment with course outcomes?",
            "Did the teacher validate accuracy and difficulty level?",
            "Could biased or incorrect questions disadvantage students?",
            "Does the institution have standards for AI-assisted assessment design?"
        ],
        "guardrails": [
            "Allow AI-assisted drafting only with human review",
            "Require alignment checks to learning outcomes",
            "Prohibit unreviewed AI-generated assessment content",
            "Build light documentation into assessment workflows"
        ],
        "next_step": "Create a review checklist for any AI-generated test content before it reaches students."
    },
    "Group project with AI involvement": {
        "role": "Program Director",
        "category": "Equity",
        "risk": "Medium",
        "scenario": "Some students in a group project used AI heavily for ideation and drafting, while others did not, leading to concerns about fairness and contribution.",
        "tensions": [
            "Innovation vs equal participation",
            "Efficiency vs authentic collaboration",
            "Shared output vs individual accountability",
            "Access to tools vs fairness in evaluation"
        ],
        "questions": [
            "What portion of the project was expected to reflect student-generated work?",
            "Were expectations about AI use clearly communicated?",
            "How can contribution be assessed fairly within the group?",
            "Does AI use mask unequal effort?"
        ],
        "guardrails": [
            "Require disclosure of AI use in collaborative work",
            "Separate evaluation of product quality from individual contribution",
            "Use reflective statements to document process",
            "Clarify acceptable AI use before the assignment begins"
        ],
        "next_step": "Add an individual reflection or contribution log so AI use does not hide unequal participation."
    }
}

# -----------------------------
# Helper
# -----------------------------
def render_analysis(data, selected_values):
    st.subheader("Situation Summary")
    st.markdown(f"**Role Context:** {data['role']}")
    st.markdown(f"**Focus Area:** {selected_values['category']}")
    st.markdown(f"**Risk Level:** {selected_values['risk']}")
    st.info(data["scenario"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Core Tensions")
        for item in data["tensions"]:
            st.markdown(f"- {item}")

        st.subheader("Decision Questions")
        for item in data["questions"]:
            st.markdown(f"- {item}")

    with col2:
        st.subheader("Adaptive Guardrails")
        for item in data["guardrails"]:
            st.markdown(f"- {item}")

        st.subheader("Recommended Next Step")
        st.success(data["next_step"])

    st.subheader("Responsible AI Position")
    st.warning(
        "This tool does not make the decision for the administrator. "
        "It structures judgment, surfaces risks, and helps leaders apply context-aware guardrails."
    )

    st.subheader("High-Level Output")
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Decisions Clarified", "1")
    metric2.metric("Risks Identified", str(len(data["tensions"])))
    metric3.metric("Guardrails Suggested", str(len(data["guardrails"])))

    with st.expander("Defensible Dean-Level Framing"):
        st.write(
            "A dean can defend this output because it does not outsource responsibility. "
            "It makes the underlying educational values explicit: learning objective, fairness, "
            "professional standards, transparency, and consistency."
        )

# -----------------------------
# UI
# -----------------------------
st.title("🧠 AI Strategy Navigator")
st.caption("Practical AI decisions, grounded in school context.")

st.markdown("## Responsible AI decisions, made in real time")
st.write(
    "Helping administrators navigate complex AI use cases with clarity, "
    "instead of relying on rigid, one-size-fits-all policies."
)

st.divider()

left, right = st.columns([1, 2])

with left:
    st.markdown("### Quick Filters")
    role = st.selectbox(
        "Role",
        [
            "Dean of a Professional School",
            "Principal",
            "Special Education Coordinator",
            "Program Director"
        ]
    )
    category = st.selectbox(
        "Primary Concern",
        ["Academic Integrity", "Accessibility", "Assessment", "Equity"]
    )
    risk = st.select_slider("Risk Level", options=["Low", "Medium", "High"], value="High")

    st.markdown("### Quick Starts")
    quick_start = st.radio(
        "Choose a real case",
        list(SCENARIOS.keys())
    )

with right:
    st.markdown("### Describe the situation in your school")
    user_scenario = st.text_area(
        "Scenario",
        value=SCENARIOS[quick_start]["scenario"],
        height=140
    )

    analyze = st.button("Analyze Scenario", use_container_width=True)

if analyze:
    selected = SCENARIOS[quick_start].copy()
    selected["scenario"] = user_scenario

    # Override displayed values from user filters for a more interactive feel
    render_analysis(selected, {
        "category": category,
        "risk": risk
    })

st.divider()

st.markdown("### Featured Scenarios")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.info("Student uses AI to write an essay")
with c2:
    st.info("AI used in IEP accommodations")
with c3:
    st.info("Teacher uses AI for grading or test creation")
with c4:
    st.info("Group project with AI involvement")

st.markdown("### Works Across")
a, b, c, d = st.columns(4)
a.success("K–12 Schools")
b.success("Higher Education")
c.success("Special Education")
d.success("Professional Programs")

st.divider()
st.markdown("### Responsible Use")
st.write(
    "This tool does not generate policy automatically or make decisions for administrators. "
    "It helps leaders clarify context, surface tensions, and apply adaptable guardrails."
)
