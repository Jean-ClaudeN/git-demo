"""
Correlation vs Causation — Interactive Teaching Tool
Built with Streamlit for classroom demo + student exploration.
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# ---------- Page config ----------
st.set_page_config(
    page_title="Correlation vs Causation",
    page_icon="📊",
    layout="wide",
)

# ---------- Header ----------
st.title("📊 Correlation vs Causation")
st.markdown(
    "*An interactive tool for exploring why correlation does not imply causation — "
    "and what it takes to move from pattern to cause.*"
)

tab1, tab2, tab3 = st.tabs(
    ["🎛️ Explore: The Confounder Simulator", "🌍 Real Examples", "🧠 Your Turn"]
)

# =====================================================
# TAB 1 — Confounder Simulator
# =====================================================
with tab1:
    st.header("Build your own spurious correlation")
    st.markdown(
        "Two variables — **ice cream sales** and **drowning incidents** — have "
        "no direct causal link. But both are influenced by a third variable: "
        "**summer heat**. Use the sliders to control how strongly heat drives each, "
        "and watch what happens to their correlation."
    )

    col_controls, col_plot = st.columns([1, 2])

    with col_controls:
        st.subheader("Controls")
        n_points = st.slider("Number of observations (days)", 30, 500, 150, step=10)
        heat_to_icecream = st.slider(
            "How strongly heat drives ice cream sales", 0.0, 1.0, 0.8, step=0.05
        )
        heat_to_drowning = st.slider(
            "How strongly heat drives drowning incidents", 0.0, 1.0, 0.7, step=0.05
        )
        noise = st.slider("Random noise", 0.0, 1.0, 0.3, step=0.05)
        seed = st.number_input("Random seed", value=42, step=1)

    # Generate data
    rng = np.random.default_rng(int(seed))
    heat = rng.uniform(0, 1, n_points)  # the hidden confounder
    ice_cream = (
        heat_to_icecream * heat
        + noise * rng.normal(0, 0.3, n_points)
    )
    drowning = (
        heat_to_drowning * heat
        + noise * rng.normal(0, 0.3, n_points)
    )

    # Rescale to interpretable units
    ice_cream_sales = 100 + 400 * (ice_cream - ice_cream.min()) / (
        ice_cream.max() - ice_cream.min() + 1e-9
    )
    drowning_count = 20 * (drowning - drowning.min()) / (
        drowning.max() - drowning.min() + 1e-9
    )
    heat_f = 60 + 40 * heat  # Fahrenheit

    df = pd.DataFrame(
        {
            "Temperature (°F)": heat_f,
            "Ice cream sales ($)": ice_cream_sales,
            "Drownings": drowning_count,
        }
    )

    # Correlation
    r, p = stats.pearsonr(df["Ice cream sales ($)"], df["Drownings"])

    with col_plot:
        show_heat = st.checkbox(
            "🔍 Reveal the confounder (color points by temperature)", value=False
        )

        if show_heat:
            fig = px.scatter(
                df,
                x="Ice cream sales ($)",
                y="Drownings",
                color="Temperature (°F)",
                color_continuous_scale="RdYlBu_r",
                trendline="ols",
                trendline_color_override="black",
            )
        else:
            fig = px.scatter(
                df,
                x="Ice cream sales ($)",
                y="Drownings",
                trendline="ols",
                trendline_color_override="crimson",
            )

        fig.update_layout(
            height=450,
            margin=dict(l=0, r=0, t=30, b=0),
            title=f"Correlation r = {r:.3f}  |  p-value = {p:.2e}",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Interpretation box
    st.markdown("---")
    if abs(r) > 0.5 and not show_heat:
        st.warning(
            f"📰 **Headline writer's dream:** *'Strong link between ice cream "
            f"and drowning (r = {r:.2f})!'* — But we built this data ourselves. "
            f"Neither variable affects the other. The correlation is entirely "
            f"driven by temperature. Check the box above to see it."
        )
    elif show_heat:
        st.success(
            "✅ Now you can see it: the color gradient shows that *both* variables "
            "are driven by temperature. High-temperature days (red) cluster in the "
            "upper right; cool days (blue) cluster in the lower left. The apparent "
            "relationship between ice cream and drowning is **spurious** — a "
            "textbook confounding variable."
        )
    else:
        st.info(
            "Try increasing both 'heat drives' sliders to see the spurious "
            "correlation grow stronger."
        )

    with st.expander("💭 Discussion prompts"):
        st.markdown(
            """
        - What would happen to the correlation if you set *both* heat-driver
          sliders to 0? Why?
        - If a researcher only observed ice cream and drowning data (no
          temperature), could they detect the confounder from the data alone?
        - Name another real-world pair of variables that might be confounded by
          a third variable you can't directly measure.
        """
        )

# =====================================================
# TAB 2 — Real Examples
# =====================================================
with tab2:
    st.header("Real-world examples of misleading correlations")

    example = st.selectbox(
        "Pick an example:",
        [
            "Firefighters & fire damage",
            "Shoe size & reading ability (in children)",
            "Countries: chocolate consumption & Nobel laureates",
        ],
    )

    rng2 = np.random.default_rng(7)

    if example == "Firefighters & fire damage":
        # Confounder: fire size / city size
        size = rng2.uniform(1, 10, 60)
        firefighters = 2 * size + rng2.normal(0, 1, 60)
        damage = 50 * size + rng2.normal(0, 20, 60)
        data = pd.DataFrame(
            {
                "Firefighters on scene": firefighters,
                "Damage ($ thousands)": damage,
                "Fire size (acres)": size,
            }
        )
        x, y, conf = "Firefighters on scene", "Damage ($ thousands)", "Fire size (acres)"
        wrong_take = (
            "**Naive conclusion:** More firefighters cause more damage — "
            "so cities should reduce fire department size."
        )
        right_take = (
            "**What's actually happening:** Bigger fires cause *both* more "
            "damage *and* the dispatch of more firefighters. Fire size is the "
            "confounder. The causal arrow runs: fire size → firefighters sent, "
            "and separately, fire size → damage."
        )

    elif example == "Shoe size & reading ability (in children)":
        # Confounder: age
        age = rng2.uniform(5, 15, 80)
        shoe = 2 + 0.6 * age + rng2.normal(0, 0.5, 80)
        reading = 20 + 8 * age + rng2.normal(0, 6, 80)
        data = pd.DataFrame(
            {
                "Shoe size": shoe,
                "Reading test score": reading,
                "Age (years)": age,
            }
        )
        x, y, conf = "Shoe size", "Reading test score", "Age (years)"
        wrong_take = (
            "**Naive conclusion:** Bigger feet make children better readers — "
            "perhaps foot size boosts brain development?"
        )
        right_take = (
            "**What's actually happening:** Older children have bigger feet *and* "
            "more reading experience. Age is the confounder driving both."
        )

    else:
        # Chocolate & Nobel — famous example from a 2012 NEJM letter
        gdp = rng2.uniform(5, 70, 25)  # GDP per capita, thousands
        chocolate = 2 + 0.15 * gdp + rng2.normal(0, 2, 25)
        nobels = 0.1 * gdp + rng2.normal(0, 3, 25)
        nobels = np.clip(nobels, 0, None)
        data = pd.DataFrame(
            {
                "Chocolate consumption (kg/person/yr)": chocolate,
                "Nobel laureates per 10M people": nobels,
                "GDP per capita ($k)": gdp,
            }
        )
        x, y, conf = (
            "Chocolate consumption (kg/person/yr)",
            "Nobel laureates per 10M people",
            "GDP per capita ($k)",
        )
        wrong_take = (
            "**Naive conclusion:** Chocolate makes you smarter — eat more and "
            "win a Nobel Prize. *(This was actually published in the New England "
            "Journal of Medicine as a tongue-in-cheek letter in 2012, and many "
            "readers missed the joke.)*"
        )
        right_take = (
            "**What's actually happening:** Wealthier countries can afford more "
            "chocolate imports *and* invest more in scientific research "
            "infrastructure. GDP per capita is the confounder."
        )

    reveal = st.toggle("Show the confounder", value=False)

    if reveal:
        fig2 = px.scatter(
            data, x=x, y=y, color=conf,
            color_continuous_scale="Viridis",
            trendline="ols",
        )
    else:
        fig2 = px.scatter(
            data, x=x, y=y,
            trendline="ols",
            trendline_color_override="crimson",
        )

    r2, _ = stats.pearsonr(data[x], data[y])
    fig2.update_layout(
        height=450,
        title=f"Observed correlation: r = {r2:.3f}",
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig2, use_container_width=True)

    if not reveal:
        st.error(wrong_take)
        st.caption("👆 Toggle 'Show the confounder' above to see what's really going on.")
    else:
        st.success(right_take)

# =====================================================
# TAB 3 — Your Turn
# =====================================================
with tab3:
    st.header("Reasoning practice: the four possibilities")
    st.markdown(
        """
    When you observe a correlation between **A** and **B**, at least four
    explanations are possible. Good causal reasoning means ruling them out
    one by one.
    """
    )

    st.markdown(
        """
    | # | Explanation | Example |
    |---|---|---|
    | 1 | A causes B | Smoking → lung cancer |
    | 2 | B causes A (reverse causation) | Depressed people use social media more — or does social media cause depression? |
    | 3 | A third variable C causes both | Ice cream & drowning (heat causes both) |
    | 4 | Coincidence (especially in small samples or many tested variables) | Nicolas Cage films & pool drownings |
    """
    )

    st.markdown("---")
    st.subheader("Practice scenario")

    scenario = st.selectbox(
        "Pick a scenario to reason through:",
        [
            "Students who eat breakfast score higher on tests",
            "Countries with more storks have higher birth rates",
            "People who own more books tend to earn more money",
            "Neighborhoods with more churches have more crime",
        ],
    )

    st.markdown(f"**Scenario:** *{scenario}*")
    st.markdown(
        "For each of the four possibilities, write what it would look like here:"
    )

    p1 = st.text_area("1️⃣ A causes B — how might this work?", height=70)
    p2 = st.text_area("2️⃣ B causes A (reverse causation) — how might this work?", height=70)
    p3 = st.text_area("3️⃣ A confounder C causes both — what could C be?", height=70)
    p4 = st.text_area("4️⃣ Coincidence — is this plausible? Why or why not?", height=70)

    if st.button("Reveal discussion notes"):
        notes = {
            "Students who eat breakfast score higher on tests": """
            - **A→B:** Nutrition genuinely aids cognition and focus.
            - **B→A (reverse):** Unlikely — test scores don't cause breakfast.
              But *a third trait* (being a "prepared student") could cause both.
            - **Confounder:** Family income and household stability. Kids with
              stable home environments eat breakfast *and* study more.
            - **Coincidence:** Unlikely given replicated studies, but effect sizes
              often shrink dramatically when controlling for socioeconomic status.
            """,
            "Countries with more storks have higher birth rates": """
            - **A→B:** Historically assumed (by folklore!) but biologically absurd.
            - **B→A:** Unlikely in any real sense.
            - **Confounder:** Country size and rural character. Large rural
              countries have more storks (habitat) *and* higher birth rates
              (demographic patterns).
            - **Coincidence:** Partially — this is a classic example used by
              statisticians Höfer et al. (2004) precisely to show how confounded
              data can produce seemingly absurd correlations.
            """,
            "People who own more books tend to earn more money": """
            - **A→B:** Reading might genuinely build skills that raise income.
            - **B→A:** Higher income lets people buy more books.
            - **Confounder:** Education level, family background, or cultural
              capital cause both book ownership and higher earnings.
            - **Coincidence:** Unlikely — this correlation replicates widely,
              but the causal mechanism is contested and probably mixed.
            """,
            "Neighborhoods with more churches have more crime": """
            - **A→B:** Almost certainly not — churches don't cause crime.
            - **B→A:** Unlikely as a direct causal path.
            - **Confounder:** Population density! Dense urban neighborhoods have
              more of *everything* — more churches, more crime, more restaurants,
              more of every count-based variable.
            - **Coincidence:** Not coincidence — it's a consistent pattern driven
              by the confounder.
            """,
        }
        st.info(notes[scenario])

# ---------- Footer ----------
st.markdown("---")
st.caption(
    "Built with Streamlit · Open source on GitHub · "
    "Designed for university social science courses."
)
