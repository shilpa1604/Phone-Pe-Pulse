import streamlit as st
import pandas as pd
import pymysql
import json
import numpy as np
from streamlit_option_menu import option_menu

import plotly.express as px

# Creating connection to MySQL PhonePe database


user = 'root'
password = 'shilpa1642'
host = 'localhost'
database = 'PhonePe'

connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=database)

cursor = connection.cursor()

st.set_page_config(page_title="Phonepe Pulse Data Visualization | By Jafar Hussain",

                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This dashboard app is created by *Jafar Hussain*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

st.markdown("""
<style>
    [data-testid=stAppViewContainer] {
        background-color: #fdf5e6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(""" <style> .font {
font-size:50px ; font-family: 'Cooper Black'; color: black;background-color:#fdf5e6} 
</style> """, unsafe_allow_html=True)

st.title(':violet[**_PhonePe Pulse_**]')

st.sidebar.header("India")
selected = option_menu(None, ["Overall Data", "Top Data", "Explore Data"],

                       menu_icon="cast", default_index=0, orientation="horizontal",
                       styles={
                           "container": {"padding": "0!important", "background-color": "#AC9474"},
                           "icon": {"color": "orange", "font-size": "25px"},
                           "nav-link": {"font-size": "25px", "text-align": "left", "margin": "0px",
                                        "--hover-color": "#eee"},
                           "nav-link-selected": {"background-color": "violet"},
                       })

with st.sidebar:
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #AC9474;
        }
    </style>
    """, unsafe_allow_html=True)
    st.header(':black[Welcome to PhonePe Pulse]')

    view = st.selectbox("What data would you like to view?", ("Transactions", "Users"))

    year = st.selectbox('Year', range(2018, 2024))

    quarter = st.selectbox('Quarter', range(1, 5))

    st.divider()

    button_op = st.button("View")

if selected == 'Overall Data':
    st.header(view)

    if view == 'Transactions':
        col1, col2, col3 = st.columns(3, gap='medium')

        with col1:
            st.subheader(":blue[**All phone transactions**]")
            cursor.execute(
                f'''select sum(Transaction_count) from PhonePe.transactions where year ={year} and quarter={quarter}''')

            i = cursor.fetchall()


            total_transactions = f'<p style="font-family:Serif; color:black; font-size: 20px;">{list(i[0])[0]}</p>'
            st.markdown(total_transactions, unsafe_allow_html=True)
            total_transactions = list(i[0])[0]

        with col2:
            st.subheader(":blue[**Total Payment Value (INR)**]")
            cursor.execute(
                f'''select sum(Transaction_Value) from PhonePe.transactions where year ={year} and quarter={quarter}''')
            i = cursor.fetchall()


            total_transactions_value = f'<p style="font-family:Serif; color:black; font-size: 20px;">{list(i[0])[0]}</p>'
            st.markdown(total_transactions_value, unsafe_allow_html=True)
            total_transactions_value = list(i[0])[0]


        with col3:
            st.subheader(":blue[**Avg. Transaction Value (INR)**]")
            avg_transaction_value = int(np.divide(int(total_transactions_value), int(total_transactions)))


            avg_transaction_value = f'<p style="font-family:Serif; color:black; font-size: 20px;">{avg_transaction_value}</p>'
            st.markdown(avg_transaction_value, unsafe_allow_html=True)

        st.divider()
        st.header('Categories')
        cursor.execute(
            f'''select distinct transaction_category,Transaction_count from PhonePe.transactions where year ={year} and quarter={quarter}''')
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction Category', 'Transaction Count'])
        fig = px.pie(df, values='Transaction Count',
                     names='Transaction Category',

                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Transaction Count'],
                     labels={'Transaction Count': 'Transaction Count'})
        fig.update_layout(autosize=False,
                          width=500,
                          height=500,
                          margin=dict(
                              l=50,
                              r=50,
                              b=100,
                              t=0,
                              pad=4
                          ),
                          paper_bgcolor="#fdf5e6")

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)


    elif view == "Users":
        st.subheader(f"User Information till till Q{quarter} {year} ")
        cursor.execute(
            f'''select distinct Registered_Users from PhonePe.users where year ={year} and quarter={quarter} union 
            select distinct App_Opens from PhonePe.users where year ={year} and quarter={quarter}''')
        df = pd.DataFrame(cursor.fetchall(), columns=['Users'], index=['Registered User', 'AppOpens'])
        fig = px.pie(df, values='Users',
                     names=['Registered User', 'AppOpens'],

                     color_discrete_sequence=px.colors.sequential.Agsunset,
                     hover_data=['Users']

                     )
        fig.update_layout(autosize=False,
                          width=500,
                          height=500,
                          margin=dict(
                              l=50,
                              r=50,
                              b=100,
                              t=0,
                              pad=4
                          ),
                          paper_bgcolor="#fdf5e6")

        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)



