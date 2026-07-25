import streamlit as st

from ui import filter_attacks, format_attack, kpi_card, load_predictions, page_header, search_dataframe


def live_feed_page():
    page_header(
        "Live Threat Feed",
        "Search, filter, sort, and export the active alerts sent to the SOC queue.",
    )

    df = filter_attacks(load_predictions())

    if df.empty:
        st.success("No active threats detected.")
        return

    with st.sidebar:
        st.markdown("### Threat Filters")
        severities = st.multiselect(
            "Severity",
            sorted(df["Severity"].dropna().unique()),
            default=sorted(df["Severity"].dropna().unique()),
            help="Filter alerts by computed risk severity.",
        )
        attacks = st.multiselect(
            "Attack Type",
            sorted(df["Predicted"].dropna().unique()),
            default=sorted(df["Predicted"].dropna().unique()),
            format_func=format_attack,
            help="Show only selected predicted attack classes.",
        )
        departments = st.multiselect(
            "Department",
            sorted(df["department"].dropna().unique()) if "department" in df.columns else [],
            default=sorted(df["department"].dropna().unique()) if "department" in df.columns else [],
            help="Narrow alerts to impacted departments.",
        )
        search = st.text_input(
            "Search",
            placeholder="Entity, country, resource, attack...",
            help="Search across entity, department, country, resource, and attack fields.",
        )

    filtered = df[
        df["Severity"].isin(severities)
        & df["Predicted"].isin(attacks)
    ].copy()

    if departments and "department" in filtered.columns:
        filtered = filtered[filtered["department"].isin(departments)]

    filtered = search_dataframe(
        filtered,
        search,
        ["entity_id", "department", "country", "city", "resource_accessed", "Predicted", "source_ip"],
    )

    filtered = filtered.sort_values(["Risk Score", "Confidence"], ascending=False)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Filtered Threats", f"{len(filtered):,}", "Current SOC queue", "danger")
    with c2:
        kpi_card("Critical", f"{len(filtered[filtered['Severity'] == 'Critical']):,}", "Risk score >= 9", "danger")
    with c3:
        avg_risk = round(filtered["Risk Score"].mean(), 2) if len(filtered) else 0
        kpi_card("Average Risk", avg_risk, "Filtered alert mean", "warning")
    with c4:
        entities = filtered["entity_id"].nunique() if "entity_id" in filtered.columns else 0
        kpi_card("Entities", f"{entities:,}", "Affected identities", "primary")

    st.divider()

    badge_counts = filtered["Severity"].value_counts().to_dict()
    st.markdown(
        " ".join(
            [
                f'<span class="risk-badge risk-critical">Critical {badge_counts.get("Critical", 0):,}</span>',
                f'<span class="risk-badge risk-high">High {badge_counts.get("High", 0):,}</span>',
                f'<span class="risk-badge risk-medium">Medium {badge_counts.get("Medium", 0):,}</span>',
                f'<span class="risk-badge risk-low">Low {badge_counts.get("Low", 0):,}</span>',
            ]
        ),
        unsafe_allow_html=True,
    )

    display_columns = [
        "Severity",
        "entity_id",
        "department",
        "country",
        "city",
        "timestamp",
        "Predicted",
        "resource_accessed",
        "Risk Score",
        "Confidence",
    ]

    available = [c for c in display_columns if c in filtered.columns]
    table = filtered[available].copy()
    if "Predicted" in table.columns:
        table["Predicted"] = table["Predicted"].map(format_attack)

    st.dataframe(
        table,
        use_container_width=True,
        height=620,
        hide_index=True,
        column_config={
            "Severity": st.column_config.TextColumn("Severity", help="Risk badge derived from confidence."),
            "Risk Score": st.column_config.NumberColumn("Risk Score", format="%.2f", help="Confidence scaled to 0-10."),
            "Confidence": st.column_config.ProgressColumn("Confidence", min_value=0, max_value=1, format="%.2f"),
        },
    )

    st.download_button(
        "Download filtered alerts",
        filtered.to_csv(index=False),
        "alerts.csv",
        "text/csv",
    )
