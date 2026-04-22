"""
Correlation vs Causation — Interactive Teaching Tool
Editorial-style design inspired by data journalism (NYT Upshot, Pudding, FiveThirtyEight).
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from scipy import stats

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Correlation vs Causation",
    page_icon="◐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# CUSTOM CSS — Editorial / data journalism aesthetic
# ==========================================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,800;1,9..144,400&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
    color: #1a1a1a;
}

.stApp {
    background: #faf8f3;
    background-image:
        radial-gradient(at 20% 10%, rgba(212, 175, 55, 0.04) 0px, transparent 50%),
        radial-gradient(at 80% 90%, rgba(180, 50, 50, 0.03) 0px, transparent 50%);
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px;
}

h1 {
    font-family: 'Fraunces', Georgia, serif !important;
    font-weight: 800 !important;
    font-size: 3.2rem !important;
    line-height: 1.05 !important;
    letter-spacing: -0.03em !important;
    color: #0a0a0a !important;
    margin-bottom: 0.3rem !important;
}

h2 {
    font-family: 'Fraunces', Georgia, serif !important;
    font-weight: 600 !important;
    font-size: 2rem !important;
    letter-spacing: -0.02em !important;
    color: #1a1a1a !important;
    margin-top: 1rem !important;
}

h3 {
    font-family: 'Fraunces', Georgia, serif !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
}

.dek {
    font-family: 'Fraunces', Georgia, serif;
    font-style: italic;
    font-size: 1.25rem;
    color: #555;
    line-height: 1.5;
    max-width: 720px;
    margin: 0 0 2rem 0;
    font-weight: 400;
}

.byline {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8b0000;
    font-weight: 500;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #8b0000;
    padding-bottom: 0.3rem;
    display: inline-block;
}

.drop-cap::first-letter {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 4.5rem;
    font-weight: 800;
    float: left;
    line-height: 0.85;
    margin: 0.3rem 0.6rem 0 0;
    color: #8b0000;
}

.body-text {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.05rem;
    line-height: 1.65;
    color: #2a2a2a;
    max-width: 680px;
}

.pull-quote {
    font-family: 'Fraunces', Georgia, serif;
    font-style: italic;
    font-size: 1.4rem;
    line-height: 1.4;
    color: #1a1a1a;
    border-left: 4px solid #8b0000;
    padding: 0.5rem 0 0.5rem 1.5rem;
    margin: 1.5rem 0;
    max-width: 640px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid #1a1a1a;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    padding: 1rem 1.5rem !important;
    background: transparent !important;
    color: #555 !important;
    border-bottom: 3px solid transparent !important;
    margin-right: 0 !important;
    transition: all 0.2s ease;
}

.stTabs [aria-selected="true"] {
    color: #8b0000 !important;
    border-bottom: 3px solid #8b0000 !important;
    background: transparent !important;
}

.stButton > button {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    background: #1a1a1a !important;
    color: #faf8f3 !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0.75rem 1.5rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #8b0000 !important;
    color: #faf8f3 !important;
    transform: translateY(-1px);
}

.stSlider label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: #1a1a1a !important;
}

.stSelectbox label, .stNumberInput label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.stCheckbox label, .stToggle label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
}

div[data-testid="stAlert"] {
    border-radius: 0 !important;
    border-left-width: 4px !important;
    border-top: none !important;
    border-right: none !important;
    border-bottom: none !important;
    font-family: 'Fraunces', Georgia, serif !important;
    font-size: 1rem !important;
    background: rgba(255, 255, 255, 0.6) !important;
}

.streamlit-expanderHeader {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    border-radius: 0 !important;
    border-left: 3px solid #d4af37 !important;
}

.stMarkdown table {
    font-family: 'Inter', sans-serif;
    font-size: 0.92rem;
    border-collapse: collapse;
    width: 100%;
    background: rgba(255, 255, 255, 0.5);
}

.stMarkdown th {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: #1a1a1a !important;
    color: #faf8f3 !important;
    padding: 0.8rem !important;
    text-align: left !important;
}

.stMarkdown td {
    padding: 0.8rem !important;
    border-bottom: 1px solid #e0dcd0 !important;
}

.stMarkdown tr:hover td {
    background: rgba(139, 0, 0, 0.03) !important;
}

code {
    font-family: 'JetBrains Mono', monospace !important;
    background: #1a1a1a !important;
    color: #d4af37 !important;
    padding: 0.15rem 0.4rem !important;
    border-radius: 2px !important;
    font-size: 0.88em !important;
}

hr {
    border: none !important;
    border-top: 1px solid #1a1a1a !important;
    margin: 2.5rem 0 !important;
    opacity: 0.15;
}

.section-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: #8b0000;
    font-weight: 500;
    margin-bottom: 0.5rem;
    display: block;
}

.caption {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    color: #666;
    font-style: italic;
    border-top: 1px solid #d0ccbf;
    padding-top: 0.5rem;
    margin-top: 0.5rem;
}

.big-stat {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 3.5rem;
    font-weight: 800;
    line-height: 1;
    color: #8b0000;
    letter-spacing: -0.04em;
}

.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #666;
    margin-top: 0.3rem;
}

.stTextArea textarea {
    font-family: 'Fraunces', Georgia, serif !important;
    font-size: 1rem !important;
    border-radius: 0 !important;
    border: 1px solid #d0ccbf !important;
    background: rgba(255, 255, 255, 0.6) !important;
}

.stTextArea textarea:focus {
    border-color: #8b0000 !important;
    box-shadow: none !important;
}

.stTextArea label {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }

.js-plotly-plot { margin: 0 !important; }

[data-testid="column"] { padding: 0 0.8rem; }

</style>
""",
    unsafe_allow_html=True,
)

