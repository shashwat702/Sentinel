import streamlit as st

from components.ai_copilot import ai_copilot_page
from components.analytics import analytics_page
from components.investigation import investigation_page
from components.live_feed import live_feed_page
from components.mitre import mitre_page
from components.overview import overview_page
from components.recommendations import recommendation_page
from ui import apply_theme, load_predictions


st.set_page_config(
    page_title="Honeywell Sentinel AI",
    page_icon="shield",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()

PAGES = {
    "Overview": overview_page,
    "Live Threat Feed": live_feed_page,
    "Analytics": analytics_page,
    "AI Copilot": ai_copilot_page,
    "Entity Investigation": investigation_page,
    "MITRE ATT&CK": mitre_page,
    "Recommendations": recommendation_page,
}

NAV_LABELS = {
    "Overview": "Home  Overview",
    "Live Threat Feed": "Alert  Live Threat Feed",
    "Analytics": "Chart  Analytics",
    "AI Copilot": "AI  Copilot",
    "Entity Investigation": "Search  Entity Investigation",
    "MITRE ATT&CK": "Shield  MITRE ATT&CK",
    "Recommendations": "Idea  Recommendations",
}


with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <h2>Sentinel AI</h2>
            <p>Behavioral Threat Intelligence</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    predictions = load_predictions()
    if not predictions.empty:
        total = len(predictions)
        threats = len(predictions[predictions["Predicted"] != "normal"]) if "Predicted" in predictions.columns else 0
        entities = predictions["entity_id"].nunique() if "entity_id" in predictions.columns else total

        st.markdown(
            f"""
            <div class="sidebar-stats">
                <div class="sidebar-stat">
                    <div class="sidebar-stat-accent" style="background:#0f766e;"></div>
                    <div class="sidebar-stat-copy">
                        <div class="sidebar-stat-label">Events</div>
                        <div class="sidebar-stat-value">{total:,}</div>
                    </div>
                </div>
                <div class="sidebar-stat">
                    <div class="sidebar-stat-accent" style="background:#dc2626;"></div>
                    <div class="sidebar-stat-copy">
                        <div class="sidebar-stat-label">Threats</div>
                        <div class="sidebar-stat-value">{threats:,}</div>
                    </div>
                </div>
                <div class="sidebar-stat">
                    <div class="sidebar-stat-accent" style="background:#f97316;"></div>
                    <div class="sidebar-stat-copy">
                        <div class="sidebar-stat-label">Entities</div>
                        <div class="sidebar-stat-value">{entities:,}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

    selected_label = st.radio(
        "Navigation",
        list(NAV_LABELS.values()),
        label_visibility="collapsed",
    )

page = next(key for key, label in NAV_LABELS.items() if label == selected_label)

st.markdown("# Honeywell Sentinel AI")
st.caption("AI Powered Behavioral Threat Intelligence Platform")

PAGES[page]()
