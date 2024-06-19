import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
def load_data():
    return pd.read_csv('support_tickets_clean.csv', parse_dates=['Creation Date', 'Resolution Date'])

# Generate the data
df = load_data()

# Set page config
st.set_page_config(page_title="Support Ticket Dashboard", page_icon=":bar_chart:", layout="wide")

# Title and description
st.title("Support Ticket Dashboard")
st.markdown("""
This dashboard provides insights into support ticket data, represents data into graphics to
            understand situation in couple of seconds
""")

# Data preview
st.subheader("Data Preview")
st.dataframe(df.head(15))


# Tickets by Status
st.subheader("Tickets by Status")
status_count = df['Status'].value_counts().reset_index()
status_count.columns = ['Status', 'Count']
fig = px.pie(status_count, values='Count', names='Status', title='It shows overall status of the tickets')
st.plotly_chart(fig)

# Tickets by Priority
st.subheader("Tickets by Priority")
priority_count = df['Priority'].value_counts().reset_index()
priority_count.columns = ['Priority', 'Count']
fig = px.bar(priority_count, x='Priority', y='Count', title='Priority set by the managers', color='Priority')
st.plotly_chart(fig)

# Resolution times
st.subheader("Resolution Times")
df['Resolution Time'] = (df['Resolution Date'] - df['Creation Date']).dt.days
resolution_times = df[df['Status'] == 'Closed']['Resolution Time'].dropna()
fig = px.histogram(resolution_times, nbins=20, title='Resolution Times gives the performance of the team')
st.plotly_chart(fig)

# Correlation heatmap
st.subheader("Correlation Heatmap")
numeric_df = df.select_dtypes(include=[np.number])
correlation = numeric_df.corr()
fig, ax = plt.subplots()
sns.heatmap(correlation, ax=ax, annot=True, cmap='coolwarm')
st.pyplot(fig)

# Resolution Time by Priority
st.subheader("Resolution Time by Priority")
priority_resolution_time = df[df['Status'] == 'Closed'].groupby('Priority')['Resolution Time'].mean().reset_index()
fig = px.bar(priority_resolution_time, x='Priority', y='Resolution Time', title='Average Resolution Time by Priority', color='Priority')
st.plotly_chart(fig)

# Tickets over Time (Line Chart)
st.subheader("Tickets over Time")
tickets_over_time = df.groupby(df['Creation Date'].dt.to_period('M')).size().reset_index(name='Count')
tickets_over_time['Creation Date'] = tickets_over_time['Creation Date'].dt.to_timestamp()
fig = px.line(tickets_over_time, x='Creation Date', y='Count', title='Date wise ticket and their count')
st.plotly_chart(fig)

st.divider()

# Contact Info
st.subheader("Contact Us")
st.write("**Mobile:** +92 333 6611988")
st.write("**Email:** uzairrajput100@gmail.com")

st.divider()
