import streamlit as st
import pandas as pd
from io import BytesIO
from utils import send_to_api

def render(api_url):
    st.subheader("Predict for Single Input")
    st.markdown("Enter feature values below to get a single prediction.")

    training_level = st.number_input("Training Level", min_value=0, max_value=5, value=3)
    work_experience = st.number_input("Work Experience (years)", min_value=0, max_value=20, value=5)
    salary = st.number_input("Salary", min_value=0, value=159148)
    level_of_education = st.selectbox("Level of Education", ["associate's degree", "some college", "high school", "bachelor's degree", "master's degree"])
    division = st.selectbox("Division", ["office supplies", "printers", "peripherals", "computer hardware", "computer software"])

    if st.button("🚀 Predict Single"):
        single_df = pd.DataFrame({
            "training level": [training_level],
            "work experience": [work_experience],
            "salary": [salary],
            "level of education": [level_of_education],
            "division": [division],
        })
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
