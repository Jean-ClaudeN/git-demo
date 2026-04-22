import streamlit as st

st.set_page_config(
    page_title="AI Strategy Navigator",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #F8FAFC;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
div[data-testid="stTextArea"] textarea {
    border-radius: 12px;
}
div.stButton > button {
    background: linear-gradient(90deg, #1D4ED8, #F59E0B);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 0.7rem 1.2rem;
    width: 100%;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 16px;
}
.hero {
    background: linear-gradient(135deg, #1D4ED8, #F59E0B);
    padding: 28px;
    border-radius: 20px;
    color: white;
    margin-bottom: 24px;
}
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 600;
    margin-right: 8px;
    margin-bottom: 8px;
}
.high { background-color: #FEE2E2; color: #B91C1C; }
.medium { background-color: #FEF3C7; color: #92400E; }
.low { background-color: #DCFCE7; color: #166534; }
</style>
""", unsafe_allow_html=True)

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
        "next_step": "Meet with faculty to clarify the assignment’s core learning objective before determining a response."
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

def risk_badge(risk):
    risk_class = risk.lower()
    return f'<span class="badge {risk_class}">{risk} Risk</span>'

def render_card(title, items):
    html = f'<div class="card"><h3>{title}</h3>'
    if isinstance(items, list):
        html += "<ul>"
        for item in items:
            html += f"<li>{item}</li>"
        html += "</ul>"
    else:
        html += f"<p>{items}</p>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧠 AI Strategy Navigator</h1>
    <p style="font-size:18px; margin-top:8px;">
        Responsible AI decisions, made in real time.
    </p>
    <p style="font-size:15px;">
        Helping administrators navigate complex AI use cases with clarity, not rigid policies.
    </p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 2])

with left:
    st.subheader("Quick Filters")
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

    risk = st.select_slider(
        "Risk Level",
        options=["Low", "Medium", "High"],
        value="High"
    )

    st.subheader("Quick Start Scenarios")
    quick_start = st.radio("Choose a case", list(SCENARIOS.keys()))

with right:
    st.subheader("Describe the situation in your school")
    user_scenario = st.text_area(
        "Scenario",
        value=SCENARIOS[quick_start]["scenario"],
        height=140
    )

    analyze = st.button("Analyze Scenario")

if analyze:
    selected = SCENARIOS[quick_start]

    st.markdown("## Analysis")
    st.markdown(risk_badge(risk), unsafe_allow_html=True)

    render_card("Situation Summary", f"""
    <strong>Role Context:</strong> {role}<br>
    <strong>Focus Area:</strong> {category}<br><br>
    {user_scenario}
    """)

    col1, col2 = st.columns(2)

    with col1:
        render_card("Core Tensions", selected["tensions"])
        render_card("Decision Questions", selected["questions"])

    with col2:
        render_card("Adaptive Guardrails", selected["guardrails"])
        render_card("Recommended Next Step", selected["next_step"])

    st.warning(
        "This tool does not make the decision for the administrator. "
        "It structures judgment, surfaces risks, and helps leaders apply context-aware guardrails."
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Decisions Clarified", "1")
    m2.metric("Risks Identified", str(len(selected["tensions"])))
    m3.metric("Guardrails Suggested", str(len(selected["guardrails"])))

    with st.expander("Why this is defensible for a dean"):
        st.write(
            "This output is defensible because it does not outsource responsibility. "
            "It makes the learning objective, fairness concerns, transparency expectations, "
            "and professional standards visible before action is taken."
        )

st.divider()

st.subheader("Works Across")
a, b, c, d = st.columns(4)
a.success("K–12 Schools")
b.success("Higher Education")
c.success("Special Education")
d.success("Professional Programs")

st.subheader("Responsible Use")
st.write(
    "This tool does not generate policy automatically or make decisions for administrators. "
    "It helps leaders clarify context, surface tensions, and apply adaptable guardrails."
)
