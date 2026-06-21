from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from content import LIMITS, PRINCIPLES, STUDIES
from model import ModelParameters, simulate


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

st.set_page_config(
    page_title="Sémiologie relationnelle · Thèse de C. Gauld",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def inject_css() -> None:
    st.markdown(
        """
        <style>
        :root { --ink:#050507; --panel:#0d0d12; --muted:#9a9aaa; --line:#24242d; --cyan:#2de2e6; --pink:#ff4fd8; }
        .stApp { background: radial-gradient(circle at 82% 3%, #17101d 0, #08080b 34%, #050507 72%); color:#f7f7fb; }
        [data-testid="stHeader"] { background:transparent; }
        [data-testid="stToolbar"] { right:1rem; }
        .block-container { max-width:1280px; padding-top:2.2rem; padding-bottom:5rem; }
        h1,h2,h3 { letter-spacing:-.035em; }
        h1 { font-size:clamp(2.8rem,7vw,6.8rem)!important; line-height:.91!important; font-weight:800!important; }
        h2 { font-size:clamp(2rem,4vw,3.7rem)!important; line-height:1!important; margin-top:2.5rem!important; }
        p, li { color:#c7c7d1; }
        .eyebrow { color:var(--cyan); font-size:.72rem; letter-spacing:.22em; text-transform:uppercase; font-weight:800; }
        .hero-sub { max-width:850px; color:#b9b9c5; font-size:1.25rem; line-height:1.55; margin-top:1.25rem; }
        .gradient { background:linear-gradient(90deg,#fff 0%,#2de2e6 42%,#ff4fd8 100%); -webkit-background-clip:text; color:transparent; }
        .stat-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:1px; background:var(--line); border:1px solid var(--line); margin:2.4rem 0; }
        .stat { background:#09090d; padding:1.4rem; min-height:115px; }
        .stat b { display:block; color:#fff; font-size:1.8rem; margin-bottom:.25rem; }
        .stat span { color:#858594; font-size:.78rem; text-transform:uppercase; letter-spacing:.08em; }
        .study { border-top:1px solid var(--line); padding:1.35rem .15rem 1.55rem; }
        .study .num { font-size:.7rem; color:#72727f; letter-spacing:.14em; }
        .study h3 { font-size:1.45rem; margin:.25rem 0 .15rem; }
        .study .tag { font-size:.68rem; letter-spacing:.11em; text-transform:uppercase; font-weight:800; }
        .study .method { color:#7f7f8d; font-size:.82rem; margin:.8rem 0; }
        .study .result { color:#f4f4f8; font-size:1.02rem; line-height:1.5; }
        .study .clinical { color:#aaaab6; font-size:.88rem; }
        .principle { height:100%; background:linear-gradient(145deg,#111117,#09090d); border:1px solid var(--line); padding:1.25rem; border-radius:2px; }
        .principle b { color:#fff; font-size:.76rem; letter-spacing:.14em; }
        .principle p { font-size:.92rem; line-height:1.45; margin:.75rem 0 0; }
        .note { border-left:3px solid var(--pink); background:#110d14; padding:1rem 1.15rem; color:#b9b0bd; font-size:.88rem; }
        .equation { text-align:center; border:1px solid var(--line); background:#08080c; padding:1.25rem; font-size:1.15rem; }
        [data-baseweb="tab-list"] { gap:2rem; border-bottom:1px solid var(--line); }
        [data-baseweb="tab"] { background:transparent!important; padding:1rem 0!important; color:#8f8f9d!important; }
        [aria-selected="true"] { color:#fff!important; }
        [data-testid="stImage"] img { border:1px solid var(--line); background:#fff; }
        div[data-testid="stMetric"] { background:#0c0c11; border:1px solid var(--line); padding:1rem; }
        .stSlider [data-baseweb="slider"] > div > div { background:#2de2e6; }
        @media(max-width:750px){ .stat-grid{grid-template-columns:1fr 1fr;} .block-container{padding-left:1rem;padding-right:1rem;} }
        </style>
        """,
        unsafe_allow_html=True,
    )


def plot_theme(fig: go.Figure, height: int = 420) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=35, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#09090d",
        font=dict(color="#bdbdc8", family="Arial"),
        legend=dict(orientation="h", y=1.08, x=0),
        xaxis=dict(gridcolor="#24242d", zerolinecolor="#34343e"),
        yaxis=dict(gridcolor="#24242d", zerolinecolor="#34343e"),
        hoverlabel=dict(bgcolor="#15151c", font_color="#fff", bordercolor="#33333f"),
    )
    return fig


