import streamlit as st

def main():
    st.set_page_config(page_title="OpenRXN Perovskite Optimizer", layout="wide")
    st.title("🔬 OpenRXN Perovskite Optimizer")

    # Add dashboard components here
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Go to", ["Discovery", "Synthesis", "Optimization"])

    if page == "Discovery":
        st.header("Materials Discovery")
        # Add discovery components
    elif page == "Synthesis":
        st.header("Synthesis Planning")
        # Add synthesis components
    elif page == "Optimization":
        st.header("Process Optimization")
        # Add optimization components

if __name__ == "__main__":
    main()