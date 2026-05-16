# Hardware Asset Registry – QA/Test Engineering Project  
### End‑to‑End Data Quality • Security Compliance • Lifecycle Validation • Financial Analysis • Automated Reporting

This project simulates a real-world **QA/Test Engineer workflow** used in manufacturing, enterprise IT, and hardware lifecycle management.  
It validates a 50,000‑record hardware asset registry across **inventory, security, lifecycle, risk, and financial dimensions**, and produces automated reports, XML configs, dashboards, and documentation.

---

## 🚀 Project Features

### ✅ Automated Python Validation
- Uniqueness checks (`asset_id`, `asset_tag`, `serial_number`)
- Completeness checks for critical fields
- Lifecycle validation (purchase → warranty → EOL → EOS)
- Security posture checks:
  - Encryption
  - Antivirus & firewall
  - Patch compliance
  - TPM & Secure Boot
- Risk & vulnerability consistency
- Financial depreciation & residual value validation

### ✅ XML Configuration Generator
Creates structured XML for downstream systems (CMDB, monitoring, security scanners).

### ✅ One‑Click Test Execution (CMD)
Runs the entire validation + XML generation pipeline.

### ✅ Excel Dashboard
Includes:
- KPI cards  
- Status distribution  
- Classification distribution  
- Risk heatmaps  
- Financial summaries  

### ✅ Word Test Report
Executive‑ready QA report with findings, charts, and recommendations.

### ✅ PowerPoint Presentation
Stakeholder‑ready summary of insights and next steps.

---

## 📁 Folder Structure
HardwareAssetRegistry/
│
├── data/
│   └── hardware_asset_registry_50000.csv
│
├── scripts/
│   ├── validate_assets.py
│   └── generate_asset_xml.py
│
├── output/
│   ├── summary_metrics.xlsx
│   ├── status_distribution.xlsx
│   ├── classification_distribution.xlsx
│   ├── issues_*.xlsx
│   └── asset_inventory_config.xml
│
├── docs/
│   ├── Test Plan
│   ├── Test Report
│   ├── PowerPoint Presentation
│   └── Excel Dashboard
│
└── run_asset_tests.cmd


---

## 📊 Outputs

- Automated issue files (`issues_*.xlsx`)
- Summary metrics
- Status & classification distributions
- XML configuration file
- Excel dashboard
- Word report
- PowerPoint deck

---

## 🛠️ Tech Stack

- Python (pandas, lxml, openpyxl)
- Excel
- Word
- PowerPoint
- CMD automation
- YAML CI/CD (optional)
- Power BI (optional)

---
                ┌────────────────────────┐
                │  Hardware Asset CSV    │
                │  (50,000 records)      │
                └──────────┬─────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │  Python Validation      │
                │  validate_assets.py     │
                └──────────┬─────────────┘
                           │
     ┌─────────────────────┼────────────────────────┐
     ▼                     ▼                        ▼
Issues Excel Files   Summary Metrics         Status/Class Dist.
(issues_*.xlsx)      (summary.xlsx)          (charts.xlsx)

                           │
                           ▼
                ┌────────────────────────┐
                │  XML Generator         │
                │  generate_asset_xml.py │
                └──────────┬─────────────┘
                           │
                           ▼
                asset_inventory_config.xml

                           │
                           ▼
                ┌────────────────────────┐
                │  Excel Dashboard        │
                └────────────────────────┘

                           │
                           ▼
                ┌────────────────────────┐
                │  Word Test Report       │
                └────────────────────────┘

                           │
                           ▼
                ┌────────────────────────┐
                │ PowerPoint Presentation │
                └────────────────────────┘
<p align="center">
  <img src="https://img.shields.io/badge/Project-Hardware%20Asset%20Registry-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Automation-QA%20Testing-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Data%20Quality-Validation-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Security-Compliance-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Excel-Dashboard-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white" />
  <img src="https://img.shields.io/badge/Word-Report-2B579A?style=for-the-badge&logo=microsoft-word&logoColor=white" />
  <img src="https://img.shields.io/badge/PowerPoint-Presentation-B7472A?style=for-the-badge&logo=microsoft-powerpoint&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
</p>



## 📌 Author
Madhu



