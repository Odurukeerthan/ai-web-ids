# 🛡️ AI-Driven Web Intrusion Detection System (IDS)

An AI-based Web Intrusion Detection System that detects malicious web traffic by analyzing real HTTP request logs generated from a vulnerable web application using machine learning and behavioral analysis.

> 🚧 This project is actively evolving. Implemented components are marked clearly, and future enhancements are listed transparently.

---

## 📌 Project Overview

Modern web applications face continuous attacks such as SQL Injection, Cross-Site Scripting (XSS), brute-force authentication attempts, and automated reconnaissance scans.  
These attacks are often hidden within large volumes of normal traffic, making manual detection impractical.

This project addresses the problem by:
- Generating **real attack traffic** using Kali Linux tools
- Capturing **real HTTP request logs**
- Engineering **temporal and behavioral features**
- Training **machine learning models** to classify attacks

---

## 🎯 Problem Statement

How can we automatically detect and classify malicious web requests hidden within normal web traffic using realistic attack data and machine learning techniques?

---

## 🧩 Current System Architecture

Kali Linux (Attacker)
↓
Vulnerable Web Application (Node.js / Express)
↓
HTTP Request Logging Layer
↓
Feature Engineering + Windowing
↓
Machine Learning Classification


---

## 🛠️ Technologies Used

| Component | Technology |
|--------|------------|
| Attacker Environment | Kali Linux |
| Attack Tools | sqlmap, hydra, nikto |
| Backend | Node.js (Express) |
| Logging | File-based HTTP request logs |
| Data Processing | Python (Pandas, NumPy) |
| Machine Learning | Scikit-learn |
| Visualization | Matplotlib |
| Version Control | Git & GitHub |

---

## 🔍 Attack Types Covered

| Attack Type | Status |
|-----------|--------|
| SQL Injection | ✅ Implemented |
| Cross-Site Scripting (XSS) | ✅ Implemented |
| Brute-force Login Attacks | ✅ Implemented |
| Reconnaissance (Nikto scans) | ✅ Implemented |
| DDoS | ❌ Not included |

All attacks are executed **locally on localhost** for ethical and legal safety.

---

## 📊 Dataset Engineering (Implemented)

- Generated **40,000+ real HTTP requests**
- Extracted request-level features:
  - Payload size
  - Status codes
  - Request timing
  - HTTP method
- Applied **weak supervision labeling**
- Built:
  - Time-based window dataset
  - Sliding-window dataset
- Final merged dataset:
  - **12,705 labeled behavioral windows**
  - Natural class imbalance preserved

### Final Dataset Classes
- Normal
- SQL Injection
- XSS
- Brute Force
- Reconnaissance

---

## 🤖 Machine Learning (Implemented)

Two models were trained and evaluated:

### 1️⃣ Logistic Regression (Baseline)
- Used to validate feature quality
- Class-weight balancing applied
- Strong recall for payload-based attacks

### 2️⃣ Random Forest (Final Model)
- Improved generalization
- ~93% overall accuracy
- High recall for SQLi and XSS
- Acceptable false positives (security-preferred behavior)

### Evaluation Metrics
- Confusion Matrix
- Precision / Recall / F1-score
- Feature Importance
- Temporal behavior analysis

---

## 📈 Explainability & Analysis (Implemented)

The project includes:
- Random Forest feature importance plot
- Confusion matrix visualization
- Dataset class distribution
- Brute-force temporal burst pattern plot

These confirm the model learns **behavioral and temporal attack patterns**, not just static strings.

---

## ⚠️ Current Limitations

- Detection is **offline / near-real-time**
- No live inference on each incoming request yet
- No frontend dashboard implemented
- Local-only deployment

---

## 🚧 Future Work

- Real-time inference pipeline
- Live security dashboard (React)
- MongoDB-based log storage
- Alert severity scoring
- Dockerized deployment
- SIEM integration

---

## 🧠 Key Learning Outcomes

- Understanding real-world web attack behavior
- Log-based intrusion detection techniques
- Handling imbalanced security datasets
- Temporal feature engineering for ML
- Security-focused evaluation metrics

---

## 📄 License

This project is intended for educational and research purposes.

