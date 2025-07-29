# TOPSISX 📊

[![PyPI Version](https://img.shields.io/pypi/v/topsisx.svg)](https://pypi.org/project/topsisx/)
[![Downloads](https://static.pepy.tech/badge/topsisx)](https://pepy.tech/project/topsisx)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/yourusername/topsisx/blob/main/LICENSE)

---

TOPSISX is a Python library for multi-criteria decision-making (MCDM) using methods like **TOPSIS**, **AHP**, **Entropy Weighting**, and **VIKOR**. It also supports PDF report generation and visualizations.

---

## 🚀 Features
- 📈 **TOPSIS**: Rank alternatives based on weighted criteria.
- 📊 **AHP**: Calculate weights using Analytic Hierarchy Process.
- 📋 **Entropy Weighting**: Objective weight calculation.
- 📑 **PDF Reports**: Generate professional reports of results.
- 🖼️ **Visualizations**: Plot graphs for better insights.

---

## 📦 Installation

Install the package from PyPI:

```bash
pip install topsisx

⚡ Quick Start
Here’s how you can use topsisx in your project:

python
Copy
Edit
from topsisx.topsis import topsis

# Sample data
data = [
    [250, 16, 12, 5],
    [200, 16, 8, 3],
    [300, 32, 16, 4],
    [275, 32, 8, 4],
    [225, 16, 16, 2]
]

weights = [0.25, 0.25, 0.25, 0.25]
impacts = ['+', '+', '-', '+']

ranked = topsis(data, weights, impacts)
print(ranked)
📖 Documentation
Go to topsisx.readthedocs.io (Coming Soon 🚧)

👨‍💻 Contributing
We welcome contributions! Please open an issue or pull request on GitHub.
https://github.com/SuvitKumar003/ranklib

📝 License
This project is licensed under the MIT License.