def study_card(study: dict) -> str:
    return f"""
    <div class="study">
      <div class="num">ÉTUDE {study['chapter']}</div>
      <h3>{study['domain']}</h3>
      <div class="tag" style="color:{study['accent']}">{study['dimension']}</div>
      <div class="method">{study['method']}</div>
      <p class="result">{study['result']}</p>
      <p class="clinical">↳ {study['clinical']}</p>
    </div>
    """


def overview_tab() -> None:
    st.markdown("## Une thèse, quatre terrains, un même déplacement")
    st.write(
        "Des catégories diagnostiques vers une science relationnelle de la sémiologie : "
        "décrire les symptômes par leurs relations, leurs trajectoires, leurs réponses aux interventions "
        "et leurs liens avec des mécanismes internes."
    )
    columns = st.columns(4)
    for column, study in zip(columns, STUDIES):
        with column:
            st.markdown(study_card(study), unsafe_allow_html=True)

    st.markdown("## Quatre principes cliniques organisateurs")
    columns = st.columns(4)
    for column, (title, text) in zip(columns, PRINCIPLES):
        with column:
            st.markdown(f'<div class="principle"><b>{title}</b><p>{text}</p></div>', unsafe_allow_html=True)

    st.markdown("## Le fil méthodologique")
    fig = go.Figure()
    labels = ["Données\ntransversales", "Données\nlongitudinales", "Issue\nthérapeutique", "Données\nhybrides", "Système\nX–Y–Z"]
    colors = ["#2DE2E6", "#FF4FD8", "#A8FF60", "#9B8CFF", "#FFFFFF"]
    for i, (label, color) in enumerate(zip(labels, colors)):
        fig.add_trace(go.Scatter(x=[i], y=[0], mode="markers+text", marker=dict(size=42, color=color, line=dict(width=4, color="#09090d")), text=[label], textposition="bottom center", hoverinfo="text", showlegend=False))
        if i:
            fig.add_shape(type="line", x0=i - 1, x1=i, y0=0, y1=0, line=dict(color="#4a4a55", width=3))
    fig.update_xaxes(visible=False, range=[-.45, 4.45])
    fig.update_yaxes(visible=False, range=[-.45, .35])
    st.plotly_chart(plot_theme(fig, 250), width="stretch", config={"displayModeBar": False})


def methodology_tab() -> None:
    st.markdown("## Résultats méthodologiques")
    st.caption("Ce que chaque dispositif rend visible — et ce qu’il ne permet pas de conclure.")
    rows = [
        ["Réseau statique comparatif", "Structure et centralité", "35 808 × 39 variables", "Comparaisons âge / sexe", "Pas de causalité individuelle"],
        ["mlVAR dynamique", "Ordre temporel intra-individuel", "8 260 EMA / 211 patients", "Temporel, contemporain, interindividuel", "Fenêtres courtes et sélection"],
        ["Network Outcome Analysis", "Entrée symptomatique vers l’issue", "136 patients × 23 items", "Issue thérapeutique intégrée au réseau", "Association directe ≠ mécanisme"],
        ["Réseau hybride", "Pont sémiologie–SEEG", "42 patients / 469 crises", "23 signes + 9 régions", "Robustesse faible (CS ≈ 0,05)"],
    ]
    frame = pd.DataFrame(rows, columns=["Dispositif", "Question", "Échelle", "Apport", "Limite"])
    st.dataframe(frame, hide_index=True, width="stretch")

    left, right = st.columns([1.05, .95], gap="large")
    with left:
        st.markdown("### Du nœud à la trajectoire")
        st.image(ASSETS / "figure_06_trouble_dynamique.png", caption="Figure 6 — Développement temporel d’un trouble psychiatrique selon la théorie des réseaux.", width="stretch")
    with right:
        st.markdown("### Le traitement dans le réseau")
        st.image(ASSETS / "figure_15_intervention_reseau.png", caption="Figure 15 — Évolution d’un réseau sous intervention (figure originale de la thèse).", width="stretch")

    st.markdown("### Lecture responsable")
    for limit in LIMITS:
        st.markdown(f"- {limit}")


