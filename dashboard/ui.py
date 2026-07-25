from pathlib import Path

import pandas as pd
import plotly.io as pio
import streamlit as st


APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parent
PREDICTIONS_PATH = APP_ROOT / "data" / "predictions.csv"

COLORS = {
    "primary": "#0f766e",
    "primary_light": "#ccfbf1",
    "accent": "#f97316",
    "danger": "#dc2626",
    "warning": "#d97706",
    "success": "#16a34a",
    "ink": "#111827",
    "muted": "#6b7280",
    "line": "#e5e7eb",
    "surface": "#ffffff",
    "soft": "#f8fafc",
}


def apply_theme():
    pio.templates["sentinel"] = pio.templates["plotly_white"]
    pio.templates["sentinel"].layout.font.family = "Inter, Segoe UI, sans-serif"
    pio.templates["sentinel"].layout.colorway = [
        "#0f766e",
        "#f97316",
        "#2563eb",
        "#dc2626",
        "#7c3aed",
        "#16a34a",
        "#d97706",
    ]
    pio.templates.default = "sentinel"

    st.markdown(
        """
        <style>
        :root {
            --sentinel-primary: #0f766e;
            --sentinel-accent: #f97316;
            --sentinel-danger: #dc2626;
            --sentinel-warning: #d97706;
            --sentinel-success: #16a34a;
            --sentinel-ink: #111827;
            --sentinel-muted: #6b7280;
            --sentinel-line: #e5e7eb;
            --sentinel-soft: #f8fafc;
        }

        .main .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2.4rem;
            max-width: 1440px;
        }

        [data-testid="stSidebar"] {
            background: #0b1220;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"] * {
            color: #e5edf5;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 8px;
            padding: 0.45rem 0.55rem;
            margin: 0.12rem 0;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .sidebar-brand {
            padding: 0.35rem 0 0.25rem;
        }

        .sidebar-brand h2 {
            color: #f8fafc;
            font-size: 1.18rem;
            margin: 0;
        }

        .sidebar-brand p {
            color: #94a3b8;
            font-size: 0.86rem;
            margin: 0.35rem 0 0;
        }

        .sidebar-stats {
            display: grid;
            gap: 0.55rem;
            margin: 1rem 0 1.15rem;
        }

        .sidebar-stat {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.75rem;
            background: rgba(15, 23, 42, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 8px;
            padding: 0.72rem 0.78rem;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        }

        .sidebar-stat-label {
            color: #94a3b8;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0;
        }

        .sidebar-stat-value {
            color: #f8fafc;
            font-size: 1.02rem;
            font-weight: 800;
        }

        .sidebar-stat-accent {
            width: 0.45rem;
            height: 2.1rem;
            border-radius: 999px;
            flex: 0 0 auto;
        }

        .sidebar-stat-copy {
            flex: 1;
        }

        .sidebar-section {
            color: #64748b;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            margin: 1rem 0 0.45rem;
            text-transform: uppercase;
        }

        h1, h2, h3 {
            color: var(--sentinel-ink);
            letter-spacing: 0;
        }

        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            border-radius: 8px;
            padding: 1rem 1rem 0.85rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
        }

        div[data-testid="stMetric"] label {
            color: var(--sentinel-muted);
        }

        div[data-testid="stMetricValue"] {
            color: var(--sentinel-ink);
            font-size: 1.55rem;
        }

        .sentinel-title {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            margin-bottom: 0.15rem;
        }

        .sentinel-subtitle {
            color: var(--sentinel-muted);
            margin-top: 0;
            margin-bottom: 1.3rem;
        }

        .sentinel-card {
            background: #ffffff;
            border: 1px solid var(--sentinel-line);
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
        }

        .kpi-card {
            min-height: 118px;
        }

        .kpi-label {
            color: var(--sentinel-muted);
            font-size: 0.86rem;
            margin-bottom: 0.45rem;
        }

        .kpi-value {
            color: var(--sentinel-ink);
            font-size: 1.8rem;
            font-weight: 750;
            line-height: 1.1;
        }

        .kpi-note {
            color: var(--sentinel-muted);
            font-size: 0.82rem;
            margin-top: 0.65rem;
        }

        .risk-badge {
            display: inline-flex;
            align-items: center;
            border-radius: 999px;
            padding: 0.22rem 0.65rem;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid transparent;
        }

        .risk-critical {
            color: #7f1d1d;
            background: #fee2e2;
            border-color: #fecaca;
        }

        .risk-high {
            color: #7c2d12;
            background: #ffedd5;
            border-color: #fed7aa;
        }

        .risk-medium {
            color: #713f12;
            background: #fef3c7;
            border-color: #fde68a;
        }

        .risk-low {
            color: #14532d;
            background: #dcfce7;
            border-color: #bbf7d0;
        }

        .section-label {
            color: var(--sentinel-muted);
            font-size: 0.78rem;
            font-weight: 750;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }

        .stDataFrame {
            border: 1px solid var(--sentinel-line);
            border-radius: 8px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_predictions():
    if not PREDICTIONS_PATH.exists():
        return pd.DataFrame()

    df = pd.read_csv(PREDICTIONS_PATH)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "Confidence" in df.columns:
        df["Risk Score"] = (df["Confidence"] * 10).round(2)
    elif "risk_score" in df.columns:
        df["Risk Score"] = pd.to_numeric(df["risk_score"], errors="coerce").fillna(5).clip(0, 10)
    else:
        df["Risk Score"] = 5.0
    df["Severity"] = df["Risk Score"].apply(severity_label)
    return df


def page_header(title, caption):
    st.markdown(f"<h2 class='sentinel-title'>{title}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='sentinel-subtitle'>{caption}</p>", unsafe_allow_html=True)


def kpi_card(label, value, note="", tone="primary"):
    color = COLORS.get(tone, COLORS["primary"])
    st.markdown(
        f"""
        <div class="sentinel-card kpi-card" style="border-top: 3px solid {color};">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def severity_label(score):
    if score >= 9:
        return "Critical"
    if score >= 7:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


def risk_badge(severity):
    css = {
        "Critical": "risk-critical",
        "High": "risk-high",
        "Medium": "risk-medium",
        "Low": "risk-low",
    }.get(severity, "risk-low")
    return f'<span class="risk-badge {css}">{severity}</span>'


def polish_chart(fig, height=390):
    fig.update_layout(
        height=height,
        margin=dict(l=18, r=18, t=56, b=24),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend_title_text="",
        hovermode="x unified",
        font=dict(family="Inter, Segoe UI, sans-serif", size=13, color=COLORS["ink"]),
    )
    fig.update_xaxes(showgrid=False, linecolor=COLORS["line"])
    fig.update_yaxes(gridcolor=COLORS["line"], linecolor=COLORS["line"])
    return fig


def filter_attacks(df):
    if "Predicted" not in df.columns:
        return df.copy()
    return df[df["Predicted"] != "normal"].copy()


def search_dataframe(df, query, columns):
    if not query:
        return df

    usable = [col for col in columns if col in df.columns]
    if not usable:
        return df

    mask = pd.Series(False, index=df.index)
    for col in usable:
        mask = mask | df[col].astype(str).str.contains(query, case=False, na=False)
    return df[mask]


def format_attack(value):
    return str(value).replace("_", " ").title()
