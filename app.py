import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

data = pd.read_csv("Athletes_summer_games.csv")
noc_region_data = pd.read_csv("regions.csv")

data = preprocessor.preprocess(data, noc_region_data)

st.set_page_config(page_title='Olympics Stats till 2020', page_icon = 'https://www.designboom.com/wp-content/uploads/2013/11/rio_2016_olympics_pictograms01.jpg', layout='wide')


st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://assets.editorial.aetnd.com/uploads/2010/01/gettyimages-466313493-2.jpg", width = 250)
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall analysis', 'Countrywise Analysis', 'Athletewise Analysis')
)


if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(data)

    selected_year = st.sidebar.selectbox("Select Years", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(data, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally till 2020 olympics ")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympics")

    st.table(medal_tally)

if user_menu == "Overall analysis":
    editions = data["Year"].unique().shape[0]
    cities = data["City"].unique().shape[0]
    sports = data["Sport"].unique().shape[0]
    events = data["Event"].unique().shape[0]
    athletes = data["Name"].unique().shape[0]
    nations = data["region"].unique().shape[0]

    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    
    nations_over_time = helper.data_over_time(data,'region')
    fig = px.line(nations_over_time, x = "Year", y="count")
    st.title("Participating nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(data,'Event')
    fig = px.line(events_over_time, x = "Year", y="count")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(data,'Name')
    fig = px.line(athletes_over_time, x = "Year", y="count")
    st.title("Atheletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events Over Time (Every Sport)")
    fig, ax = plt.subplots(figsize = (20,20))
    x = data.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index = "Sport", columns = 'Year', values = "Event", aggfunc = "count").fillna(0).astype(int),
                     annot = True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(data,selected_sport)
    st.table(x)

if user_menu == 'Countrywise Analysis':
    
    st.sidebar.title('Country-wise Analysis')

    country_list = data['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(data,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(data,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(data,selected_country)
    st.table(top10_df)

if user_menu == 'Athletewise Analysis':
    athlete_df = data.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')


    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(data)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
