import streamlit as st

def render(df, uploaded_file_bytes, uploaded_file_name):
    if df is not None:
        st.subheader("Dataset Overview")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📄 Filename", uploaded_file_name)
        c2.metric("📝 Rows", f"{len(df):,}")
        c3.metric("📊 Columns", len(df.columns))
        size_kb = (len(uploaded_file_bytes or b"")) / 1024
        c4.metric("💾 Size", f"{size_kb:.1f} KB")

        with st.expander("👀 View Data", expanded=True):
            st.dataframe(df.head(), use_container_width=True)

        if st.checkbox("📈 Show Data Statistics"):
            st.subheader("Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)
    else:
        st.info("Upload a CSV or Excel file from the sidebar to preview dataset.")