import streamlit as st
import time
import pandas as pd
from utils import send_to_api

def render(df, file_bytes, uploaded_file_name, api_url):
    st.subheader("Generate Predictions for Uploaded Dataset")
    if df is None:
        st.info("Upload a file first from the sidebar.")
    else:
        if st.button("🚀 Predict Batch"):
            with st.spinner("🤖 Generating predictions..."):
                start = time.time()
                data = send_to_api(file_bytes, uploaded_file_name, api_url)
                if data:
                    preds = data["data"]["predictions"]
                    st.session_state.results = pd.DataFrame(df.head(len(preds)))
                    st.session_state.results["Predicted Sales"] = preds
                    st.success(f"✅ Predictions generated in {time.time()-start:.2f}s!")

        if st.session_state.get("results") is not None:
            st.subheader("🎯 Predictions")
            st.dataframe(st.session_state.results, use_container_width=True, height=400)
            st.download_button(
                label="📥 Download Predictions (CSV)",
                data=st.session_state.results.to_csv(index=False),
                file_name="predictions.csv",
                mime="text/csv",
            )