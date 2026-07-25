import plotly.express as px
import streamlit as st

from ui import filter_attacks, format_attack, kpi_card, load_predictions, page_header, polish_chart, search_dataframe


def investigation_page():
    page_header(
        "Entity Investigation",
        "Drill into affected identities, timelines, resources, and the raw alert history.",
    )

    df = filter_attacks(load_predictions())

    if df.empty:
        st.success("No suspicious entities detected.")
        return

    with st.sidebar:
        st.markdown("### Investigation Filters")
        search = st.text_input(
            "Search entity",
            placeholder="USER_0001, Finance, India...",
            help="Search by entity, department, country, city, resource, or source IP.",
        )
        selected_attacks = st.multiselect(
            "Attack Type",
            sorted(df["Predicted"].dropna().unique()),
            default=sorted(df["Predicted"].dropna().unique()),
            format_func=format_attack,
            help="Limit entity list to selected attack classes.",
        )

    filtered = df[df["Predicted"].isin(selected_attacks)].copy()
    filtered = search_dataframe(
        filtered,
        search,
        ["entity_id", "department", "country", "city", "resource_accessed", "source_ip", "Predicted"],
    )

    entities = sorted(filtered["entity_id"].astype(str).unique())
    if not entities:
        st.warning("No entities match the current filters.")
        return

    selected = st.selectbox(
        "Select Entity",
        entities,
        help="Pick an entity to inspect its alert timeline and affected resources.",
    )

    entity = filtered[filtered["entity_id"].astype(str) == selected].copy()
    entity = entity.sort_values("Risk Score", ascending=False)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total Alerts", f"{len(entity):,}", selected, "danger")
    with c2:
        risk = round(entity["Risk Score"].mean(), 2) if len(entity) else 0
        kpi_card("Risk Score", risk, "Average entity risk", "warning")
    with c3:
        dept = entity["department"].iloc[0] if "department" in entity.columns else "Unknown"
        kpi_card("Department", dept, "Primary owner", "primary")
    with c4:
        country = entity["country"].iloc[0] if "country" in entity.columns else "Unknown"
        kpi_card("Country", country, "Most recent context", "accent")

    st.divider()

    left, right = st.columns(2, gap="large")

    with left:
        attack = entity["Predicted"].value_counts().reset_index()
        attack.columns = ["Attack", "Count"]
        attack["Attack"] = attack["Attack"].map(format_attack)
        fig = px.pie(
            attack,
            values="Count",
            names="Attack",
            hole=0.5,
            title="Attack Types",
        )
        st.plotly_chart(polish_chart(fig), use_container_width=True)

    with right:
        if "resource_accessed" in entity.columns:
            resource = entity["resource_accessed"].value_counts().reset_index()
            resource.columns = ["Resource", "Count"]
            fig = px.bar(
                resource,
                x="Resource",
                y="Count",
                color="Count",
                title="Resources Accessed",
            )
            st.plotly_chart(polish_chart(fig), use_container_width=True)

    st.divider()

    if "timestamp" in entity.columns:
        timeline = entity.dropna(subset=["timestamp"]).sort_values("timestamp").copy()
        timeline["Alert"] = 1

        fig = px.scatter(
            timeline,
            x="timestamp",
            y="Risk Score",
            color="Predicted",
            size="Risk Score",
            hover_data=["resource_accessed", "country", "source_ip"],
            title="Entity Alert Timeline",
        )
        fig.for_each_trace(lambda trace: trace.update(name=format_attack(trace.name)))
        st.plotly_chart(polish_chart(fig, 430), use_container_width=True)

    st.divider()

    st.subheader("Investigation Data")
    table_cols = [
        "timestamp",
        "Severity",
        "Predicted",
        "Risk Score",
        "Confidence",
        "resource_accessed",
        "source_ip",
        "country",
        "city",
        "explanation",
    ]
    available = [col for col in table_cols if col in entity.columns]
    table = entity[available].copy()
    if "Predicted" in table.columns:
        table["Predicted"] = table["Predicted"].map(format_attack)

    st.dataframe(
        table,
        use_container_width=True,
        height=360,
        hide_index=True,
        column_config={
            "Risk Score": st.column_config.NumberColumn("Risk Score", format="%.2f"),
            "Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1, format="%.2f"),
            "explanation": st.column_config.TextColumn("Explanation", width="large"),
        },
    )
