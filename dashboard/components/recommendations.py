import pandas as pd
import streamlit as st

from ui import filter_attacks, format_attack, kpi_card, load_predictions, page_header


RECOMMENDATIONS = {
    "brute_force": {
        "Priority": "High",
        "Recommendation": "Enable MFA and configure account lockout policies for repeated login failures.",
        "Owner": "IAM Team",
    },
    "credential_stuffing": {
        "Priority": "Critical",
        "Recommendation": "Force password resets for exposed accounts, enable MFA, and monitor failed login bursts.",
        "Owner": "IAM Team",
    },
    "impossible_travel": {
        "Priority": "High",
        "Recommendation": "Revoke suspicious sessions and require step-up authentication for risky geographies.",
        "Owner": "SOC Team",
    },
    "device_spoofing": {
        "Priority": "Medium",
        "Recommendation": "Validate device fingerprints and require re-enrollment for unknown devices.",
        "Owner": "Endpoint Security",
    },
    "lateral_movement": {
        "Priority": "Critical",
        "Recommendation": "Review admin access, isolate affected entities, and inspect privileged session activity.",
        "Owner": "SOC Team",
    },
    "low_slow_exfiltration": {
        "Priority": "Critical",
        "Recommendation": "Inspect outbound traffic, isolate affected endpoints, and enforce Data Loss Prevention controls.",
        "Owner": "Incident Response",
    },
    "insider_drift": {
        "Priority": "High",
        "Recommendation": "Review access scope, compare behavior against peer groups, and validate business justification.",
        "Owner": "SOC Team",
    },
}


def recommendation_page():
    page_header(
        "AI Security Recommendations",
        "Prioritized actions based on the attack types currently detected by the model.",
    )

    attacks = filter_attacks(load_predictions())

    if attacks.empty:
        st.success("No active threats. Your environment looks secure.")
        return

    rows = []
    for attack in sorted(attacks["Predicted"].dropna().unique()):
        action = RECOMMENDATIONS.get(
            attack,
            {
                "Priority": "Medium",
                "Recommendation": "Review logs and investigate suspicious behavior.",
                "Owner": "SOC Team",
            },
        )
        rows.append(
            {
                "Priority": action["Priority"],
                "Attack": attack,
                "Events": int((attacks["Predicted"] == attack).sum()),
                "Affected Entities": attacks[attacks["Predicted"] == attack]["entity_id"].nunique()
                if "entity_id" in attacks.columns
                else 0,
                "Recommendation": action["Recommendation"],
                "Owner": action["Owner"],
            }
        )

    rec_df = pd.DataFrame(rows)

    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    rec_df["priority_sort"] = rec_df["Priority"].map(priority_order).fillna(9)
    rec_df = rec_df.sort_values(["priority_sort", "Events"], ascending=[True, False]).drop(columns=["priority_sort"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Recommendations", len(rec_df), "Attack-specific actions", "primary")
    with c2:
        kpi_card("Critical", len(rec_df[rec_df["Priority"] == "Critical"]), "Immediate response", "danger")
    with c3:
        kpi_card("High", len(rec_df[rec_df["Priority"] == "High"]), "Priority queue", "warning")
    with c4:
        kpi_card("Owners", rec_df["Owner"].nunique(), "Teams involved", "accent")

    st.divider()

    display = rec_df.copy()
    display["Attack"] = display["Attack"].map(format_attack)

    st.dataframe(
        display,
        use_container_width=True,
        height=360,
        hide_index=True,
        column_config={
            "Events": st.column_config.NumberColumn("Events", help="Count of alerts for this attack type."),
            "Affected Entities": st.column_config.NumberColumn("Affected Entities", help="Unique entities impacted."),
            "Recommendation": st.column_config.TextColumn("Recommendation", width="large"),
        },
    )

    st.divider()

    critical = len(rec_df[rec_df["Priority"] == "Critical"])
    high = len(rec_df[rec_df["Priority"] == "High"])
    top_owner = rec_df["Owner"].value_counts().idxmax()

    st.markdown(
        f"""
        <div class="sentinel-card">
            <div class="section-label">Executive Summary</div>
            <h3>{critical} critical and {high} high-priority recommendation sets</h3>
            <p>The highest workload owner is <b>{top_owner}</b>. Start with critical recommendations, then validate affected entities and source IP patterns.</p>
            <p>Immediate actions: isolate suspicious sessions, enforce MFA, review privileged access, and preserve evidence before containment.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.download_button(
        "Download recommendations report",
        rec_df.to_csv(index=False),
        "security_recommendations.csv",
        "text/csv",
    )
