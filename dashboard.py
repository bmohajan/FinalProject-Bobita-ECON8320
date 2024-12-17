import streamlit as st
import pandas as pd
import plotly.express as px

st.write("# Bobita Mohajan  ECON 8320 Semester Project")
st.markdown(
        """
       This dashboard allows you to examine key metrics related to Unemployment Rate, Total Nonfarm Employees, Private Sector Employees.

    **INSTRUCTIONS:**
    - Choose a time range using the dropdown menus, and the line graphs will display the selected data.
    - Each graph can be zoomed in to explore details further. Double-click to exit zoomed view.
    - You can view the specific data values by moving your mouse cursor over any point on the lines in the charts.
    
    The metrics included in this demonstration are:
    - **Unemployment Rate** (LNS14000000): Percentage of unemployed individuals in the labor force.
    - **Total Nonfarm Employees** (CES0000000001): Total number of employed individuals.
    - **Private Sector Employees** (CES0500000002): Total employees in the private sector.

    **Note:** Data is sourced from the U.S. Bureau of Labor Statistics, and variations may exist for specific years due to changes in reporting or categorization.
    """
    )

df= pd.read_csv("data.csv")

df['timestamp'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY=1))
print(df.head())

df_unemployment = df[df["series_id"] == "LNS14000000"]
start_years = sorted(df_unemployment["Year"].unique())
st.write("### Unemployment rate")
option_start_year = st.selectbox(label="Start Year", options=start_years, key="start_year_unemployment")
end_years = [year for year in start_years if year >option_start_year]
option_end_year = st.selectbox(label="End Year", options=end_years, key="end_year_unemployment")


filtered_data = df_unemployment[(df_unemployment.Year >= option_start_year )& (df_unemployment.Year <= option_end_year )]
fig_unemployment = px.line(filtered_data, x="timestamp", y="Value", title=f"Unemployment Rate from {option_start_year} to {option_end_year}")
st.plotly_chart(fig_unemployment)

df_employees = df[df["series_id"] == "CES0000000001"]
start_years = sorted(df_employees["Year"].unique())
st.write("### Employees")
option_start_year = st.selectbox(label="Start Year", options=start_years, key="start_year_employees")
end_years = [year for year in start_years if year >option_start_year]
option_end_year = st.selectbox(label="End Year", options=end_years,  key="end_year_employees")


filtered_data = df_employees[(df_employees.Year >= option_start_year )& (df_employees.Year <= option_end_year )]
fig_employees = px.line(filtered_data, x="timestamp", y="Value",
                        title=f"employees from {option_start_year} to {option_end_year}")
st.plotly_chart(fig_employees)

df_private_employees = df[df["series_id"] == "CES0500000002"]
start_years = sorted(df_private_employees["Year"].unique())
st.write("### Private Employees")
option_start_year = st.selectbox(label="Start Year", options=start_years, key="start_year_private_employees")
end_years = [year for year in start_years if year >option_start_year]
option_end_year = st.selectbox(label="End Year", options=end_years,  key="end_year_private_employees")


filtered_data = df_private_employees[(df_private_employees.Year >= option_start_year )& (df_private_employees.Year <= option_end_year )]
fig_private_employees = px.line(filtered_data, x="timestamp", y="Value",
                        title=f"private_employees from {option_start_year} to {option_end_year}")
st.plotly_chart(fig_private_employees)