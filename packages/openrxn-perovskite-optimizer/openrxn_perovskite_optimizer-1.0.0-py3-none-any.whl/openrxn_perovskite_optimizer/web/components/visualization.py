import streamlit as st
import plotly.express as px
import pandas as pd

def plot_property(df: pd.DataFrame, property_name: str):
    fig = px.scatter(df, x="composition", y=property_name, title=f"{property_name} vs. Composition")
    st.plotly_chart(fig)