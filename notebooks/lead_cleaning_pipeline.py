# Databricks + OpenAI Lead Processing Pipeline (Sanitized)

# Required Libraries
%pip install simple-salesforce pandas requests openai

import pandas as pd
import openai
from simple_salesforce import Salesforce
import numpy as np
import json
import os

# Fetch secrets from Databricks secrets scope (assumed pre-configured)
OPENAI_API_KEY = dbutils.secrets.get("salesforce", "openai_api_key")
SF_USERNAME = dbutils.secrets.get("salesforce", "username")
SF_PASSWORD = dbutils.secrets.get("salesforce", "password")
SF_SECURITY_TOKEN = dbutils.secrets.get("salesforce", "security_token")

# Configure OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def clean_lead_data(lead):
    prompt = f"""
    You are an AI assistant that processes and cleans lead data before inserting into Salesforce.
    Given the following lead record, correct any missing or incorrectly formatted fields:

    {json.dumps(lead)}

    - Capitalize names correctly.
    - Infer missing email using company domain if absent.
    - Format phone number as (XXX) XXX-XXXX.
    - Standardize 'lead_source' to one of: ['Web', 'Referral', 'Event', 'Cold Call', 'Other'].
    Return only valid JSON.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI that returns only valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )
    try:
        return json.loads(response.choices[0].message.content.strip())
    except json.JSONDecodeError:
        return {}

# Load CSV (replace with your actual path)
df = pd.read_csv("sample_data/leads_sample.csv")

# Clean the data
df["cleaned_leads"] = df.apply(lambda x: clean_lead_data(x.to_dict()), axis=1)
cleaned_df = pd.DataFrame(df["cleaned_leads"].tolist())

# Prepare cleaned data for Salesforce
cleaned_df.columns = cleaned_df.columns.str.strip().str.casefold()
column_mapping = {
    "first_name": "FirstName",
    "last_name": "LastName",
    "email": "Email",
    "company": "Company",
    "lead_source": "LeadSource",
    "phone": "Phone"
}
cleaned_df = cleaned_df.rename(columns=column_mapping)
valid_fields = ["FirstName", "LastName", "Email", "Company", "Phone", "LeadSource"]
cleaned_df = cleaned_df[valid_fields]
cleaned_df = cleaned_df.replace({np.nan: None})
cleaned_leads = cleaned_df.to_dict(orient="records")

# Connect to Salesforce
sf = Salesforce(username=SF_USERNAME, password=SF_PASSWORD, security_token=SF_SECURITY_TOKEN)
bulk_url = f"https://{sf.sf_instance}/services/data/v60.0/composite/sobjects"

# Push to Salesforce
def insert_leads(batch):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {sf.session_id}"
    }
    payload = json.dumps({
        "records": [{"attributes": {"type": "Lead"}, **lead} for lead in batch]
    })
    response = requests.post(bulk_url, headers=headers, data=payload)
    print(response.status_code, response.text)

batch_size = 200
for i in range(0, len(cleaned_leads), batch_size):
    insert_leads(cleaned_leads[i:i+batch_size])
