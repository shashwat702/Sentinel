import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ui import filter_attacks, format_attack, kpi_card, load_predictions, page_header, polish_chart


def overview_page():
    page_header(
        "SOC Executive Overview",
        "A compact view of alert volume, model confidence, affected entities, and attack mix.",
    )

    predictions = load_predictions()

    if predictions.empty:
        st.error("predictions.csv not found. Run `python classifier/train_classifier.py` first.")
        return

    attacks = filter_attacks(predictions)
    total_alerts = len(predictions)
    critical_alerts = len(attacks)
    entities = predictions["entity_id"].nunique() if "entity_id" in predictions.columns else total_alerts
    accuracy = round(predictions["Confidence"].mean() * 100, 2) if "Confidence" in predictions.columns else 0
    risk = round(attacks["Risk Score"].mean(), 2) if len(attacks) else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Events Analyzed", f"{total_alerts:,}", "Full prediction sample", "primary")
    with c2:
        kpi_card("Active Threats", f"{critical_alerts:,}", "Non-normal predictions", "danger")
    with c3:
        kpi_card("Entities Monitored", f"{entities:,}", "Unique identities", "accent")
    with c4:
        kpi_card("Avg Confidence", f"{accuracy}%", "Classifier confidence", "success")

    st.divider()

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=accuracy,
                number={"suffix": "%"},
                title={"text": "Detection Confidence"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#0f766e"},
                    "steps": [
                        {"range": [0, 60], "color": "#fee2e2"},
                        {"range": [60, 85], "color": "#ffedd5"},
                        {"range": [85, 100], "color": "#dcfce7"},
                    ],
                },
            )
        )
        st.plotly_chart(polish_chart(fig, 340), use_container_width=True)

    with col2:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=risk,
                title={"text": "Average Threat Risk"},
                gauge={
                    "axis": {"range": [0, 10]},
                    "bar": {"color": "#dc2626"},
                    "steps": [
                        {"range": [0, 5], "color": "#dcfce7"},
                        {"range": [5, 7], "color": "#fef3c7"},
                        {"range": [7, 10], "color": "#fee2e2"},
                    ],
                },
            )
        )
        st.plotly_chart(polish_chart(fig, 340), use_container_width=True)

    st.divider()

    col1, col2 = st.columns([1.25, 1], gap="large")

    with col1:
        st.subheader("Alert Trend")
        if "timestamp" in predictions.columns:
            trend = (
                predictions.dropna(subset=["timestamp"])
                .assign(Hour=lambda x: x["timestamp"].dt.hour)
                .groupby("Hour")
                .size()
                .reset_index(name="Alerts")
            )
            fig = px.line(trend, x="Hour", y="Alerts", markers=True, title="Events by Hour")
            fig.update_traces(line=dict(width=3), marker=dict(size=7))
            st.plotly_chart(polish_chart(fig), use_container_width=True)
        else:
            st.warning("Timestamp column not found.")

    with col2:
        st.subheader("Attack Distribution")
        if len(attacks) > 0:
            attack_counts = attacks["Predicted"].value_counts().reset_index()
            attack_counts.columns = ["Attack", "Count"]
            attack_counts["Attack"] = attack_counts["Attack"].map(format_attack)
            fig = px.pie(
                attack_counts,
                values="Count",
                names="Attack",
                hole=0.58,
                title="Detected Attack Types",
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(polish_chart(fig), use_container_width=True)
        else:
            st.success("No anomalies detected.")
