import streamlit as st
import pandas as pd
import plotly.express as px

# Load your data
df = pd.read_csv("PSales.csv")

# UI Header
st.title("📊 Product Sales Dashboard")

# Dropdown for selecting categories
categories = df['Category'].unique()
selected_categories = st.multiselect("Select Category:", categories, default=list(categories))

# Filter data
filtered_df = df[df['Category'].isin(selected_categories)]

# Bar Chart: Sales by SubCategory
bar_fig = px.bar(
    filtered_df.groupby('SubCategory')['Sales'].sum().reset_index(),
    x='SubCategory',
    y='Sales',
    title='Sales by SubCategory'
)
st.plotly_chart(bar_fig)

# Pie Chart: Profit by SubCategory
pie_fig = px.pie(
    filtered_df.groupby('SubCategory')['Profit'].sum().reset_index(),
    names='SubCategory',
    values='Profit',
    title='Profit by SubCategory'
)
st.plotly_chart(pie_fig)

# Sunburst Chart: Discount Breakdown
sunburst_fig = px.sunburst(
    filtered_df,
    path=['Category', 'SubCategory', 'Discount'],
    values='Discount',
    title='Discount Breakdown'
)
st.plotly_chart(sunburst_fig)