def clinical_tab() -> None:
    st.markdown("## Résultats cliniques")
    sample_values = [35808, 8260, 136, 42]
    fig = go.Figure(go.Bar(
        x=[s["domain"] for s in STUDIES],
        y=sample_values,
        marker_color=[s["accent"] for s in STUDIES],
        text=["35 808 participants", "8 260 observations", "136 patients", "42 patients"],
        textposition="outside",
        hovertemplate="%{x}<br>%{text}<extra></extra>",
    ))
    fig.update_yaxes(type="log", title="Échelle (logarithmique)")
    st.plotly_chart(plot_theme(fig, 390), width="stretch", config={"displayModeBar": False})

    for start in (0, 2):
        columns = st.columns(2, gap="large")
        for column, study in zip(columns, STUDIES[start : start + 2]):
            with column:
                st.markdown(study_card(study), unsafe_allow_html=True)

    st.markdown("### Figures cliniques principales")
    gallery = st.tabs(["Catatonie · NOA", "Catatonie · groupes", "Épileptologie"])
    with gallery[0]:
        st.image(ASSETS / "figure_18_catatonie_noa.png", caption="Figure 18 — L’immobilité/stupeur est l’unique connexion directe avec la réponse aux benzodiazépines.", width="stretch")
    with gallery[1]:
        c1, c2 = st.columns(2)
        c1.image(ASSETS / "figure_16_catatonie_non_repondeurs.png", caption="Figure 16 — Non-répondeurs (n = 76).", width="stretch")
        c2.image(ASSETS / "figure_17_catatonie_repondeurs.png", caption="Figure 17 — Répondeurs (n = 60).", width="stretch")
    with gallery[2]:
        st.image(ASSETS / "figure_20_reseau_semiologique.png", caption="Figure 20 — Réseau sémiologique des crises préfrontales (N = 42).", width="stretch")


