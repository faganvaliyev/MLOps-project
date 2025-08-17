import streamlit as st
from config import API_URL
from utils import load_df_from_bytes
from tabs import dataset_tab, batch_tab, single_tab, visualizations_tab

def main():
    # Session State 
    if "uploaded" not in st.session_state:
        st.session_state.uploaded = None
        st.session_state.file_bytes = None
        st.session_state.df = None
        st.session_state.results = None

    # Sidebar 
    with st.sidebar:
        st.title("Data Upload")
        st.markdown("Upload your dataset or manually input features to get predictions.")
        st.markdown("---")
        uploaded = st.file_uploader("📁 Choose your file", type=["csv", "xlsx", "xls"])
        if uploaded is not None:
            if uploaded is not st.session_state.uploaded:
                st.session_state.uploaded = uploaded
                st.session_state.file_bytes = uploaded.getvalue()
                st.session_state.df = load_df_from_bytes(st.session_state.file_bytes, uploaded.name)
                st.session_state.results = None
        else:
            st.session_state.uploaded = None
            st.session_state.file_bytes = None
            st.session_state.df = None
            st.session_state.results = None

    #  Tabs 
    st.markdown("<h1 style='text-align:center;'>💼 DM Office Sales Predictor</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dataset Preview", 
        "🔮 Batch Predictions", 
        "🖊️ Single Prediction", 
        "📈 Visualizations"
    ])

    with tab1:
        dataset_tab.render(st.session_state.df, st.session_state.file_bytes, st.session_state.uploaded.name if st.session_state.uploaded else "")
    with tab2:
        batch_tab.render(st.session_state.df, st.session_state.file_bytes, st.session_state.uploaded.name if st.session_state.uploaded else "", API_URL)
    with tab3:
        single_tab.render(API_URL)
    with tab4:
        visualizations_tab.render()

if __name__ == "__main__":
    main()