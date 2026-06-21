from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from content import LIMITS, PRINCIPLES, STUDIES
from model import CLINICAL_PROFILES, ModelParameters, simulate


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"

st.set_page_config(
    page_title="Sémiologie et réseaux · Thèse de C. Gauld",
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
    rows = [
        ["Réseau statique comparatif", "Structure et centralité", "35 808 × 39 variables", "Comparaisons âge / sexe", "Pas de causalité individuelle"],
        ["mlVAR dynamique", "Ordre temporel intra-individuel", "8 260 EMA / 211 patients", "Temporel, contemporain, interindividuel", "Fenêtres courtes et sélection"],
        ["Network Outcome Analysis", "Entrée symptomatique vers l’issue", "136 patients × 23 items", "Issue thérapeutique intégrée au réseau", "Association directe ≠ mécanisme"],
        ["Réseau hybride", "Pont sémiologie–SEEG", "42 patients / 469 crises", "23 signes + 9 régions", "Robustesse faible (CS ≈ 0,05)"],
    ]
    frame = pd.DataFrame(rows, columns=["Méthode", "Question", "Échelle", "Apport", "Limite"])
    st.dataframe(frame, hide_index=True, width="stretch")

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
    gallery = st.tabs(["Sommeil", "Addictologie", "Catatonie", "Épileptologie"])
    with gallery[0]:
        st.image(ASSETS / "figure_07_sleep_sex_networks.png", caption="Figure 7 — Réseaux du sommeil selon le sexe : femmes (A) et hommes (B).", width="stretch")
        st.image(ASSETS / "figure_08_sleep_age_networks.png", caption="Figure 8 — Réseaux du sommeil selon l’âge : 18–30 ans (A), 31–45 ans (B), 46–55 ans (C), > 55 ans (D).", width="stretch")
    with gallery[1]:
        st.image(ASSETS / "figure_12_addiction_simple_networks.png", caption="Figure 12 — Réseaux simplifiés : contemporain, temporel et interindividuel.", width="stretch")
        st.image(ASSETS / "figure_13_addiction_full_networks.png", caption="Figure 13 — Réseaux complets à six variables : contemporain, temporel et interindividuel.", width="stretch")
    with gallery[2]:
        c1, c2 = st.columns(2)
        c1.image(ASSETS / "figure_16_catatonie_non_repondeurs.png", caption="Figure 16 — Non-répondeurs au lorazépam (n = 76).", width="stretch")
        c2.image(ASSETS / "figure_17_catatonie_repondeurs.png", caption="Figure 17 — Répondeurs au lorazépam (n = 60).", width="stretch")
        st.image(ASSETS / "figure_18_catatonie_noa.png", caption="Figure 18 — Network Outcome Analysis : connexion directe entre immobilité/stupeur et réponse aux benzodiazépines.", width="stretch")
    with gallery[3]:
        st.image(ASSETS / "figure_20_reseau_semiologique.png", caption="Figure 20 — Réseau sémiologique des crises préfrontales (N = 42).", width="stretch")
        st.image(ASSETS / "figure_21_epilepsy_hybrid_network.png", caption="Figure 21 — Réseau hybride associant caractéristiques sémiologiques et activité cérébrale (N = 42).", width="stretch")


def dynamical_tab() -> None:
    st.markdown("## Modèle clinique computationnel")
    st.markdown(
        '<div class="note">Simulation pédagogique du cadre formel discuté dans la thèse. '
        "Elle emploie les quatre équations du travail <i>Dynamical Systems for Computational Psychiatry</i> ; le modèle reste qualitatif et non ajusté aux données empiriques.</div>",
        unsafe_allow_html=True,
    )
    st.latex(r"""
    \begin{aligned}
    \tau_x\frac{dx}{dt} &= \frac{S_{max}}{1+\exp\!\left(\frac{R_s-y}{\lambda_s}\right)}-x \\
    \tau_y\frac{dy}{dt} &= \frac{P}{1+\exp\!\left(\frac{R_b-y}{\lambda_b}\right)}+fL-xy-z \\
    \tau_z\frac{dz}{dt} &= S(\alpha x+\beta y)\,\zeta(t)-z \\
    \tau_f\frac{df}{dt} &= y-\lambda_f f
    \end{aligned}
    """)
    st.caption("x = intensité symptomatique · y = état interne / potentiation · z = environnement perçu · f = fluctuations lentes des facteurs prédisposants")

    controls, chart = st.columns([.32, .68], gap="large")
    with controls:
        st.markdown("### Paramètres")
        profile_name = st.selectbox("Profil qualitatif", list(CLINICAL_PROFILES))
        profile = CLINICAL_PROFILES[profile_name]
        r_b = st.slider("Seuil interne Rᵦ", 0.88, 1.08, float(profile["r_b"]), 0.002, key=f"rb_{profile_name}")
        predisposition_l = st.slider("Prédisposition L", 0.10, 1.20, float(profile["predisposition_l"]), 0.01, key=f"l_{profile_name}")
        sensitivity_s = st.slider("Sensibilité environnementale S", 2.0, 12.0, float(profile["environmental_sensitivity"]), 0.1, key=f"s_{profile_name}")
        noise = st.slider("Intensité du bruit ζ(t)", 0.0, 0.50, 0.0, 0.05)
        duration = st.slider("Durée simulée (jours)", 180, 1500, 800, 20)
        x0 = st.slider("Intensité symptomatique initiale x", 0.0, 2.0, 0.0, 0.05)
        y0 = st.slider("Potentiation initiale y", 0.0, 2.0, 0.10, 0.05)
        params = ModelParameters(
            r_b=r_b,
            predisposition_l=predisposition_l,
            environmental_sensitivity=sensitivity_s,
        )
        time, states = simulate(params, (x0, y0, 0.0, 0.0), duration=duration, steps=max(1200, duration * 3), noise_strength=noise)
    with chart:
        fig = go.Figure()
        for index, (name, color) in enumerate([("x · symptômes", "#2DE2E6"), ("y · potentiation", "#FF4FD8"), ("z · environnement perçu", "#A8FF60"), ("f · fluctuations lentes", "#9B8CFF")]):
            fig.add_trace(go.Scatter(x=time, y=states[:, index], name=name, mode="lines", line=dict(color=color, width=3)))
        fig.update_xaxes(title="Temps (jours)")
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
            scene=dict(bgcolor="#09090d", xaxis_title="z · environnement", yaxis_title="y · potentiation", zaxis_title="x · symptômes", xaxis=dict(gridcolor="#24242d"), yaxis=dict(gridcolor="#24242d"), zaxis=dict(gridcolor="#24242d")),
        )
        st.plotly_chart(phase, width="stretch", config={"displayModeBar": False})

    st.markdown("### Exemple de deux régimes dynamiques observés dans la thèse")
    regime_tabs = st.tabs(["Cues → craving", "Craving → cues"])
    with regime_tabs[0]:
        c1, c2 = st.columns([.36, .64])
        c1.image(ASSETS / "figure_25_phase_indices_craving.jpeg", width="stretch")
        c2.image(ASSETS / "figure_25_trajectoires_indices_craving.jpeg", width="stretch")
        st.caption("Figure 25 — Profil dans lequel les cues précèdent le craving (n = 154).")
    with regime_tabs[1]:
        c1, c2 = st.columns([.39, .61])
        c1.image(ASSETS / "figure_26_phase_craving_indices.jpeg", width="stretch")
        c2.image(ASSETS / "figure_26_trajectoires_craving_indices.jpeg", width="stretch")
        st.caption("Figure 26 — Profil dans lequel le craving précède les cues (n = 57).")


inject_css()
st.markdown('<div class="eyebrow">Thèse de doctorat · Christophe Gauld</div>', unsafe_allow_html=True)
st.markdown('<h1>SÉMIOLOGIE<br><span class="gradient">ET RÉSEAUX</span></h1>', unsafe_allow_html=True)
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
      <div class="stat"><b>x · y · z · f</b><span>système dynamique couplé</span></div>
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
