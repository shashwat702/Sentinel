#  Honeywell Sentinel AI
# AI-Powered Behavioral Threat Intelligence Platform

Honeywell Sentinel AI is an intelligent cybersecurity platform designed to detect behavioral anomalies, insider threats, and suspicious user activities using Machine Learning.

Unlike traditional signature-based detection systems, Sentinel AI focuses on **how users behave** rather than simply matching known attack patterns. This enables the platform to identify previously unseen threats while reducing alert fatigue for Security Operations Center (SOC) analysts.

---

##  Problem Statement

Organizations generate millions of security events every day. Security teams often struggle to identify genuine threats hidden among thousands of alerts.

Traditional systems mainly rely on predefined attack signatures, making them less effective against:

- Insider Threats
- Credential Misuse
- Behavioral Deviations
- Unknown Attack Patterns
- Zero-Day Behaviors

Honeywell Sentinel AI addresses this challenge using AI-driven behavioral analytics.

---

#  Key Features

- AI-Based Behavioral Anomaly Detection
- Random Forest Threat Classification
- Executive SOC Dashboard
- Live Threat Feed
- Security Analytics
- Entity Investigation
- MITRE ATT&CK Mapping
- AI Security Copilot
- Intelligent Security Recommendations
- Risk Scoring
- Confidence Estimation

---

#  System Architecture

```
User Activity Logs
        │
        ▼
Behavior Profiling
        │
        ▼
Random Forest Model
        │
        ▼
Threat Detection
        │
        ▼
SOC Dashboard
        │
 ┌──────┼───────────┬───────────┐
 ▼      ▼           ▼           ▼
Analytics Investigation MITRE AI Copilot
                     │
                     ▼
             Recommendations
```

---

#  Machine Learning Pipeline

1. Synthetic behavioral log generation
2. Baseline user profiling
3. Feature engineering
4. Random Forest classification
5. Confidence estimation
6. Risk score generation
7. Dashboard visualization

---

#  Dashboard Modules

### Executive Overview
Provides a high-level summary of system health, active threats, model confidence, and risk indicators.

### Live Threat Feed
Displays real-time suspicious activities with filtering, severity classification, and downloadable reports.

### Security Analytics
Visualizes attack trends, targeted departments, geographical distribution, and resource usage.

### Entity Investigation
Allows analysts to investigate individual users, departments, locations, timelines, and accessed resources.

### MITRE ATT&CK Mapping
Maps detected attacks to MITRE ATT&CK techniques and provides mitigation guidance.

### AI Security Copilot
Summarizes detected threats and assists analysts with investigation insights.

### Recommendations
Provides prioritized remediation actions based on detected attack types.

---

#  Technologies Used

## Frontend
- Streamlit
- Plotly

## Backend
- Python

## Machine Learning
- Scikit-learn
- Random Forest

## Data Processing
- Pandas
- NumPy

---

#  Project Structure

```
Honeywell-SentinelAI
│
├── baseline/
├── classifier/
├── dashboard/
├── data/
├── generator/
├── presentation/
├── report/
└── requirements.txt
```


#  Results

- High behavioral anomaly detection accuracy
- Real-time threat visualization
- MITRE ATT&CK integration
- Explainable investigation workflow
- Actionable remediation recommendations

# Future Scope
- Real-time streaming with Kafka
- Explainable AI (SHAP/LIME)
- Deep Learning based detection
- Cloud deployment
- Integration with Microsoft Sentinel and Splunk
- Automated SOAR playbooks



**Honeywell Sentinel AI**

Developed as part of the Honeywell Connect Hackathon.

---

#  License

This project is developed for educational and hackathon purposes.
