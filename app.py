
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="ROADWISE | Accident Analytics",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD DATA ----------------
DATA_FILE = Path(__file__).parent / "data" / "cleaned_accidents.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load the dataset: {e}")
    st.stop()

required = ["city", "weather", "cause", "accident_severity"]
missing = [col for col in required if col not in df.columns]

if missing:
    st.error(f"Missing required columns: {', '.join(missing)}")
    st.stop()

# ---------------- WEATHER THEMES ----------------
themes = {
    "rain": {
        "name": "Rain Mode",
        "emoji": "🌧️",
        "primary": "#0284c7",
        "secondary": "#38bdf8",
        "background": "#eaf6ff",
        "banner1": "#0f3b63",
        "banner2": "#087eaa",
        "message": "Explore recorded accidents during rainy conditions."
    },
    "fog": {
        "name": "Fog Mode",
        "emoji": "🌫️",
        "primary": "#64748b",
        "secondary": "#94a3b8",
        "background": "#f1f5f9",
        "banner1": "#334155",
        "banner2": "#64748b",
        "message": "Explore recorded accidents during foggy conditions."
    },
    "clear": {
        "name": "Clear Mode",
        "emoji": "☀️",
        "primary": "#d97706",
        "secondary": "#fbbf24",
        "background": "#fff8e7",
        "banner1": "#92400e",
        "banner2": "#d97706",
        "message": "Explore recorded accidents during clear conditions."
    }
}

weather_values = sorted(
    df["weather"].dropna().astype(str).unique().tolist()
)
weather_lookup = {w.lower(): w for w in weather_values}

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.markdown("## ⚙️ Dashboard Controls")
st.sidebar.caption("Filter the accident records")

cities = sorted(df["city"].dropna().astype(str).unique())
selected_cities = st.sidebar.multiselect(
    "Select cities",
    options=cities,
    default=cities
)

weather_choices = ["All weather"] + weather_values
selected_weather = st.sidebar.selectbox(
    "Select weather theme",
    options=weather_choices,
    index=0
)

# ---------------- FILTER DATA ----------------
filtered = df.copy()

if selected_cities:
    filtered = filtered[
        filtered["city"].astype(str).isin(selected_cities)
    ]
else:
    filtered = filtered.iloc[0:0]

if selected_weather != "All weather":
    filtered = filtered[
        filtered["weather"].astype(str) == selected_weather
    ]

# Use the selected weather to style the page.
# For All weather, use a neutral blue theme.
theme_key = selected_weather.lower()
theme = themes.get(theme_key, {
    "name": "All Weather Overview",
    "emoji": "🌍",
    "primary": "#2563eb",
    "secondary": "#60a5fa",
    "background": "#f3f7fc",
    "banner1": "#123456",
    "banner2": "#256b91",
    "message": "Explore recorded accidents across all weather conditions."
})

