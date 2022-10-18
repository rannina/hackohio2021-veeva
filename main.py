import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import altair as alt
import json
with open("states.json") as json_file:
    states = json.load(json_file)

df = pd.read_csv("Prescriber_Data.csv", index_col=0).reset_index(drop=True)
df_copy = pd.read_csv("Prescriber_Data.csv", index_col=0).reset_index(drop=True)
#df = df.assign(pos_simple=df.pos.apply(lambda x: x.split("_")[0]))

# Header
st.title("Prescriber Data")
st.write(f"Veeva.")

st.subheader("Raw Dataset")
st.write(df)
#st.write(df.describe())
#count = 0

code = {'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'}
    


def sum_trx(df_row):
    total_trx = 0
    total_trx += df_row['TRx_Month_1']
    total_trx += df_row['TRx_Month_2']
    total_trx += df_row['TRx_Month_3']
    total_trx += df_row['TRx_Month_4']
    total_trx += df_row['TRx_Month_5']
    total_trx += df_row['TRx_Month_6']
    return total_trx

def sum_nrx(df_row):
    total_nrx = 0
    total_nrx += df_row['NRx_Month_1']
    total_nrx += df_row['NRx_Month_2']
    total_nrx += df_row['NRx_Month_3']
    total_nrx += df_row['NRx_Month_4']
    total_nrx += df_row['NRx_Month_5']
    total_nrx += df_row['NRx_Month_6']
    return total_nrx

def state_total_trx (s) :
    total_trx = 0
    for index, row in df.iterrows():
        if row['State'] == s :
            total_trx += sum_trx(row)
    return total_trx

def product_total_trx (p):
    total_trx = 0
    for index, row in df.iterrows():
        if row['Product'] == p :
            total_trx += sum_trx(row)
    return total_trx

def state_total_trx_product (s, p):
    total_trx = 0
    for index, row in df.iterrows():
        if row['State'] == s and row['Product'] == p:
            total_trx += sum_trx(row)
    return total_trx

def create_product_totalTRx_Graph(products):
    data = []
    for p in products:
        data.append(product_total_trx(p))
    fig = go.Figure([go.Bar(x=products, y=data)])
    fig.update_xaxes(title_text="Product")
    fig.update_yaxes(title_text="Total Number of Prescriptions")
    st.plotly_chart(fig)



def create_state_product_totalTRx_Graph(products):
    data = []
    for p in products:
        data.append(product_total_trx(p))
    fig = go.Figure([go.Bar(x=products, y=data)])
    fig.update_xaxes(title_text="Product")
    fig.update_yaxes(title_text="Total Number of Prescriptions")
    st.plotly_chart(fig)

products = []
for p in df['Product']:
    if p not in products:
        products.append(p)

def top_doctors_by_productTRx(df_data, p):
    doctors = []
    trx = []
    switch = 0
    for index, row in df_data.iterrows():
        if p == "All":
            switch = 1
        if row['Product'] == p or switch == 1:
            total_trx = sum_trx(row)
            if (len(doctors) == 0):
                doctors.append(row['first_name'] + ' ' + row['last_name'])
                trx.append(total_trx)
            elif (len(doctors) < 10 and len(doctors) != 0):
                for i in range(len(doctors)):
                    if total_trx > trx[i]:
                        doctors.insert(i, row['first_name'] + ' ' + row['last_name'])
                        trx.insert(i, total_trx)
                        break
                    else:
                        doctors.append(row['first_name'] + ' ' + row['last_name'])
                        trx.append(total_trx)
            elif (len(doctors) >= 10):
                for i in range(len(doctors)):
                    if total_trx > trx[i]:
                        doctors.insert(i, row['first_name'] + ' ' + row['last_name'])
                        trx.insert(i, total_trx)
                        del doctors[-1]
                        del trx[-1]
                        break
    df_doctors = pd.DataFrame({"Doctor": doctors, "Total TRx": trx})
    return df_doctors

def top_doctors_by_productNRx(df_data, p):
    doctors = []
    nrx = []
    switch = 0
    for index, row in df_data.iterrows():
        if p == "All":
            switch = 1
        if row['Product'] == p or switch == 1:
            total_nrx = sum_nrx(row)
            if (len(doctors) == 0):
                doctors.append(row['first_name'] + ' ' + row['last_name'])
                nrx.append(total_nrx)
            elif (len(doctors) < 10 and len(doctors) != 0):
                for i in range(len(doctors)):
                    if total_nrx > nrx[i]:
                        doctors.insert(i, row['first_name'] + ' ' + row['last_name'])
                        nrx.insert(i, total_nrx)
                        break
                    else:
                        doctors.append(row['first_name'] + ' ' + row['last_name'])
                        nrx.append(total_nrx)
            elif (len(doctors) >= 10):
                for i in range(len(doctors)):
                    if total_nrx > nrx[i]:
                        doctors.insert(i, row['first_name'] + ' ' + row['last_name'])
                        nrx.insert(i, total_nrx)
                        del doctors[-1]
                        del nrx[-1]
                        break
    df_doctors = pd.DataFrame({"Doctor": doctors, "Total NRx": nrx})
    return df_doctors

create_product_totalTRx_Graph(products)

products_copy = []
for p in products:
    products_copy.append(p)
products_copy.append("All")
product_option = st.selectbox("Product", options=products_copy, index=products.index("Cholecap"))

top_trx_doctors, top_nrx_doctors = st.columns(2)
with top_trx_doctors:
    st.write("Top Doctors for " + product_option + " by Total TRx")
    st.write(top_doctors_by_productTRx(df, product_option))
with top_nrx_doctors:
    st.write("Top Doctors for " + product_option + " by Total NRx")
    st.write(top_doctors_by_productNRx(df, product_option))

df_copy['Code'] = df['State'].map(code)


placeholder = []
for index, row in df_copy.iterrows():
        placeholder.append(sum_trx(row))

df_copy['Total_TRx'] = placeholder

#def create_totalTRx_column(df):
 #   for index, row in df.iterrows():
  #      placeholder.append(sum_trx(row))
   #     df_copy['Total_TRx'].append(placeholder[index])
    #print(df['Total_TRx'])

#create_totalTRx_column(df_copy)

state_names = {v: k for k, v in code.items()}


state_totaltrx = []

for i in range(51):
    state_totaltrx.append(0)

def merge_states(df):
    states = ["Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
    states_abbr = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    for index, row in df.iterrows():
        for i in range(len(states)):
            if row['State'] == states[i]:
                state_totaltrx[i] = state_totaltrx[i] + row['Total_TRx']            
    df_statetrx = pd.DataFrame({"State": states_abbr, "Total_TRx": state_totaltrx})
    return df_statetrx


fig = px.choropleth(merge_states(df_copy), geojson=states,
                    locations='State',
                    color='Total_TRx',
                    color_continuous_scale=[(0.00, "red"),   (0.25, "red"),
                                                     (0.25, "green"), (0.5, "green"),
                                                     (0.5, "blue"),  (0.75, "blue"),
                                                     (0.75, "purple"), (1.00, "purple")],
                    hover_name='State',
                    locationmode='USA-states',
                    
                    scope='usa')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig)
