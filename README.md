---
# Databricks + OpenAI Lead Processing Pipeline

![License](https://img.shields.io/badge/license-MIT-green)
![Last Commit](https://img.shields.io/github/last-commit/visaoenhance/databricks-openai-lead-processing)
![Built By](https://img.shields.io/badge/built%20by-VisaoEnhance-blue)

This project demonstrates an automated lead cleaning and enrichment pipeline using **OpenAI GPT-4**, **Databricks**, and the **Salesforce Bulk API**.

It extracts raw leads from a CSV file, uses GPT-4 to clean and validate fields, and inserts them into Salesforce in batch.

---

## 🔍 Use Case
This is ideal for:
- CRM & Marketing teams managing bulk lead imports
- Consultants automating messy data cleanup
- AI-enhanced enrichment pipelines for customer data

---

## 📁 Folder Structure
```
databricks-openai-lead-processing/
├── notebooks/                  # Python notebook with full pipeline
├── sample_data/               # Sample leads CSV file
├── architecture_decisions.md  # Design justifications
├── README.md                  # This file
```

---

## 🧱 Tech Stack
- **Databricks (Python)**
- **OpenAI GPT-4 (chat.completions API)**
- **Salesforce API**
- **Pandas, Requests, Simple-Salesforce**

---

## 🔧 Setup
1. Upload your `leads_sample.csv` to the `sample_data/` directory.
2. Create a **Databricks Secret Scope** named `salesforce`:
   - `openai_api_key`
   - `username`, `password`, `security_token` for Salesforce
3. Install required Python packages:
   ```python
   %pip install simple-salesforce pandas requests openai
   ```

---

## ▶️ How It Works
1. Loads CSV data into a Pandas DataFrame
2. Sends each row to OpenAI for data cleanup
3. Transforms GPT output into Salesforce-ready format
4. Batches cleaned leads and inserts them via API
5. Logs status and verifies results

---

## 🧠 Diagram
```
+--------------------+
|   leads_sample.csv  |
+----------+---------+
           ↓
  +--------+--------+
  | Databricks Notebook |
  +--------+--------+
           ↓
   +-------+--------+
   | OpenAI GPT-4 API |
   +-------+--------+
           ↓
   +-------+--------+
   | Cleaned DataFrame |
   +-------+--------+
           ↓
   +-------+--------+
   | Salesforce Bulk API |
   +--------------------+
```

---

## 📜 License
[MIT](./LICENSE)

---

## 🔗 Related Projects
- CRM Data Model Blueprint → [View Repo](https://github.com/visaoenhance/crm-data-model-blueprint)
- Medium Post → *Coming Soon*
- YouTube Demo → *Coming Soon*

---

## ✍️ Author
Built by Emilio Taylor • [VisaoEnhance](https://www.visaoenhance.com) 