# ---------------- CUSTOM DESIGN ----------------
st.markdown(f"""
<style>
    .stApp {{
        background: {theme["background"]};
    }}

    [data-testid="stSidebar"] {{
        background: #ffffff;
        border-right: 1px solid #dbe5ef;
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }}

    .hero {{
        background: linear-gradient(120deg,
            {theme["banner1"]}, {theme["banner2"]});
        padding: 38px 42px;
        border-radius: 24px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 12px 30px rgba(15, 45, 75, 0.16);
    }}

    .hero-tag {{
        font-size: 13px;
        letter-spacing: 2px;
        font-weight: 700;
        opacity: 0.85;
    }}

    .hero h1 {{
        color: white;
        font-size: 42px;
        margin: 10px 0 8px 0;
        font-weight: 800;
    }}

    .hero p {{
        color: #eaf6ff;
        font-size: 16px;
        margin-bottom: 0;
    }}

    .section-heading {{
        color: #18324d;
        font-size: 24px;
        font-weight: 750;
        margin: 26px 0 14px 0;
    }}

    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid #e0e9f2;
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 5px 18px rgba(30, 64, 100, 0.06);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #64748b;
        font-weight: 600;
    }}

    div[data-testid="stMetricValue"] {{
        color: #17324f;
        font-size: 30px;
        font-weight: 800;
    }}

    div[data-testid="stPlotlyChart"] {{
        background: white;
        border: 1px solid #e0e9f2;
        border-radius: 16px;
        padding: 10px;
        box-shadow: 0 5px 18px rgba(30, 64, 100, 0.05);
    }}

    .insight {{
        background: white;
        border-left: 5px solid {theme["primary"]};
        padding: 16px 20px;
        border-radius: 10px;
        margin: 10px 0 20px 0;
        color: #334155;
        box-shadow: 0 4px 14px rgba(30, 64, 100, 0.05);
    }}

    .footer {{
        color: #64748b;
        text-align: center;
        font-size: 12px;
        padding: 25px 0 5px 0;
    }}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">🚦 ROAD SAFETY • DATA INTELLIGENCE</div>
    <h1>ROADWISE {theme["emoji"]}</h1>
    <p>Indian Road Accident Probability Analysis</p>
    <br>
    <h2 style="color:white; margin-bottom:8px;">
        Understand patterns. Explore the data.
    </h2>
    <p>{theme["message"]}</p>
    <p style="font-size:12px; opacity:0.8; margin-top:12px;">
        Selected view: {theme["name"]}
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- METRICS ----------------
st.markdown('<div class="section-heading">📊 Accident Overview</div>',
            unsafe_allow_html=True)

total = len(filtered)
severity_text = filtered["accident_severity"].astype(str).str.lower()
fatal_count = severity_text.eq("fatal").sum()
fatal_percent = (fatal_count / total * 100) if total else 0
city_count = filtered["city"].nunique()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Recorded Accidents", f"{total:,}")
m2.metric("Fatal Records", f"{fatal_count:,}")
m3.metric("Cities Covered", f"{city_count:,}")
m4.metric("Fatal Record %", f"{fatal_percent:.2f}%")

if total == 0:
    st.warning("No records match the selected filters.")
    st.stop()

# ---------------- CHART HELPERS ----------------
def style_chart(fig):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Arial", color="#334155", size=12),
        margin=dict(l=20, r=20, t=45, b=30),
        title_font=dict(size=17, color="#18324d"),
        legend_title_font=dict(color="#334155"),
        hoverlabel=dict(bgcolor="white", font_color="#18324d")
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#e5edf5")
    return fig

# ---------------- ACCIDENT ANALYSIS ----------------
st.markdown('<div class="section-heading">📈 Accident Analysis</div>',
            unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    cause_counts = (
        filtered["cause"].dropna().astype(str)
        .value_counts()
        .rename_axis("Cause")
        .reset_index(name="Accidents")
        .sort_values("Accidents", ascending=True)
    )
    if not cause_counts.empty:
        fig = px.bar(
            cause_counts,
            x="Accidents",
            y="Cause",
            orientation="h",
            title="Accidents by Cause",
            color="Accidents",
            color_continuous_scale=["#bfdbfe", theme["primary"]],
            text="Accidents"
        )
        fig.update_traces(textposition="outside", cliponaxis=False)
        fig.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_chart(fig), use_container_width=True)
    else:
        st.info("No cause data available.")

with right:
    weather_counts = (
        filtered["weather"].dropna().astype(str)
        .value_counts()
        .rename_axis("Weather")
        .reset_index(name="Accidents")
    )
    if not weather_counts.empty:
        fig = px.pie(
            weather_counts,
            names="Weather",
            values="Accidents",
            title="Accidents by Weather",
            hole=0.58,
            color_discrete_sequence=[
                theme["primary"], "#14b8a6", "#f59e0b",
                "#818cf8", "#f97316"
            ]
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            marker=dict(line=dict(color="white", width=3))
        )
        st.plotly_chart(style_chart(fig), use_container_width=True)
    else:
        st.info("No weather data available.")

# ---------------- SEVERITY ANALYSIS ----------------
st.markdown('<div class="section-heading">🚨 Severity Analysis</div>',
            unsafe_allow_html=True)

severity_counts = (
    filtered["accident_severity"].dropna().astype(str)
    .value_counts()
    .rename_axis("Severity")
    .reset_index(name="Accidents")
)

if not severity_counts.empty:
    fig = px.bar(
        severity_counts,
        x="Severity",
        y="Accidents",
        title="Recorded Accidents by Severity",
        color="Severity",
        color_discrete_map={
            "fatal": "#ef4444",
            "major": "#f59e0b",
            "minor": "#10b981"
        },
        text="Accidents"
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(style_chart(fig), use_container_width=True)
else:
    st.info("No severity data available.")

# ---------------- HOURLY ANALYSIS ----------------
if "hour" in filtered.columns:
    st.markdown('<div class="section-heading">🕒 Time Pattern</div>',
                unsafe_allow_html=True)
    hourly = filtered.copy()
    hourly["hour"] = pd.to_numeric(hourly["hour"], errors="coerce")
    hourly = hourly.dropna(subset=["hour"])
    hourly["hour"] = hourly["hour"].astype(int)
    hourly = hourly.groupby("hour").size().reset_index(name="Accidents")

    if not hourly.empty:
        fig = px.line(
            hourly,
            x="hour",
            y="Accidents",
            markers=True,
            title="Recorded Accidents by Hour",
            labels={"hour": "Hour of day"}
        )
        fig.update_traces(
            line=dict(color=theme["primary"], width=4),
            marker=dict(size=8)
        )
        fig.update_xaxes(dtick=1, title="Hour (0–23)")
        st.plotly_chart(style_chart(fig), use_container_width=True)

# ---------------- PROBABILITY EXPLORER ----------------
st.markdown('<div class="section-heading">🧮 Probability Explorer</div>',
            unsafe_allow_html=True)

st.write(
    "Choose a weather condition and severity to calculate "
    "the conditional probability from the filtered records."
)

prob_data = df.copy()
if selected_cities:
    prob_data = prob_data[
        prob_data["city"].astype(str).isin(selected_cities)
    ]
else:
    prob_data = prob_data.iloc[0:0]

prob_data = prob_data.dropna(
    subset=["weather", "accident_severity"]
)

available_weather = sorted(prob_data["weather"].astype(str).unique())
available_severity = sorted(
    prob_data["accident_severity"].astype(str).unique()
)

if available_weather and available_severity:
    p1, p2 = st.columns(2)

    with p1:
        chosen_weather = st.selectbox(
            "Probability: select weather",
            available_weather,
            key="prob_weather"
        )

    with p2:
        chosen_severity = st.selectbox(
            "Probability: select severity",
            available_severity,
            key="prob_severity"
        )

    weather_records = prob_data[
        prob_data["weather"].astype(str) == chosen_weather
    ]
    matching = weather_records[
        weather_records["accident_severity"].astype(str)
        == chosen_severity
    ]

    denominator = len(weather_records)
    numerator = len(matching)
    probability = numerator / denominator if denominator else 0

    q1, q2, q3 = st.columns(3)
    q1.metric("Records in selected weather", f"{denominator:,}")
    q2.metric("Matching severity records", f"{numerator:,}")
    q3.metric("Conditional probability", f"{probability:.2%}")

    st.markdown(f"""
    <div class="insight">
        <b>Probability result</b><br>
        P({chosen_severity} | {chosen_weather}) =
        {numerator:,} / {denominator:,} =
        <b>{probability:.4f} ({probability:.2%})</b>
        <br><br>
        Among recorded accidents in {chosen_weather} weather,
        {probability:.2%} were classified as {chosen_severity}.
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No weather and severity records are available for these cities.")

# ---------------- DATA TABLES ----------------
with st.expander("📋 View cause summary"):
    st.dataframe(
        filtered["cause"].dropna().value_counts()
        .rename_axis("Cause")
        .reset_index(name="Count"),
        use_container_width=True,
        hide_index=True
    )

with st.expander("🔎 Explore filtered accident records"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
    ROADWISE • Indian Road Accident Probability Analysis<br>
    Probabilities describe recorded accidents in this dataset;
    they do not measure accident risk per trip.
</div>
""", unsafe_allow_html=True)