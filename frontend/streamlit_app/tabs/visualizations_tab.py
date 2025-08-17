import streamlit as st
import plotly.express as px

def render():
    st.subheader("Visualizations of Predictions")
    if st.session_state.get("results") is None:
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