---
# 🧠 Architecture Decisions – Databricks + OpenAI Lead Processing

This document explains the key architectural choices and trade-offs made in the design of this pipeline.

---

## 🔹 1. Why Use Databricks?
- Databricks offers scalable notebooks and integration with distributed compute.
- It's ideal for batch-style pipelines involving external APIs, like OpenAI or Salesforce.
- Secrets management is available for secure API credential storage.

## 🔹 2. Why OpenAI GPT-4?
- GPT-4's natural language capabilities are ideal for interpreting and cleaning user-submitted text.
- It can infer missing data, fix name formatting, normalize phone numbers, and guess emails — tasks that traditional rules-based cleaning cannot handle effectively.

## 🔹 3. Why Simple-Salesforce?
- Simple, proven Python package for Salesforce REST/Bulk APIs.
- Allows authenticated inserts and SOQL queries with minimal overhead.

---

## 🔸 4. Secrets Handling
- API keys (Salesforce + OpenAI) are stored securely in a Databricks Secret Scope (`salesforce`).
- These are fetched at runtime using `dbutils.secrets.get()`.
- Avoids hardcoding credentials or storing them in version control.

## 🔸 5. Cleaning Strategy
- Each row is sent to GPT-4 with an explicit prompt.
- Output is enforced to be JSON via role instructions.
- Results are parsed and validated before API submission.

---

## 🔸 6. Batch Insertion
- Records are chunked into batches of 200 (Salesforce Bulk API standard limit).
- Insertions are made using `requests.post` with valid Salesforce session tokens.

## 🔸 7. Observability
- Key steps print preview summaries for debugging:
  - Incoming vs cleaned records
  - API responses
  - DataFrame column mapping validations

---

## 💡 Future Considerations
- Add retry logic or OpenAI error handling for malformed JSON
- Support async processing for high-volume jobs
- Expand to include additional enrichment sources (Clearbit, ZoomInfo, etc)

---

Built by Emilio Taylor • [VisaoEnhance](https://www.visaoenhance.com) 