elif selected == 'Top Data':
    if view == 'Transactions':
        st.header("Transactions")

        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            st.subheader("Top 10 States")
            cursor.execute(
                f'''select distinct state,transaction_value from PhonePe.top_state_transactions where year ={year} and quarter={quarter}''')
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction Amount'])
            fig = px.pie(df, values='Transaction Amount',
                         names='State',

                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['State'],
                         labels={'Transaction Amount': 'Transaction Amount'}
                         )
            fig.update_layout(autosize=False,
                              width=450,
                              height=500,
                              margin=dict(
                                  l=50,
                                  r=90,
                                  b=100,
                                  t=0,
                                  pad=4
                              ),
                              paper_bgcolor="#fdf5e6")

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        with col2:
            st.subheader("Top 10 Districts")
            cursor.execute(
                f'''select district,transaction_value from (select distinct district,transaction_value,dense_rank() over(order by transaction_value asc) as rnk
  from PhonePe.top_district_transactions where year ={year} and quarter={quarter})a
where a.rnk<=10''')
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transaction Amount'])
            fig = px.pie(df, values='Transaction Amount',
                         names='District',

                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['District'],
                         labels={'Transaction Amount': 'Transaction Amount'}
                         )
            fig.update_layout(autosize=False,
                              width=500,
                              height=500,
                              margin=dict(
                                  l=50,
                                  r=50,
                                  b=100,
                                  t=0,
                                  pad=4
                              ),
                              paper_bgcolor="#fdf5e6")

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        with col3:
            st.subheader("Top 10 Postal Codes")
            cursor.execute(
                f'''select distinct pincode,transaction_value from PhonePe.top_pin_transactions where year ={year} and quarter={quarter}''')
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Transaction Amount'])
            fig = px.pie(df, values='Transaction Amount',
                         names='Pincode',

                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Pincode'],
                         labels={'Transaction Amount': 'Transaction Amount'}
                         )
            fig.update_layout(autosize=False,
                              width=500,
                              height=500,
                              margin=dict(
                                  l=50,
                                  r=50,
                                  b=100,
                                  t=0,
                                  pad=4
                              ),
                              paper_bgcolor="#fdf5e6")

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)




    elif view == 'Users':
        st.header("Users")

        col1, col2, col3 = st.columns(3, gap="large")
        with col1:
            st.subheader("Top 10 States")
            cursor.execute(
                f'''select distinct state,Registered_Users from PhonePe.top_state_users where year ={year} and quarter={quarter}''')
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Registered Users'])
            fig = px.pie(df, values='Registered Users',
                         names='State',

                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['State'],
                         labels={'Registered Users': 'Registered Users'}
                         )
            fig.update_layout(autosize=False,
                              width=450,
                              height=500,
                              margin=dict(
                                  l=50,
                                  r=90,
                                  b=100,
                                  t=0,
                                  pad=4
                              ),
                              paper_bgcolor="#fdf5e6")

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        with col2:
            st.subheader("Top 10 Districts")
            cursor.execute(
                f'''select district,Registered_Users from (select distinct district,Registered_Users,dense_rank() over(order by Registered_Users asc) as rnk
              from PhonePe.top_district_users where year ={year} and quarter={quarter})a
            where a.rnk<=10''')
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Registered Users'])
            fig = px.pie(df, values='Registered Users',
                         names='District',

                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['District'],
                         labels={'Registered Users': 'Registered Users'}
                         )
            fig.update_layout(autosize=False,
                              width=450,
                              height=500,
                              margin=dict(
                                  l=50,
                                  r=90,
                                  b=100,
                                  t=0,
                                  pad=4
                              ),
                              paper_bgcolor="#fdf5e6")

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        with col3:
            st.subheader("Top 10 Postal Codes")
            cursor.execute(
                f'''select distinct pincode,Registered_Users from PhonePe.top_pin_users where year ={year} and quarter={quarter}''')
            df = pd.DataFrame(cursor.fetchall(), columns=['Pincode', 'Registered Users'])
            fig = px.pie(df, values='Registered Users',
                         names='Pincode',

                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Pincode'],
                         labels={'Registered Users': 'Registered Users'}
                         )
            fig.update_layout(autosize=False,
                              width=450,
                              height=500,
                              margin=dict(
                                  l=50,
                                  r=90,
                                  b=100,
                                  t=0,
                                  pad=4
                              ),
                              paper_bgcolor="#fdf5e6")

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

