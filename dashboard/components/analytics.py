import plotly.express as px
import streamlit as st

from ui import filter_attacks, format_attack, kpi_card, load_predictions, page_header, polish_chart, search_dataframe


def analytics_page():
    page_header(
        "Security Analytics",
        "Explore attack distribution, impacted business areas, geography, and event timing.",
    )

    attacks = filter_attacks(load_predictions())

    if attacks.empty:
        st.success("No attacks detected.")
        return

    with st.sidebar:
        st.markdown("### Analytics Filters")
        selected_attacks = st.multiselect(
            "Attack Type",
            sorted(attacks["Predicted"].dropna().unique()),
            default=sorted(attacks["Predicted"].dropna().unique()),
            format_func=format_attack,
            help="Limit charts to selected attack classes.",
        )
        selected_countries = st.multiselect(
            "Country",
            sorted(attacks["country"].dropna().unique()) if "country" in attacks.columns else [],
            default=sorted(attacks["country"].dropna().unique()) if "country" in attacks.columns else [],
            help="Compare activity by country.",
        )
        search = st.text_input(
            "Search analytics",
            placeholder="Entity, resource, department...",
            help="Search across operational context columns.",
        )

    filtered = attacks[attacks["Predicted"].isin(selected_attacks)].copy()
    if selected_countries and "country" in filtered.columns:
        filtered = filtered[filtered["country"].isin(selected_countries)]

    filtered = search_dataframe(
        filtered,
        search,
        ["entity_id", "department", "country", "city", "resource_accessed", "Predicted"],
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Threat Events", f"{len(filtered):,}", "Filtered alerts", "danger")
    with c2:
        kpi_card("Attack Types", filtered["Predicted"].nunique(), "Distinct predictions", "accent")
    with c3:
        entities = filtered["entity_id"].nunique() if "entity_id" in filtered.columns else 0
        kpi_card("Entities", f"{entities:,}", "Affected identities", "primary")
    with c4:
        avg_risk = round(filtered["Risk Score"].mean(), 2) if len(filtered) else 0
        kpi_card("Average Risk", avg_risk, "0-10 score", "warning")

    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        attack_counts = filtered["Predicted"].value_counts().reset_index()
        attack_counts.columns = ["Attack", "Count"]
        attack_counts["Attack"] = attack_counts["Attack"].map(format_attack)
        fig = px.pie(
            attack_counts,
            values="Count",
            names="Attack",
            hole=0.55,
            title="Attack Distribution",
        )
        fig.update_traces(textinfo="percent+label", textposition="inside")
        st.plotly_chart(polish_chart(fig), use_container_width=True)

    with col2:
        if "department" in filtered.columns:
            dept = filtered["department"].value_counts().reset_index()
            dept.columns = ["Department", "Count"]
            fig = px.bar(
                dept,
                x="Department",
                y="Count",
                color="Count",
                title="Most Targeted Departments",
            )
            st.plotly_chart(polish_chart(fig), use_container_width=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        if "country" in filtered.columns:
            country = filtered["country"].value_counts().reset_index()
            country.columns = ["Country", "Count"]
            fig = px.bar(
                country,
                x="Country",
                y="Count",
                color="Count",
                title="Attacks by Country",
            )
            st.plotly_chart(polish_chart(fig), use_container_width=True)

    with col2:
        if "resource_accessed" in filtered.columns:
            resource = filtered["resource_accessed"].value_counts().head(10).reset_index()
            resource.columns = ["Resource", "Count"]
            fig = px.bar(
                resource,
                x="Count",
                y="Resource",
                orientation="h",
                color="Count",
                title="Top Targeted Resources",
            )
            fig.update_layout(yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(polish_chart(fig), use_container_width=True)

    st.divider()

    if "timestamp" in filtered.columns:
        hourly = (
            filtered.dropna(subset=["timestamp"])
            .assign(Hour=lambda x: x["timestamp"].dt.hour)
            .groupby(["Hour", "Predicted"])
            .size()
            .reset_index(name="Attacks")
        )
        hourly["Predicted"] = hourly["Predicted"].map(format_attack)

        fig = px.line(
            hourly,
            x="Hour",
            y="Attacks",
            color="Predicted",
            markers=True,
            title="Hourly Attack Timeline",
        )
        fig.update_traces(line=dict(width=3), marker=dict(size=7))
        st.plotly_chart(polish_chart(fig, 430), use_container_width=True)
