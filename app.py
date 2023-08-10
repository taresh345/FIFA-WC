import streamlit as st
import pandas as pd
import helper, preprocesser
import plotly.express as px

# _____________________________________________________________________________________________________________

matches = pd.read_csv('archive-WC/WorldCupMatches.csv')
players = pd.read_csv("archive-WC/WorldCupPlayers.csv")
wc = pd.read_csv("archive-WC/WorldCups.csv")

wc['Attendance'] = wc['Attendance'].str.replace('.', '')
wc['Attendance'] = pd.to_numeric(wc['Attendance'])

df = preprocesser.preprocess(matches, players)

# ____________________________________________GLOBAL ______________________________________________________________________________

year_list = helper.Edition_list(df)

st.sidebar.header(" WELCOME TO FIFA WC  ANALYSIS")

user_menu = st.sidebar.radio(

    "SELECT AN OPTION",
    (
        'OVERALL ANALYSIS', 'Match by Match Analysis',
        'Historical Comparison and Insights')
)

# ______________________________OVERALL ANALYSIS_______________________________________________________________________________
# ________________________________________________________________________________________________________________________


if user_menu == 'OVERALL ANALYSIS':
    st.title('FIFA WORLD CUP OVER THE YEARS ')

    selected_year = st.selectbox("Select  Edition of FIFA WC", year_list)

    tmp = helper.Structure(matches, selected_year)
    st.table(tmp)

    host, winner, runners_up, goals_scored, no_of_teams, matches_played, attendance, temp = helper.Overall_data(
        selected_year, wc)

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.title(temp[temp['Year'] == selected_year].columns[1])
        st.write("\n")
        st.subheader(host)
    with col2:
        st.title(temp[temp['Year'] == selected_year].columns[2])
        st.write("\n")

        st.subheader(winner)
    with col3:
        st.title(temp[temp['Year'] == selected_year].columns[3])
        st.write("\n")

        st.subheader(runners_up)
    with col4:
        st.title(temp[temp['Year'] == selected_year].columns[4])
        st.write("\n")
        st.subheader(goals_scored)

    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.title(temp[temp['Year'] == selected_year].columns[4])
        st.write("\n")
        st.subheader(no_of_teams)
    with col2:
        st.title(temp[temp['Year'] == selected_year].columns[6])
        st.write("\n")

        st.subheader(matches_played)
    with col3:
        st.title(temp[temp['Year'] == selected_year].columns[7])
        st.write("\n")

        st.subheader(attendance)

    # __________________________________________________________________________________
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.title('Goal-Scoring Trends Over the years')

    temp = wc.groupby(by=['Year'])[wc.columns[6:9].tolist()].sum().reset_index()
    fig = px.line(temp, x=temp['Year'], y=temp.columns[[1, 2, 3, ]].tolist())

    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    # __________________________________________________________________________________

    # ATTENDANCE VS YEARS
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.title('ATTENDANCE Over the years')
    # ATTENDANCE TREND OVER THE YEARS
    temp = wc[['Year', 'Attendance']]
    fig = px.line(temp, x=temp['Year'], y=temp['Attendance'])

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # # -_______________Squad by edition and country_____________________________________
    st.header("Sqaud by EDITION AND COUNTRY  ")

    selected_year = st.selectbox("Select Edition", year_list)

    country_list = helper.country_list_by_year(selected_year, df)

    selected_country = st.selectbox("Select Country", list(country_list.keys()))

    squad = helper.squad_by_year(df, selected_country, selected_year, country_list)

    st.header(selected_country + ' Squad for ' + str(selected_year))
    st.table(squad)
    #  ______________most popular matches by year ______________
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.title("Most popular matches by attendance(per match) in a World cup ")
    col1, col2 = st.columns([1, 3], gap="medium")

    with col1:
        st.subheader("SELECT EDITION")
        selected_year = st.selectbox("EDITION", year_list)

    with col2:
        tmp = helper.popular_matches(matches, selected_year)
        fig = px.bar(tmp, x='Match name', y='Attendance')
        st.plotly_chart(fig)

# ______________________________OVERALL ANALYSIS__END_____________________________________________________________________________
# ________________________________________________________________________________________________________________________


# ______________________________,MATCH BY MATCH ANALYSIS_______________________________________________________________________________
# ________________________________________________________________________________________________________________________


