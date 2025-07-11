import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="🌐 Global Digital Capability Dashboard")

gdb_data = pd.read_csv("digital_government.csv")
gdb_data_internet = pd.read_csv("internet_access.csv")

# Sidebar Filters
st.sidebar.header("🧭 Filters")
continents = gdb_data['continent'].dropna().astype(str).unique()
continent_filter = st.sidebar.selectbox("🌍 Continent", options=["All"] + sorted(continents))
filtered_data = gdb_data[gdb_data['continent'] == continent_filter] if continent_filter != "All" else gdb_data

# Main Title
st.markdown("""
    <h1 style='text-align: center;'>🌐 Global Digital Capability Dashboard</h1>
    <hr />
""", unsafe_allow_html=True)

# KPI Header
col1, col2, col3, col4 = st.columns(4)
col1.metric("🌎 Total Countries", gdb_data['country'].nunique())
col2.metric("🗺️ Filtered Countries", filtered_data['country'].nunique())
col3.metric("📊 Avg. Overall Score", f"{filtered_data['overall_score'].mean():.2f}")
col4.metric("🧱 Avg. Data Infrastructure", f"{filtered_data['score_by_action_area'].mean():.2f}")

# Map
st.subheader("🗺️ Digital Capability Map")
map_fig = px.scatter_geo(
    filtered_data,
    locations="country",
    locationmode="country names",
    color="overall_score",
    hover_name="country",
    size="overall_score",
    size_max=20,
    projection="natural earth",
    color_continuous_scale="Blues"
)
map_fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        showland=True,
        landcolor="LightGray"
    ),
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)
st.plotly_chart(map_fig, use_container_width=True)

# Top and Lowest Performers
st.subheader("🏅 Notable Performers")
highest_score_row = filtered_data.loc[filtered_data['overall_score'].idxmax()]
lowest_score_row = filtered_data.loc[filtered_data['overall_score'].idxmin()]

col_high, col_low = st.columns(2)
with col_high:
    st.markdown(f"**🥇 Highest Scoring Country: {highest_score_row['country']}**")
    st.markdown(f"""
    - 🌐 Overall Score: {highest_score_row['overall_score']}
    - 🏛️ Digital Government: {highest_score_row['score_by_indicator']}
    - 🧱 Data Infrastructure: {highest_score_row['score_by_action_area']}
    - ⚖️ Governance Foundation: {highest_score_row['score_by_cluster']}
    """)
with col_low:
    st.markdown(f"**🚨 Lowest Scoring Country: {lowest_score_row['country']}**")
    st.markdown(f"""
    - 🌐 Overall Score: {lowest_score_row['overall_score']}
    - 🏛️ Digital Government: {lowest_score_row['score_by_indicator']}
    - 🧱 Data Infrastructure: {lowest_score_row['score_by_action_area']}
    - ⚖️ Governance Foundation: {lowest_score_row['score_by_cluster']}
    """)

# Country Score Table
st.subheader("📋 Country Scores")
table_df = (
    filtered_data[[
        'country', 'score_by_action_area', 'score_by_indicator', 'score_by_cluster'
    ]]
    .rename(columns={
        'country': 'Country',
        'score_by_action_area': 'Data Infrastructure',
        'score_by_indicator': 'Digital Government',
        'score_by_cluster': 'Governance Foundation'
    })
    .sort_values(by='Data Infrastructure', ascending=False)
    .reset_index(drop=True)
)
st.dataframe(table_df, use_container_width=True)

# Charts
c1, c2 = st.columns(2)

# Bar Chart: Average Overall Score by Country
with c1:
    avg_score = filtered_data.groupby('country')['overall_score'].mean().sort_values(ascending=False).reset_index()
    bar_fig = px.bar(
        avg_score, x='country', y='overall_score',
        title="📊 Average Overall Score by Country",
        color='overall_score',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(bar_fig, use_container_width=True)

# Stacked Bar Chart: Digital Capability
with c2:
    stacked_df = filtered_data.groupby('country').agg({
        'score_by_action_area': 'mean',
        'score_by_indicator': 'mean',
        'score_by_cluster': 'mean'
    }).reset_index()
    stacked_fig = go.Figure(data=[
        go.Bar(name='Data Infrastructure', x=stacked_df['country'], y=stacked_df['score_by_action_area'], marker_color='#3399FF'),
        go.Bar(name='Digital Government', x=stacked_df['country'], y=stacked_df['score_by_indicator'], marker_color='#0066CC'),
        go.Bar(name='Governance Foundation', x=stacked_df['country'], y=stacked_df['score_by_cluster'], marker_color='#003366')
    ])
    stacked_fig.update_layout(barmode='stack', title='📊 Digital Capability Scores (Stacked)')
    st.plotly_chart(stacked_fig, use_container_width=True)

# Additional Charts
c3, c4 = st.columns(2)

# Horizontal Bar: Data Infrastructure by Continent
with c3:
    continent_df = gdb_data.dropna(subset=['continent']).groupby('continent')['score_by_action_area'].mean().reset_index()
    continent_bar = px.bar(
        continent_df, x='score_by_action_area', y='continent',
        orientation='h',
        title="🧱 Avg. Data Infrastructure by Continent",
        labels={'score_by_action_area': 'Average Score'},
        color='score_by_action_area',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(continent_bar, use_container_width=True)

# Scatter Plot
with c4:
    scatter_fig = px.scatter(
        filtered_data,
        x='score_by_action_area',
        y='score_by_indicator',
        hover_name='country',
        title="🔎 Data Infrastructure vs Digital Government",
        labels={
            'score_by_action_area': 'Data Infrastructure Score',
            'score_by_indicator': 'Digital Government Score'
        },
        color='overall_score',
        color_continuous_scale='Blues'
    )
    st.plotly_chart(scatter_fig, use_container_width=True)

# Internet Access Section
filtered_data_internet = gdb_data_internet[gdb_data_internet['continent'] == continent_filter] if continent_filter != "All" else gdb_data_internet

col_map, col_bar = st.columns(2)

with col_map:
    st.subheader("📡 Internet Access Map by Country")
    map_fig_internet = px.scatter_geo(
        filtered_data_internet,
        locations="country",
        title="📊 Internet Access Map by Country",
        locationmode="country names",
        color="score_by_indicator",
        hover_name="country",
        size="score_by_indicator",
        size_max=20,
        projection="natural earth",
        color_continuous_scale="Blues"
    )
    map_fig_internet.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            showland=True,
            landcolor="LightGray"
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    st.plotly_chart(map_fig_internet, use_container_width=True)

with col_bar:
    internet_continent_df = (
        filtered_data_internet
        .dropna(subset=['continent'])
        .groupby('continent')['score_by_indicator']
        .mean()
        .reset_index()
    )
    internet_bar_fig = px.bar(
        internet_continent_df,
        x='score_by_indicator',
        y='continent',
        orientation='h',
        color='score_by_indicator',
        color_continuous_scale='Blues',
        labels={'score_by_indicator': 'Avg. Internet Score', 'continent': 'Continent'}
    )
    st.plotly_chart(internet_bar_fig, use_container_width=True)