EDITORIAL_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", size=12, color="#2a2a2a"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,0.4)",
    xaxis=dict(
        gridcolor="rgba(26,26,26,0.08)",
        linecolor="#1a1a1a", linewidth=1, ticks="outside",
        tickfont=dict(family="JetBrains Mono, monospace", size=11),
        title_font=dict(family="Inter, sans-serif", size=13, color="#1a1a1a"),
    ),
    yaxis=dict(
        gridcolor="rgba(26,26,26,0.08)",
        linecolor="#1a1a1a", linewidth=1, ticks="outside",
        tickfont=dict(family="JetBrains Mono, monospace", size=11),
        title_font=dict(family="Inter, sans-serif", size=13, color="#1a1a1a"),
    ),
    margin=dict(l=60, r=20, t=50, b=60),
    title_font=dict(family="Fraunces, Georgia, serif", size=16, color="#1a1a1a"),
)

# ==========================================
# HEADER — Editorial masthead
# ==========================================
st.markdown('<div class="byline">Issue 01 · Statistical Reasoning · Spring 2026</div>', unsafe_allow_html=True)
st.markdown("# Correlation <em style='font-family:Fraunces;font-weight:400;font-style:italic;color:#8b0000;'>is not</em> Causation", unsafe_allow_html=True)
st.markdown(
    '<p class="dek">An interactive investigation into why two variables moving together '
    'tells us almost nothing about whether one causes the other — and what it takes, '
    'methodologically, to make the leap.</p>',
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(
    ["◐  THE SIMULATOR", "◉  FROM THE ARCHIVES", "✎  YOUR INVESTIGATION"]
)

# ==========================================
# TAB 1 — Confounder Simulator
# ==========================================
with tab1:
    st.markdown('<span class="section-num">§ 01 — LIVE DEMONSTRATION</span>', unsafe_allow_html=True)
    st.markdown("## Manufacture a spurious correlation")
    st.markdown(
        '<p class="body-text drop-cap">Two variables — <strong>ice cream sales</strong> and '
        '<strong>drowning incidents</strong> — have no direct causal relationship. '
        'Yet they move together, season after season, year after year. The reason is '
        'simple and hidden: both are driven by a third variable you cannot see in the '
        'data unless you think to look for it. The controls below let you play the '
        'role of nature, tuning how strongly <em>heat</em> drives each outcome.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    col_controls, col_plot = st.columns([1, 2], gap="large")

    with col_controls:
        st.markdown('<span class="section-num">CONTROLS</span>', unsafe_allow_html=True)
        n_points = st.slider("Observations (days)", 30, 500, 180, step=10)
        heat_to_icecream = st.slider(
            "Heat → Ice cream sales", 0.0, 1.0, 0.80, step=0.05,
        )
        heat_to_drowning = st.slider(
            "Heat → Drowning incidents", 0.0, 1.0, 0.70, step=0.05,
        )
        noise = st.slider("Random noise", 0.0, 1.0, 0.25, step=0.05)
        seed = st.number_input("Random seed", value=42, step=1)

    rng = np.random.default_rng(int(seed))
    heat = rng.uniform(0, 1, n_points)
    ice_cream = heat_to_icecream * heat + noise * rng.normal(0, 0.3, n_points)
    drowning = heat_to_drowning * heat + noise * rng.normal(0, 0.3, n_points)

    ice_cream_sales = 100 + 400 * (ice_cream - ice_cream.min()) / (ice_cream.max() - ice_cream.min() + 1e-9)
    drowning_count = 20 * (drowning - drowning.min()) / (drowning.max() - drowning.min() + 1e-9)
    heat_f = 60 + 40 * heat

    df = pd.DataFrame({
        "Temperature (°F)": heat_f,
        "Ice cream sales ($)": ice_cream_sales,
        "Drownings": drowning_count,
    })

    r, p = stats.pearsonr(df["Ice cream sales ($)"], df["Drownings"])

    with col_plot:
        show_heat = st.checkbox("Reveal the confounder (color by temperature)", value=False)

        if show_heat:
            fig = px.scatter(
                df, x="Ice cream sales ($)", y="Drownings",
                color="Temperature (°F)",
                color_continuous_scale=[[0, "#1a4d6e"], [0.5, "#d4af37"], [1, "#8b0000"]],
                trendline="ols", trendline_color_override="#1a1a1a",
            )
        else:
            fig = px.scatter(
                df, x="Ice cream sales ($)", y="Drownings",
                trendline="ols", trendline_color_override="#8b0000",
                color_discrete_sequence=["#1a1a1a"],
            )

        fig.update_traces(marker=dict(size=7, opacity=0.65, line=dict(width=0.5, color="white")))
        fig.update_layout(**EDITORIAL_LAYOUT, height=440)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="big-stat">{r:.2f}</div>'
            f'<div class="stat-label">Pearson correlation coefficient</div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="big-stat">{p:.1e}</div>'
            f'<div class="stat-label">p-value</div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="big-stat">0</div>'
            f'<div class="stat-label">Actual causal arrows between X and Y</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    if abs(r) > 0.5 and not show_heat:
        st.markdown(
            f'<div class="pull-quote">"Strong link found between ice cream and drowning (r = {r:.2f}) — '
            f'researchers urge public caution."</div>'
            f'<p class="body-text" style="font-size:0.95rem;color:#666;">'
            f'— A plausible headline, and an entirely wrong one. Neither variable affects '
            f'the other. Toggle <em>Reveal the confounder</em> above.</p>',
            unsafe_allow_html=True,
        )
    elif show_heat:
        st.success(
            "**The confounder revealed.** The color gradient shows what the scatter "
            "plot alone cannot: high-temperature days (warm colors) cluster in the upper "
            "right, cool days (blue) in the lower left. Both variables respond to "
            "temperature independently. The apparent ice-cream-to-drowning relationship "
            "is spurious — a textbook confounding variable."
        )
    else:
        st.info(
            "Increase both *Heat →* sliders to watch the spurious correlation grow. "
            "Set them both to 0 and the correlation collapses, because heat is the "
            "only thing linking the two variables."
        )

    with st.expander("DISCUSSION PROMPTS FOR CLASS"):
        st.markdown(
            """
- **Mechanism.** If you set *both* heat-driver sliders to 0, what happens to the correlation? Why?
- **Detection.** A researcher sees only ice cream and drowning data — no temperature column. Can they detect the confounder from the data alone? What would they need?
- **Generalization.** Name a real pair of variables in your field that might be confounded by something you *cannot* directly measure. What would it take to convince you the relationship was causal?
            """
        )

# ==========================================
# TAB 2 — Real Examples (The Archives)
# ==========================================
with tab2:
    st.markdown('<span class="section-num">§ 02 — CASE FILES</span>', unsafe_allow_html=True)
    st.markdown("## Three correlations that fooled (almost) everyone")
    st.markdown(
        '<p class="body-text">Each of these patterns is real. Each looks compelling at first glance. '
        'And each dissolves the moment you identify what else is going on in the background.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    example = st.selectbox(
        "Select a case",
        [
            "CASE NO. 1 — Firefighters & fire damage",
            "CASE NO. 2 — Shoe size & reading ability (in children)",
            "CASE NO. 3 — Chocolate consumption & Nobel laureates",
        ],
    )

    rng2 = np.random.default_rng(7)

    if "CASE NO. 1" in example:
        size = rng2.uniform(1, 10, 60)
        firefighters = 2 * size + rng2.normal(0, 1, 60)
        damage = 50 * size + rng2.normal(0, 20, 60)
        data = pd.DataFrame({
            "Firefighters on scene": firefighters,
            "Damage ($ thousands)": damage,
            "Fire size (acres)": size,
        })
        x, y, conf = "Firefighters on scene", "Damage ($ thousands)", "Fire size (acres)"
        headline = "CITIES WITH MORE FIREFIGHTERS SUFFER WORSE FIRES"
        wrong_take = (
            "A budget-minded councilmember reading this correlation might propose "
            "cutting the fire department to reduce damage — an intervention that "
            "would kill people."
        )
        right_take = (
            "Larger fires cause *both* more damage and the dispatch of more firefighters. "
            "Fire size is the confounder. The correct causal diagram is: "
            "fire size → firefighters dispatched, and separately, fire size → damage. "
            "The two observed variables are correlated only through their common cause."
        )

    elif "CASE NO. 2" in example:
        age = rng2.uniform(5, 15, 80)
        shoe = 2 + 0.6 * age + rng2.normal(0, 0.5, 80)
        reading = 20 + 8 * age + rng2.normal(0, 6, 80)
        data = pd.DataFrame({
            "Shoe size": shoe,
            "Reading test score": reading,
            "Age (years)": age,
        })
        x, y, conf = "Shoe size", "Reading test score", "Age (years)"
        headline = "LARGER FEET LINKED TO SUPERIOR READING SKILLS"
        wrong_take = (
            "One might theorize that foot size boosts brain development, or that "
            "reading somehow promotes growth. Both are absurd — and yet the data "
            "shows a clear positive correlation."
        )
        right_take = (
            "Age drives both variables. Older children have bigger feet *and* "
            "more years of reading instruction. Within any single age group, "
            "the correlation vanishes."
        )

    else:
        gdp = rng2.uniform(5, 70, 25)
        chocolate = 2 + 0.15 * gdp + rng2.normal(0, 2, 25)
        nobels = np.clip(0.1 * gdp + rng2.normal(0, 3, 25), 0, None)
        data = pd.DataFrame({
            "Chocolate consumption (kg/person/yr)": chocolate,
            "Nobel laureates per 10M people": nobels,
            "GDP per capita ($k)": gdp,
        })
        x, y, conf = "Chocolate consumption (kg/person/yr)", "Nobel laureates per 10M people", "GDP per capita ($k)"
        headline = "CHOCOLATE CONSUMPTION PREDICTS NATIONAL INTELLIGENCE"
        wrong_take = (
            "Published in the New England Journal of Medicine as a tongue-in-cheek "
            "letter in 2012. Many readers, including some journalists, missed the joke "
            "entirely and ran with the causal claim."
        )
        right_take = (
            "Wealthier countries can afford chocolate imports *and* sustain the "
            "research infrastructure that produces Nobel laureates. GDP per capita "
            "is the common cause."
        )

    reveal = st.toggle("Reveal the confounder", value=False)

    r2, _ = stats.pearsonr(data[x], data[y])

    if reveal:
        fig2 = px.scatter(
            data, x=x, y=y, color=conf,
            color_continuous_scale=[[0, "#1a4d6e"], [0.5, "#d4af37"], [1, "#8b0000"]],
            trendline="ols", trendline_color_override="#1a1a1a",
        )
    else:
        fig2 = px.scatter(
            data, x=x, y=y,
            trendline="ols", trendline_color_override="#8b0000",
            color_discrete_sequence=["#1a1a1a"],
        )

    fig2.update_traces(marker=dict(size=9, opacity=0.7, line=dict(width=0.5, color="white")))
    fig2.update_layout(**EDITORIAL_LAYOUT, height=460)

    st.markdown(
        f'<div class="pull-quote" style="font-style:normal;font-weight:600;'
        f'text-transform:uppercase;letter-spacing:0.04em;font-size:1.1rem;'
        f'font-family:JetBrains Mono,monospace;border-left-color:#1a1a1a;">'
        f'{headline}</div>',
        unsafe_allow_html=True,
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown(
        f'<p class="caption">Fig. {example.split(" — ")[0].replace("CASE NO. ", "")}: '
        f'Observed correlation r = {r2:.3f}. '
        f'{"Points colored by " + conf + "." if reveal else "Confounder hidden."}</p>',
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if not reveal:
        st.error(f"**The naive reading —** {wrong_take}")
        st.markdown(
            '<p class="caption" style="text-align:center;">↑ '
            'Toggle <em>Reveal the confounder</em> above to see what is really going on. ↑</p>',
            unsafe_allow_html=True,
        )
    else:
        st.success(f"**What is really going on —** {right_take}")

# ==========================================
# TAB 3 — Your Investigation
# ==========================================
with tab3:
    st.markdown('<span class="section-num">§ 03 — METHODOLOGY</span>', unsafe_allow_html=True)
    st.markdown("## The four-possibilities test")
    st.markdown(
        '<p class="body-text">When you observe a correlation between two variables '
        '<strong>A</strong> and <strong>B</strong>, at least four explanations are '
        'possible. Good causal reasoning means ruling each out, deliberately, '
        'rather than defaulting to the most intuitive story.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
| No. | Explanation | Canonical example |
|----|-----|------|
| I   | A causes B | Smoking → lung cancer |
| II  | B causes A (reverse causation) | Do depressed people use social media more, or does social media cause depression? |
| III | A confounder C causes both A and B | Ice cream & drowning (heat causes both) |
| IV  | Coincidence — especially in small samples or when many variables are tested | Nicolas Cage films & pool drownings |
        """
    )

    st.markdown("---")
    st.markdown('<span class="section-num">EXERCISE</span>', unsafe_allow_html=True)
    st.markdown("### Reason through a scenario")

    scenario = st.selectbox(
        "Choose a scenario",
        [
            "Students who eat breakfast score higher on tests",
            "Countries with more storks have higher birth rates",
            "People who own more books tend to earn more money",
            "Neighborhoods with more churches have more crime",
        ],
    )

    st.markdown(
        f'<div class="pull-quote">{scenario}.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="body-text" style="font-size:0.95rem;">For each possibility, '
        'write down how it might plausibly work in this case.</p>',
        unsafe_allow_html=True,
    )

    p1 = st.text_area("I — A causes B: how might this work?", height=80, key="p1")
    p2 = st.text_area("II — B causes A (reverse causation): how might this work?", height=80, key="p2")
    p3 = st.text_area("III — A confounder C causes both: what could C be?", height=80, key="p3")
    p4 = st.text_area("IV — Coincidence: is this plausible here? Why or why not?", height=80, key="p4")

    if st.button("Reveal instructor notes"):
        notes = {
            "Students who eat breakfast score higher on tests": """
**I.** Nutrition genuinely aids cognition and focus — plausible.
**II.** Unlikely — test scores don't cause breakfast. But a trait like "being a prepared student" could cause both.
**III.** *The likely culprit.* Family income and household stability. Kids in stable, resourced home environments eat breakfast *and* study more, *and* have fewer absences.
**IV.** Unlikely given replicated studies. Note that effect sizes often shrink dramatically when controlling for socioeconomic status — a diagnostic signature of confounding.
            """,
            "Countries with more storks have higher birth rates": """
**I.** Biologically absurd (and yet folklore persisted for centuries).
**II.** Unlikely in any real sense.
**III.** *The likely culprit.* Country size and rural character. Large rural countries have more stork habitat *and* higher birth rates (demographic patterns correlate with rurality).
**IV.** Partially — this is a classic example (Höfer et al., 2004) used to illustrate exactly this failure mode.
            """,
            "People who own more books tend to earn more money": """
**I.** Reading could genuinely build skills, vocabulary, and critical thinking that raise income.
**II.** Higher income clearly lets people buy more books.
**III.** *The likely culprit.* Education level, parental background, cultural capital — these cause both book ownership and higher earnings.
**IV.** Unlikely to be coincidence — the pattern replicates widely. The harder question is how to decompose the mixed causal contributions.
            """,
            "Neighborhoods with more churches have more crime": """
**I.** Almost certainly not — churches don't cause crime.
**II.** Unlikely as a direct path.
**III.** *The likely culprit.* Population density. Dense urban neighborhoods have more of *everything* — more churches, more crime, more restaurants, more of every count-based variable.
**IV.** Not coincidence — it's a consistent pattern, but the confounder explains it completely.
            """,
        }
        st.info(notes[scenario])

# ==========================================
# FOOTER
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    '<div style="border-top:2px solid #1a1a1a;padding-top:1rem;font-family:JetBrains Mono,monospace;'
    'font-size:0.7rem;letter-spacing:0.15em;text-transform:uppercase;color:#666;">'
    'Built with Streamlit · Open source · For university social science courses · '
    '<span style="color:#8b0000;">◐ End of issue</span>'
    '</div>',
    unsafe_allow_html=True,
)
