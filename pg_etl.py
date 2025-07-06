import pandas as pd
import requests

# ✅ Supabase credentials
SUPABASE_API_URL = "https://wdshpnyxruuvchxkmndh.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indkc2hwbnl4cnV1dmNoeGttbmRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE2NTQxMjEsImV4cCI6MjA2NzIzMDEyMX0.U2ObVljcxev5q5-yzsBCP0hVv5EAeunN85O3wnmd4s4"

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

    # Save to raw CSV
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
    except Exception as e:
        print(f"❌ Failed to read or transform CSV: {e}")

def main():
    data = extract_data()
    if data:
        transform_data()

if __name__ == "__main__":
    main()
