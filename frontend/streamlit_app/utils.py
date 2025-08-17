from io import BytesIO
import pandas as pd
import requests
import streamlit as st

def detect_mime(filename: str) -> str:
    name = (filename or "").lower()
    if name.endswith(".csv"):
        return "text/csv"
    if name.endswith(".xlsx"):
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if name.endswith(".xls"):
        return "application/vnd.ms-excel"
    return "application/octet-stream"

def load_df_from_bytes(file_bytes: bytes, filename: str) -> pd.DataFrame | None:
    try:
        bio = BytesIO(file_bytes)
        if filename.lower().endswith(".csv"):
            return pd.read_csv(bio)
        elif filename.lower().endswith((".xlsx", ".xls")):
            return pd.read_excel(bio)
        else:
            st.error("Unsupported file format.")
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def send_to_api(file_bytes: bytes, filename: str, api_url: str) -> dict | None:
    try:
        files = {"file": (filename, file_bytes, detect_mime(filename))}
        resp = requests.post(api_url, files=files, timeout=60)
        if resp.headers.get("content-type", "").startswith("application/json"):
            data = resp.json()
        else:
            st.error(f"Unexpected response from API (status {resp.status_code})")
            return None
        if resp.status_code == 200 and data.get("status") == "success":
            return data
        else:
            st.error(f"API Error {resp.status_code}: {data.get('detail', data)}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Network error while calling API: {e}")
        return None