def dynamical_tab() -> None:
    st.markdown("## Modèle clinique computationnel")
    st.markdown(
        '<div class="note">Simulation pédagogique du cadre formel discuté dans la thèse. '
        "Les fonctions utilisées ici illustrent un système non linéaire couplé ; elles ne sont pas ajustées aux données empiriques.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div class="equation">
    dX/dt = f(X,Y) &nbsp;&nbsp;·&nbsp;&nbsp; dY/dt = g(Y,Z) &nbsp;&nbsp;·&nbsp;&nbsp; dZ/dt = h(Z,Y,X)
    </div>
    """, unsafe_allow_html=True)
    st.caption("X = symptômes observables · Y = mécanismes internes · Z = environnement ou intervention")

    controls, chart = st.columns([.32, .68], gap="large")
    with controls:
        st.markdown("### Paramètres")
        external = st.slider("Entrée externe / intervention", -1.0, 1.0, 0.20, 0.05)
        y_to_x = st.slider("Influence Y → X", 0.0, 2.0, 1.15, 0.05)
        z_to_y = st.slider("Influence Z → Y", 0.0, 2.0, 0.95, 0.05)
        feedback = st.slider("Rétroactions du système", 0.0, 1.0, 0.35, 0.05)
        nonlinearity = st.slider("Non-linéarité / saturation", 0.01, 0.40, 0.12, 0.01)
        x0 = st.slider("Symptôme initial X", -1.0, 2.0, 0.25, 0.05)
        y0 = st.slider("Mécanisme initial Y", -1.0, 2.0, 0.20, 0.05)
        z0 = st.slider("Contexte initial Z", -1.0, 2.0, 0.15, 0.05)
        params = ModelParameters(
            coupling_yx=y_to_x,
            coupling_zy=z_to_y,
            feedback_xy=feedback,
            feedback_xz=feedback * 0.65,
            feedback_yz=feedback * 0.85,
            nonlinearity=nonlinearity,
            external_input=external,
        )
        time, states = simulate(params, (x0, y0, z0))
    with chart:
        fig = go.Figure()
        for index, (name, color) in enumerate([("X · symptôme", "#2DE2E6"), ("Y · mécanisme", "#FF4FD8"), ("Z · contexte / traitement", "#A8FF60")]):
            fig.add_trace(go.Scatter(x=time, y=states[:, index], name=name, mode="lines", line=dict(color=color, width=3)))
        fig.update_xaxes(title="Temps")
        fig.update_yaxes(title="État du système")
        st.plotly_chart(plot_theme(fig, 450), width="stretch", config={"displayModeBar": False})

        phase = go.Figure(go.Scatter3d(
            x=states[:, 2], y=states[:, 1], z=states[:, 0],
            mode="lines", line=dict(color=time, colorscale=[[0, "#2DE2E6"], [1, "#FF4FD8"]], width=6),
            hovertemplate="Z=%{x:.2f}<br>Y=%{y:.2f}<br>X=%{z:.2f}<extra></extra>",
        ))
        phase.update_layout(
            height=480, margin=dict(l=0, r=0, t=30, b=0),
            paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#bdbdc8"),
            scene=dict(bgcolor="#09090d", xaxis_title="Z · contexte", yaxis_title="Y · mécanisme", zaxis_title="X · symptôme", xaxis=dict(gridcolor="#24242d"), yaxis=dict(gridcolor="#24242d"), zaxis=dict(gridcolor="#24242d")),
        )
        st.plotly_chart(phase, width="stretch", config={"displayModeBar": False})

    st.markdown("### Deux régimes dynamiques observés dans la thèse")
    regime_tabs = st.tabs(["Indices → craving", "Craving → indices", "Espaces de phase empiriques"])
    with regime_tabs[0]:
        c1, c2 = st.columns([.36, .64])
        c1.image(ASSETS / "figure_25_phase_indices_craving.jpeg", width="stretch")
        c2.image(ASSETS / "figure_25_trajectoires_indices_craving.jpeg", width="stretch")
        st.caption("Figure 25 — Profil dans lequel les indices précèdent le craving (n = 154).")
    with regime_tabs[1]:
        c1, c2 = st.columns([.39, .61])
        c1.image(ASSETS / "figure_26_phase_craving_indices.jpeg", width="stretch")
        c2.image(ASSETS / "figure_26_trajectoires_craving_indices.jpeg", width="stretch")
        st.caption("Figure 26 — Profil dans lequel le craving précède les indices (n = 57).")
    with regime_tabs[2]:
        c1, c2 = st.columns(2)
        c1.image(ASSETS / "figure_24_espace_phase_patient_1.png", caption="Patient 1", width="stretch")
        c2.image(ASSETS / "figure_24_espace_phase_patient_2.png", caption="Patient 2", width="stretch")


inject_css()
st.markdown('<div class="eyebrow">Thèse de doctorat · Christophe Gauld</div>', unsafe_allow_html=True)
st.markdown('<h1>SÉMIOLOGIE<br><span class="gradient">EN MOUVEMENT</span></h1>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Applications cliniques et neuroscientifiques des réseaux de symptômes — '
    "sémiologie, dynamique, intervention et explication.</div>",
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="stat-grid">
      <div class="stat"><b>4</b><span>terrains cliniques</span></div>
      <div class="stat"><b>4</b><span>principes organisateurs</span></div>
      <div class="stat"><b>44 246</b><span>participants / observations clés</span></div>
      <div class="stat"><b>X · Y · Z</b><span>système dynamique couplé</span></div>
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(["Vue d’ensemble", "Résultats méthodologiques", "Résultats cliniques", "Système dynamique"])
with tabs[0]:
    overview_tab()
with tabs[1]:
    methodology_tab()
with tabs[2]:
    clinical_tab()
with tabs[3]:
    dynamical_tab()

st.divider()
st.caption("Synthèse interactive réalisée à partir du manuscrit de thèse. Usage scientifique et pédagogique — ne constitue pas un outil de décision clinique.")
