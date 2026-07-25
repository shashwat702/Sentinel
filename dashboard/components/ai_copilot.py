import streamlit as st

from ui import filter_attacks, format_attack, kpi_card, load_predictions, page_header


def _top_value(df, column):
    if column not in df.columns or df.empty:
        return "Unknown", 0
    counts = df[column].value_counts()
    if counts.empty:
        return "Unknown", 0
    return counts.idxmax(), counts.max()


def ai_copilot_page():
    page_header(
        "AI Security Copilot",
        "Fast SOC answers from the current prediction data, with concise investigation prompts.",
    )

    df = load_predictions()
    attacks = filter_attacks(df)

    if attacks.empty:
        st.success("No attacks detected.")
        return

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total Alerts", f"{len(attacks):,}", "Non-normal predictions", "danger")
    with c2:
        kpi_card("Attack Types", attacks["Predicted"].nunique(), "Distinct classes", "accent")
    with c3:
        entities = attacks["entity_id"].nunique() if "entity_id" in attacks.columns else 0
        kpi_card("Entities Affected", f"{entities:,}", "Unique entities", "primary")
    with c4:
        confidence = round(attacks["Confidence"].mean() * 100, 2) if "Confidence" in attacks.columns else 0
        kpi_card("Avg Confidence", f"{confidence}%", "Model certainty", "success")

    st.divider()

    questions = [
        "Give today's SOC summary",
        "Which attack is most common?",
        "Which department is attacked the most?",
        "Which country generated the highest alerts?",
        "Explain Brute Force",
        "Explain Credential Stuffing",
        "How should I respond to exfiltration?",
        "Show highest risk entity",
    ]

    question = st.selectbox(
        "Ask AI Copilot",
        questions,
        help="Choose a common analyst question. Answers are generated from dashboard prediction data.",
    )

    st.divider()

    if question == "Give today's SOC summary":
        top_attack, top_attack_count = _top_value(attacks, "Predicted")
        top_dept, _ = _top_value(attacks, "department")
        top_country, _ = _top_value(attacks, "country")

        st.markdown(
            f"""
            <div class="sentinel-card">
                <div class="section-label">SOC Summary</div>
                <h3>{len(attacks):,} active alerts across {entities:,} entities</h3>
                <p>The most common attack is <b>{format_attack(top_attack)}</b> with {top_attack_count:,} events.</p>
                <p>Highest impacted department: <b>{top_dept}</b>. Highest alert geography: <b>{top_country}</b>.</p>
                <p>Recommendation: prioritize Critical and High risk alerts first, then validate entity history and source IP reuse.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif question == "Which attack is most common?":
        attack, count = _top_value(attacks, "Predicted")
        st.info(f"Most frequent attack: {format_attack(attack)} with {count:,} occurrences.")

    elif question == "Which department is attacked the most?":
        dept, count = _top_value(attacks, "department")
        st.warning(f"{dept} has the highest alert count with {count:,} events.")

    elif question == "Which country generated the highest alerts?":
        country, count = _top_value(attacks, "country")
        st.info(f"{country} generated the highest alert volume with {count:,} events.")

    elif question == "Explain Brute Force":
        st.markdown(
            """
            <div class="sentinel-card">
                <div class="section-label">Threat Explanation</div>
                <h3>Brute Force</h3>
                <p>Repeated login attempts using guessed passwords until access succeeds or the account locks.</p>
                <p><b>Mitigation:</b> enforce MFA, lockout policies, throttling, and alerting on failed login bursts.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif question == "Explain Credential Stuffing":
        st.markdown(
            """
            <div class="sentinel-card">
                <div class="section-label">Threat Explanation</div>
                <h3>Credential Stuffing</h3>
                <p>Attackers reuse leaked credentials from other breaches to attempt access at scale.</p>
                <p><b>Mitigation:</b> MFA, breached-password checks, velocity controls, and forced resets for exposed users.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif question == "How should I respond to exfiltration?":
        st.markdown(
            """
            <div class="sentinel-card">
                <div class="section-label">Response Guidance</div>
                <h3>Low and Slow Exfiltration</h3>
                <p>Inspect outbound traffic, isolate suspicious sessions, validate business need, and apply DLP controls.</p>
                <p>Preserve logs before containment and hunt for similar access patterns across peer entities.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif question == "Show highest risk entity":
        row = attacks.sort_values("Risk Score", ascending=False).iloc[0]
        st.error(
            f"Highest risk entity: {row.get('entity_id', 'Unknown')} | "
            f"Attack: {format_attack(row.get('Predicted', 'Unknown'))} | "
            f"Risk: {round(row.get('Risk Score', 0), 2)} | "
            f"Department: {row.get('department', 'Unknown')} | "
            f"Country: {row.get('country', 'Unknown')}"
        )
