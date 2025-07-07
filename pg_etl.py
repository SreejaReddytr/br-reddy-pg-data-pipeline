import pandas as pd
import requests
import os

# ✅ Supabase credentials
SUPABASE_API_URL = os.getenv("SUPABASE_API_URL") or "https://wdshpnyxruuvchxkmndh.supabase.co"
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indkc2hwbnl4cnV1dmNoeGttbmRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE2NTQxMjEsImV4cCI6MjA2NzIzMDEyMX0.U2ObVljcxev5q5-yzsBCP0hVv5EAeunN85O3wnmd4s4"

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}"
}

def extract_data():
    print("📥 Fetching data from Supabase...")
    url = f"{SUPABASE_API_URL}/rest/v1/students?select=*"
    res = requests.get(url, headers=headers)
    print("✅ Status Code:", res.status_code)

    if res.status_code != 200:
        print("❌ Failed to fetch data:", res.text)
        return []

    data = res.json()
    if not data:
        print("⚠️ No data received from Supabase.")
    else:
        print(f"✅ Retrieved {len(data)} rows.")

    pd.DataFrame(data).to_csv("students_raw.csv", index=False)
    print("✅ Data saved to students_raw.csv")
    return data

def transform_data():
    try:
        df = pd.read_csv("students_raw.csv")
        df["aadhaar_uploaded"] = df["aadhaar_url"].notna() if "aadhaar_url" in df.columns else False
        df["registered_day"] = pd.to_datetime(df["created_at"], errors='coerce').dt.date if "created_at" in df.columns else None
        df.to_csv("students_clean.csv", index=False)
        print("✅ Data transformed and saved to students_clean.csv")
        return df
    except Exception as e:
        print(f"❌ Failed to transform data: {e}")
        return None

def upload_cleaned_data(df_clean):
    if df_clean is None:
        print("❌ No data to upload.")
        return

    print(f"📤 Uploading {len(df_clean)} cleaned records to Supabase...")

    # Only send columns that exist in Supabase schema
    allowed_columns = [
        "full_name", "contact_number", "room_number",
        "gmail_address", "college_name", "aadhaar_url", "created_at"
    ]

    if not all(col in df_clean.columns for col in allowed_columns):
        print("❌ Missing expected columns. Please check your DataFrame.")
        return

    df_clean = df_clean[allowed_columns]  # Filter to allowed columns

    url = f"{SUPABASE_API_URL}/rest/v1/students"
    for i, row in df_clean.iterrows():
        payload = row.to_dict()
        response = requests.post(url, json=payload, headers=headers)
        print(f"Row {i+1}: Status {response.status_code}")
        if response.status_code >= 300:
            print("❌ Error:", response.text)

def main():
    data = extract_data()
    if data:
        df_clean = transform_data()
        upload_cleaned_data(df_clean)

if __name__ == "__main__":
    main()
