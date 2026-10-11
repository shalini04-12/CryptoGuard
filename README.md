# 🛡️ CryptoGuard

### Enterprise Cryptographic Inventory & Post-Quantum Migration Planner

CryptoGuard is a Python-based application designed to identify cryptographic assets, assess potential quantum-computing risks, and recommend migration strategies toward Post-Quantum Cryptography (PQC).

The project combines cryptographic inventory analysis, risk scoring, migration recommendations, and a Streamlit dashboard to help organisations understand their cryptographic exposure and plan their transition to quantum-resistant algorithms.

## 🎯 Problem Statement

Advances in quantum computing may threaten widely used public-key cryptographic algorithms, including RSA and elliptic-curve cryptography. Organisations need a structured way to discover vulnerable cryptographic assets, prioritise risks, and plan their migration to post-quantum alternatives.

CryptoGuard addresses this challenge by providing a centralised inventory analysis and migration-planning prototype.

## ✨ Key Features

* **Cryptographic Inventory:** Reads cryptographic asset information from CSV files.
* **Quantum Risk Assessment:** Identifies potentially quantum-vulnerable algorithms and assigns prototype risk scores.
* **Migration Planning:** Recommends migration actions based on the identified algorithms.
* **Interactive Dashboard:** Presents project information and analysis through a Streamlit web interface.
* **Processor Comparison:** Compares circuit compilation metrics for illustrative Processor A and Processor B configurations.
* **CSV Reports:** Saves inventory assessments and benchmark comparison results for further analysis.

## 🛠️ Technology Stack

* Python
* Streamlit
* Pandas
* Qiskit
* CSV and JSON

## 📂 Project Structure

```text
CryptoGuard/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── data/
│   ├── raw/
│   │   └── crypto_inventory.csv
│   └── processed/
│       └── risk_assessment.csv
├── processors/
│   ├── processor_A.json
│   └── processor_B.json
├── results/
│   └── tables/
│       └── processor_comparison.csv
└── src/
    ├── __init__.py
    ├── inventory.py
    ├── migration.py
    ├── risk_scoring.py
    └── benchmark.py
```

## ⚙️ Installation and Setup

### Prerequisites

* Python 3.11 or a compatible Python version
* pip package manager

### 1. Clone the repository

```bash
git clone https://github.com/shalini04-12/CryptoGuard.git
cd CryptoGuard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the inventory analysis

```bash
python main.py
```

The analysis reads the configured inventory and saves the assessment results to:

```text
data/processed/risk_assessment.csv
```

### 5. Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal to access the dashboard.

### 6. Run the preliminary processor comparison

```bash
python -m src.benchmark
```

The comparison results are saved to:

```text
results/tables/processor_comparison.csv
```

## 📊 How It Works

1. **Inventory Collection:** Cryptographic asset information is loaded from a CSV file.
2. **Algorithm Analysis:** The application identifies the algorithms associated with each asset.
3. **Risk Assessment:** Algorithms are evaluated using the project's prototype risk-scoring rules.
4. **Migration Recommendations:** The system suggests potential migration actions based on the identified algorithms.
5. **Results Generation:** The assessment is saved as a CSV file for review.
6. **Processor Comparison:** A test quantum circuit is transpiled using illustrative processor configurations, and selected compilation metrics are recorded.

## 🔐 Post-Quantum Cryptography

CryptoGuard recognises selected classical cryptographic algorithms and post-quantum cryptographic algorithm names, including:

* RSA
* ECDSA
* ECDH
* 3DES
* ML-KEM
* ML-DSA
* SLH-DSA

The migration planner provides preliminary recommendations to support planning for a transition to quantum-resistant cryptography.

Actual migration decisions should consider current standards, protocol compatibility, implementation requirements, data sensitivity, and the organisation's security policies.

## 🧪 Benchmarking Status

The repository includes a preliminary comparison between illustrative five-qubit and seven-qubit processor configurations.

The current comparison records:

* Available and logical qubit counts
* Transpiled circuit depth
* Two-qubit gate count
* SWAP count
* Transpilation time

**Important:** The current results are preliminary software measurements using illustrative connectivity settings. They are not official hardware execution results, and the configurations have not been verified against the challenge organisers' exact processor definitions. The comparison must not be interpreted as proof that one real quantum processor outperforms another.

## ⚠️ Limitations

* Risk scores are prototype triage indicators, not official NIST security ratings.
* Results depend on the input inventory and the project's configured scoring rules.
* Migration recommendations are preliminary and require expert review before production use.
* The current processor comparison measures circuit compilation rather than execution on real quantum hardware.
* Official processor configurations and noise assumptions must be incorporated when the organisers' specifications are available.

## 🚀 Future Enhancements

* Integration of verified processor configurations and noise models.
* More comprehensive cryptographic asset discovery.
* Improved risk prioritisation using asset sensitivity and exposure.
* Detailed migration tracking and progress reporting.
* Integration with enterprise cryptographic inventories.
* More extensive benchmarking and visual comparisons.

## 👩‍💻 Project Information

**Project:** CryptoGuard
**Focus:** Cryptographic Inventory, Quantum Risk Assessment, and Post-Quantum Migration Planning
**Repository:** https://github.com/shalini04-12/CryptoGuard

---

*CryptoGuard is a prototype developed to explore cryptographic inventory analysis, quantum-risk awareness, and post-quantum migration planning. It is intended for demonstration and research purposes, not as a replacement for a formal cryptographic security assessment.*