elif selected == 'Explore Data':

    state_transaction_query = f'''select replace(state,'-',' ') as state, sum(Transaction_count) as 
    Transaction_count, sum(Transaction_value) as Transaction_value from PhonePe.state_transactions where state not in (
    'dadra-&-nagar-haveli-&-daman-&-diu','ladakh') and year ={year}
    and quarter ={quarter}
    group by state '''

    state_user_query = f'''select replace(state,'-',' ') as state, sum(Registered_Users) as 
    Registered_Users, sum(App_Opens) as App_Opens from PhonePe.state_users where state not in (
    'dadra-&-nagar-haveli-&-daman-&-diu','ladakh') and year ={year} and quarter ={quarter}
    group by state '''

    state_transaction_df = pd.read_sql_query(state_transaction_query, connection)
    state_user_df = pd.read_sql_query(state_user_query, connection)

    indian_states = json.load(open("C:\\Users\\Dell\\PycharmProjects\\pythonProject\\venv\\states_india.geojson", 'r'))
    state_id_map = {}
    for feature in indian_states['features']:
        feature['id'] = feature['properties']['state_code']
        state_id_map[feature['properties']['st_nm'].lower()] = feature['id']

    state_id_map['arunachal pradesh'] = state_id_map.pop('arunanchal pradesh')
    state_id_map['andaman & nicobar islands'] = state_id_map.pop('andaman & nicobar island')
    state_id_map['delhi'] = state_id_map.pop('nct of delhi')

    if view == "Transactions":
        st.subheader("Transactions")

        state_transaction_df['id'] = state_transaction_df['state'].apply(lambda x: state_id_map[x])
        state_transaction_df['Transaction Amount Scale'] = np.log10(state_transaction_df['Transaction_value'])

        fig = px.choropleth(state_transaction_df,
                            locations='id',
                            geojson=indian_states,
                            # featureidkey="properties.st_nm",
                            hover_name='state',
                            hover_data=['Transaction_count', 'Transaction_value'],
                            fitbounds='locations',
                            color="Transaction Amount Scale",
                            color_continuous_scale='sunset',

                            basemap_visible=False,
                            labels=None
                            )
        fig.update_layout(autosize=False,
                          width=800,
                          height=1000,
                          margin=dict(
                              l=50,
                              r=90,
                              b=100,
                              t=0,
                              pad=4
                          ),
                          paper_bgcolor="#fdf5e6")

        st.plotly_chart(fig, use_container_width=True)
        cursor.execute(
            f'''select distinct state  from PhonePe.district_transactions where year ={year} and quarter={quarter} ''')
        df = pd.DataFrame(cursor.fetchall(), columns=['State'])

        state_selected = st.selectbox("Select State to view data in detail", df['State'])

        sql = f"select distinct district  from PhonePe.district_transactions where year ={year} and quarter={quarter} and state=%s"

        cursor.execute(sql, state_selected)

        df = pd.DataFrame(cursor.fetchall(), columns=['District'])
        district_selected = st.selectbox("District", df)

        sql = f"select distinct transaction_count,transaction_value   from PhonePe.district_transactions where year ={year} and quarter={quarter} and  district =%s"
        cursor.execute(sql, district_selected)
        df = pd.DataFrame(cursor.fetchall(), columns=['No. Of Transactions', 'Transaction Amount'], index=None)

        st.write(df)

    elif view == 'Users':
        st.subheader("Users")

        state_user_df['id'] = state_user_df['state'].apply(lambda x: state_id_map[x])
        state_user_df['Registered_Users_Scale'] = np.log10(state_user_df['Registered_Users'])

        fig = px.choropleth(state_user_df,
                            locations='id',
                            geojson=indian_states,
                            # featureidkey="properties.st_nm",
                            hover_name='state',
                            hover_data=['Registered_Users', 'App_Opens'],
                            fitbounds='locations',
                            color="Registered_Users_Scale",
                            color_continuous_scale='sunset',

                            basemap_visible=False,
                            labels=None
                            )
        fig.update_layout(autosize=False,
                          width=800,
                          height=1000,
                          margin=dict(
                              l=50,
                              r=90,
                              b=100,
                              t=0,
                              pad=4
                          ),
                          paper_bgcolor="#fdf5e6")

        st.plotly_chart(fig, use_container_width=True)
        cursor.execute(
            f'''select distinct state  from PhonePe.district_users where year ={year} and quarter={quarter} ''')
        df = pd.DataFrame(cursor.fetchall(), columns=['State'])

        state_selected = st.selectbox("Select State to view data in detail", df['State'])

        sql = f"select distinct district  from PhonePe.district_users where year ={year} and quarter={quarter} and state=%s"

        cursor.execute(sql, state_selected)

        df = pd.DataFrame(cursor.fetchall(), columns=['District'])
        district_selected = st.selectbox("District", df)

        sql = f"select distinct Registered_Users,App_Opens   from PhonePe.district_users where year ={year} and quarter={quarter} and  district =%s"
        cursor.execute(sql, district_selected)
        df = pd.DataFrame(cursor.fetchall(), columns=['Registered Users', 'App Opens'], index=None)

        st.write(df)
