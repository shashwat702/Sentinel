import pandas as pd
import streamlit as st

from ui import filter_attacks, format_attack, kpi_card, load_predictions, page_header


MITRE_MAP = {
    "brute_force": {
        "Technique ID": "T1110",
        "Technique": "Brute Force",
        "Tactic": "Credential Access",
        "Severity": "High",
        "Recommendation": "Enable MFA, account lockout policies, and failed-login monitoring.",
    },
    "credential_stuffing": {
        "Technique ID": "T1110.004",
        "Technique": "Credential Stuffing",
        "Tactic": "Credential Access",
        "Severity": "High",
        "Recommendation": "Rotate exposed credentials, enforce MFA, and block automated login bursts.",
    },
    "impossible_travel": {
        "Technique ID": "T1078",
        "Technique": "Valid Accounts",
        "Tactic": "Defense Evasion",
        "Severity": "High",
        "Recommendation": "Verify login origin, revoke suspicious sessions, and require step-up authentication.",
    },
    "device_spoofing": {
        "Technique ID": "T1036",
        "Technique": "Masquerading",
        "Tactic": "Defense Evasion",
        "Severity": "Medium",
        "Recommendation": "Validate device fingerprints and challenge unknown devices.",
    },
    "lateral_movement": {
        "Technique ID": "T1021",
        "Technique": "Remote Services",
        "Tactic": "Lateral Movement",
        "Severity": "Critical",
        "Recommendation": "Restrict admin access, review privileged sessions, and segment networks.",
    },
    "low_slow_exfiltration": {
        "Technique ID": "T1041",
        "Technique": "Exfiltration Over C2 Channel",
        "Tactic": "Exfiltration",
        "Severity": "Critical",
        "Recommendation": "Monitor outbound traffic, apply DLP controls, and isolate suspicious sessions.",
    },
    "insider_drift": {
        "Technique ID": "T1078",
        "Technique": "Valid Accounts",
        "Tactic": "Persistence",
        "Severity": "High",
        "Recommendation": "Review access patterns, enforce least privilege, and validate business justification.",
    },
}


def mitre_page():
    page_header(
        "MITRE ATT&CK Mapping",
        "Map detected behavioral threats to tactics, techniques, severity, and response guidance.",
    )

    attacks = filter_attacks(load_predictions())

    if attacks.empty:
        st.success("No attacks detected.")
        return

    rows = []
    for attack in sorted(attacks["Predicted"].dropna().unique()):
        if attack in MITRE_MAP:
            row = MITRE_MAP[attack].copy()
            row["Detected Attack"] = attack
            row["Events"] = int((attacks["Predicted"] == attack).sum())
            rows.append(row)

    mitre_df = pd.DataFrame(rows)

    if mitre_df.empty:
        st.warning("No MITRE mappings found for the detected attack labels.")
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Mapped Attacks", len(mitre_df), "Detected classes", "primary")
    with c2:
        critical = len(mitre_df[mitre_df["Severity"] == "Critical"])
        kpi_card("Critical Techniques", critical, "Require priority review", "danger")
    with c3:
        kpi_card("Total Events", f"{mitre_df['Events'].sum():,}", "Mapped alerts", "accent")

    st.divider()

    table = mitre_df.copy()
    table["Detected Attack"] = table["Detected Attack"].map(format_attack)

    st.dataframe(
        table[
            [
                "Detected Attack",
                "Events",
                "Technique ID",
                "Technique",
                "Tactic",
                "Severity",
                "Recommendation",
            ]
        ],
        use_container_width=True,
        height=360,
        hide_index=True,
        column_config={
            "Recommendation": st.column_config.TextColumn("Recommendation", width="large"),
            "Events": st.column_config.NumberColumn("Events", help="Number of dashboard alerts with this predicted label."),
        },
    )

    st.divider()

    attack = st.selectbox(
        "Choose Attack",
        mitre_df["Detected Attack"].tolist(),
        format_func=format_attack,
        help="Review technique detail and mitigation guidance for one detected attack class.",
    )

    info = MITRE_MAP[attack]

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            f"""
            <div class="sentinel-card">
                <div class="section-label">Technique</div>
                <h3>{format_attack(attack)}</h3>
                <p><b>{info['Technique ID']}</b> - {info['Technique']}</p>
                <p>Tactic: <b>{info['Tactic']}</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="sentinel-card">
                <div class="section-label">Response</div>
                <h3>{info['Severity']} Severity</h3>
                <p>{info['Recommendation']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