if user_menu == 'Match by Match Analysis':
    # AVG _GOALS PER STAGE(ANY YEAR)________________
    selected_year = st.sidebar.selectbox("EDITION", year_list)

    st.header("Average goals per stage per year ")
    col1, col2 = st.columns([1.5, 3], gap="medium")

    with col1:
        st.subheader("SELECT EDITION")

        st.write('1) Group Stage: The average number of goals might be relatively high in\
                    the group stage, as teams aim to secure points for advancement. \n')

        st.write('2) Knockout Stage: The average goals may vary in the knockout stage.\
                    Early knockout rounds might see cautious play, resulting in fewer goals,\
                    while later rounds and the final could see more goals due to higher stakes and potential \
                                                                                                for extra time. \n')
        st.write('3) Extra Time and Penalties: Matches that go into extra time or \
                                penalties might have fewer goals per match due to the pressure and defensive strategies')

    with col2:
        tmp = helper.avg_goals_per_stage(matches, selected_year)

        fig = px.bar(tmp, x='Stage', y='Mean goals per stage')
        st.plotly_chart(fig)

        # AVG _GOALS PER Stadium ________________
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')
        st.write('\n')

    st.header("Average goals per stadium for Any Edition ")
    col1, col2 = st.columns([3, 5], gap="medium")

    with col1:
        # st.subheader("SELECT EDITION")
        # selected_year = st.selectbox("EDITION", year_list)
        tmp1, tmp2 = helper.venue_impact(matches, selected_year)

        st.subheader('No of matches per stadium in ' + str(selected_year))
        st.table(tmp1)

    with col2:
        fig = px.bar(tmp2, x='Stadium', y='Avg Goals')

        st.plotly_chart(fig)

    # GOALS PER Stadium per country and year ________________

    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.header("Team's Performance in Different Cities/Stadiums ")
    """5)Team's Performance in Different Cities/Stadiums:(team analysis)

    Assess whether a team's performance varies depending on the city or stadium where they are playing."""

    country_list = helper.country_list_by_year(selected_year, df)
    selected_country = st.selectbox("Select Country", country_list)

    new_df = helper.goals_in_stadium_per_country(matches, selected_year, selected_country)

    fig = px.bar(new_df, x='Stadium', y='Goals', color='Stage')
    st.plotly_chart(fig, use_container_width=True)

    total_goals = int(helper.goal_bycountry_by_year(matches, selected_year, selected_country))
    st.header('Total number of goals by ' + selected_country)
    st.subheader(total_goals)

# ______________________________,MATCH BY MATCH ANALYSIS__END_____________________________________________________________________________
# ________________________________________________________________________________________________________________________


# ______________________________HISTORICAL ANALYSIS AND INSIGHTS_______________________________________________________________________________
# ________________________________________________________________________________________________________________________
if user_menu == 'Historical Comparison and Insights':
    #   _________________Average attendance over the years __________________
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.header('Average attendance of every Edition of FIFA WC')
    tmp = matches.groupby('Year')[['Attendance']].mean().reset_index()
    fig = px.bar(tmp, x='Year', y='Attendance')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("The FIFA World Cup editions of 1942 and 1946 were not held due to the "
                 "occurrence of World War 2,"
                 " resulting in their suspension. Consequently, there were no attendance figures recorded for these tournaments.")
    # ____________________________Winner, Runners-Up, Third, Fourth______________________________________________________

    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    # '''Winner, Runners-Up, Third, Fourth: To study the top-performing teams in
    #                                                 each World Cup and identify consistent podium finishers'''
    st.header(' Winner, Runners-Up, Third:  top-performing teams in '
              'each World Cup and consistent podium finishers')
    tmp = helper.win_stats(wc)
    fig = px.bar(tmp, x="index", y=["Winner", 'Runners-Up', 'Third'],
                 barmode='group',
                 height=500)
    st.plotly_chart(fig, use_container_width=True)

    # -_______________ hosting frequency___________________________
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')

    st.header('Hosting frequency')
    host = wc['Country'].value_counts().reset_index()
    fig = px.bar(host, x="index", y='Country',
                 barmode='group',
                 height=500)

    st.plotly_chart(fig, use_container_width=True)
    st.write('Europe and south america have been the more popular hosts for the FIFA WC')

    # _____________Average Goals per Game______________________________________________________________

    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.write('\n')
    st.header("Average Goals per Edition ")
    st.write('The average goals per match might experience fluctuations due to the implementation of\
                        new regulations aimed at discouraging defensive playing styles or the inclusion\
                                                                of additional teams in the FIFA World Cup.')

    col1, col2 = st.columns([2, 5], gap="medium")

    with col1:
        tmp = wc[['Year']]
        tmp['Matches played'] = wc['MatchesPlayed']
        tmp['Average goals per Edition'] = wc['GoalsScored'] / wc['MatchesPlayed']
        st.table(tmp)

    with col2:
        tmp = wc[['Year']]
        tmp['Average goals per Edition'] = wc['GoalsScored'] / wc['MatchesPlayed']
        tmp['Host'] = wc['Country']
        fig = px.bar(tmp, x='Year', y='Average goals per Edition', color='Host')
        st.plotly_chart(fig, use_container_width=True)

    st.header('_______________________________END____________________________')

    # ______________________________HISTORICAL ANALYSIS AND INSIGHTS  END_______________________________________________________________________________
    # ________________________________________________________________________________________________________________________
