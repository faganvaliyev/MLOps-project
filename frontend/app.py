import time
from io import BytesIO
import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="DM Office Sales Predictor",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💼",
)

# ----------------- Helper Functions -----------------
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
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
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

# ----------------- Main App -----------------
def main():
    # ----------------- Session State -----------------
    if "uploaded" not in st.session_state:
        st.session_state.uploaded = None
        st.session_state.file_bytes = None
        st.session_state.df = None
        st.session_state.results = None

    # ----------------- Sidebar -----------------
    with st.sidebar:
        st.title("💼 DM Office Sales Predictor")
        st.markdown("Upload your dataset or manually input features to get predictions.")
        st.markdown("---")
        api_url = "http://backend:8000/predict"

        uploaded = st.file_uploader(
            "📁 Choose your file",
            type=["csv", "xlsx", "xls"],
        )

        if uploaded is not None:
            if uploaded is not st.session_state.uploaded:
                st.session_state.uploaded = uploaded
                st.session_state.file_bytes = uploaded.getvalue()
                st.session_state.df = load_df_from_bytes(
                    st.session_state.file_bytes, uploaded.name
                )
                st.session_state.results = None
        else:
            st.session_state.uploaded = None
            st.session_state.file_bytes = None
            st.session_state.df = None
            st.session_state.results = None

    # ----------------- Tabs -----------------
    st.markdown("<h1 style='text-align:center;'>💼 DM Office Sales Predictor</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dataset Preview", 
        "🔮 Batch Predictions", 
        "🖊️ Single Prediction", 
        "📈 Visualizations"
    ])

    # ----------------- Tab 1: Dataset Preview -----------------
    with tab1:
        if st.session_state.df is not None:
            st.subheader("Dataset Overview")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("📄 Filename", st.session_state.uploaded.name)
            c2.metric("📝 Rows", f"{len(st.session_state.df):,}")
            c3.metric("📊 Columns", len(st.session_state.df.columns))
            size_kb = (len(st.session_state.file_bytes or b"")) / 1024
            c4.metric("💾 Size", f"{size_kb:.1f} KB")

            with st.expander("👀 View Data", expanded=True):
                st.dataframe(st.session_state.df.head(), use_container_width=True)

            if st.checkbox("📈 Show Data Statistics"):
                st.subheader("Statistical Summary")
                st.dataframe(st.session_state.df.describe(), use_container_width=True)
        else:
            st.info("Upload a CSV or Excel file from the sidebar to preview dataset.")

    # ----------------- Tab 2: Batch Predictions -----------------
    with tab2:
        st.subheader("Generate Predictions for Uploaded Dataset")
        if st.session_state.df is None:
            st.info("Upload a file first from the sidebar.")
        else:
            if st.button("🚀 Predict Batch"):
                with st.spinner("🤖 Generating predictions..."):
                    start = time.time()
                    data = send_to_api(
                        st.session_state.file_bytes,
                        st.session_state.uploaded.name,
                        api_url,
                    )
                    if data:
                        preds = data["data"]["predictions"]
                        st.session_state.results = pd.DataFrame(
                            st.session_state.df.head(len(preds))
                        )
                        st.session_state.results["Predicted Sales"] = preds
                        st.success(f"✅ Predictions generated in {time.time()-start:.2f}s!")

            if st.session_state.results is not None:
                st.subheader("🎯 Predictions")
                st.dataframe(st.session_state.results, use_container_width=True, height=400)
                st.download_button(
                    label="📥 Download Predictions (CSV)",
                    data=st.session_state.results.to_csv(index=False),
                    file_name="predictions.csv",
                    mime="text/csv",
                )

    # ----------------- Tab 3: Single Prediction -----------------
    with tab3:
        st.subheader("Predict for Single Input")
        st.markdown("Enter feature values below to get a single prediction.")

        training_level = st.number_input("Training Level", min_value=0, max_value=5, value=3)
        work_experience = st.number_input("Work Experience (years)", min_value=0, max_value=20, value=5)
        salary = st.number_input("Salary", min_value=0, value=159148)
        level_of_education = st.selectbox("Level of Education", ["associate's degree", "some college", "high school", "bachelor's degree", "master's degree"])
        division = st.selectbox("Division", ["office supplies", "printers", "peripherals", "computer hardware", "computer software"])

        if st.button("🚀 Predict Single"):
            single_df = pd.DataFrame(
                {
                    "training level": [training_level],
                    "work experience": [work_experience],
                    "salary": [salary],
                    "level of education": [level_of_education],
                    "division": [division],
                }
            )
            with st.spinner("🤖 Generating prediction..."):
                try:
                    buffer = BytesIO()
                    single_df.to_csv(buffer, index=False)
                    buffer.seek(0)
                    result = send_to_api(buffer.getvalue(), "single_input.csv", api_url)
                    if result and "data" in result:
                        pred = result["data"]["predictions"][0]
                        st.success(f"🎯 Predicted Sales: {pred:.2f}")
                except Exception as e:
                    st.error(f"Error generating prediction: {e}")

    # ----------------- Tab 4: Visualizations -----------------
    with tab4:
        st.subheader("Visualizations of Predictions")
        if st.session_state.results is None:
            st.info("Generate batch predictions first to visualize.")
        else:
            df_viz = st.session_state.results.copy()
            st.markdown("### 📊 Distribution of Predicted Sales")
            fig1 = px.histogram(df_viz, x="Predicted Sales", nbins=20, title="Predicted Sales Distribution")
            st.plotly_chart(fig1, use_container_width=True)

            st.markdown("### ⚡ Predicted Sales vs Features")
            numeric_features = ["training level", "work experience", "salary"]
            feature = st.selectbox("Select feature to visualize", numeric_features)
            fig2 = px.scatter(df_viz, x=feature, y="Predicted Sales", color=feature, size="Predicted Sales", title=f"Predicted Sales vs {feature}")
            st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### 📋 Summary Statistics")
            st.write(df_viz["Predicted Sales"].describe())

if __name__ == "__main__":
    main()