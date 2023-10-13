import streamlit as st
import pandas as pd

st.title('Moneycontrol.com SWOT')

st.markdown("""
This app show the SWOT (Strength, Weakness, Opportunity and Thread) details specified by Moneycontrol.com.
""")


@st.cache_data
def load_data():
    return pd.read_csv('MoneyControlSWOT10Sep2023.csv')


df = load_data()
strings = ['MCEssential', 'Strengths', 'Weaknesses', 'Opportunities', 'Threats']
st.sidebar.markdown("Specify SWOT preferred order to sort companies.")
sorted_swot = st.sidebar.multiselect("Arrange the SWOT:", strings, strings)
sorted_df = df.sort_values(by=sorted_swot, ascending=False)

display_column = ['Company'] + sorted_swot + ['Sector', 'Link']
company_name = st.text_input('Show specific Company Name')
st.header('Display Companies')

if company_name:
    filtered_df = sorted_df[sorted_df['Company'].str.contains(company_name, case=False, regex=True)]
else:
    filtered_df = sorted_df

st.dataframe(filtered_df[display_column])