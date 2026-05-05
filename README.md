📊 SLA Breach Analysis & Prediction (ITSM)

🚀 Overview

This project focuses on analyzing ITSM incident data to identify SLA breach patterns and building a predictive model to proactively flag high-risk tickets.
The objective was to move beyond reporting and answer: 👉 Where SLA is failing, why it is failing, and how it can be predicted in advance.

📁 Dataset

~138K+ ITSM incidents
Includes attributes like: assignment group, category, priority, urgency, timestamps, etc.
Target variable: SLA Breach (0/1)

🔍 Key Analysis Performed

1. SLA Performance & Bottleneck Analysis
Identified 6.52% overall SLA breach rate
Detected high breach concentration in specific assignment groups
Analyzed peak breach hours across weekdays
Observed impact of priority & urgency on SLA failures

2. Root Cause Analysis

Teams with higher:
Resolution time
Reassignment count
Reopen rate
showed strong correlation with SLA breaches

3. Feature Importance (Drivers of Breach)

Top contributing factors:
Assignment Groups
Ticket Category / Subcategory
Operational workflow patterns

🤖 Machine Learning Model
Built a classification model to predict SLA breaches.

📌 Model Performance:
Accuracy: 79.77%
Precision: 11.92%
Recall: 34.13%
F1 Score: 17.66%

⚠️ Observation:

Dataset is highly imbalanced (~6–7% breaches)
Accuracy alone is misleading
Recall is more important to capture potential breaches

📊 Key Insights

High-risk incidents have ~15.5% breach rate, nearly 2x higher than medium (8%) and low risk (3%)
Majority of tickets fall under medium-risk category, making it a key improvement area
Assignment groups are major bottlenecks impacting SLA performance
Model is more suitable for risk prioritization rather than exact prediction

📈 Dashboard

Built an interactive Power BI dashboard with two main views:

1. SLA Performance & Bottlenecks
SLA breach distribution by team
Peak breach hours
Priority-wise breach analysis
Root cause indicators (resolution time, reassignment, reopen)

2. SLA Breach Prediction & Insights
Model performance metrics
Feature importance
Risk distribution
Actual vs predicted comparison

🛠️ Tech Stack

Python (Pandas, NumPy, Scikit-learn)
Power BI (Dashboard & Visualization)
Excel (Data preprocessing)
💡 Key Learning

This project highlighted that:
A model does not need perfect accuracy to be useful — even moderate performance can drive meaningful business decisions when combined with proper analysis.
📌 Conclusion
The project demonstrates how combining data analysis + machine learning + visualization can help organizations:
Identify SLA bottlenecks
Prioritize high-risk incidents
Improve operational efficiency
