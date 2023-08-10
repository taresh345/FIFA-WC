# function to get name of stages for any year and  list of match id by the selected stage
import pandas as pd
import numpy as np
import streamlit as st


def Edition_list(df):
    year_list = df['Year'].unique().tolist()
    return year_list


def fetch_stage_byYear(df, year):
    group_list = df[df['Year'] == year][['MatchID', 'Stage']].groupby(
        by=['Stage', 'MatchID']).sum().reset_index().Stage.unique().tolist()
    return group_list


def fetch_MatchId_by_Stage(year, selected_stage, df):
    matchid_list = df[df['Year'] == year][df['Stage'] == selected_stage][['MatchID', 'Stage']].groupby(
        by=['Stage', 'MatchID']).sum().reset_index().MatchID.unique().tolist()
    return matchid_list


def country_list_by_year(year, df):
    selected_data = df[df['Year'] == year]

    ccodes = {}

    for _, row in selected_data.iterrows():
        ccodes[row['Home Team Name']] = row['Home Team Initials']
        ccodes[row['Away Team Name']] = row['Away Team Initials']

    return ccodes


# _____________________________OVERALL DATA______________________________________________________________________________________________


# Breakdown thstructure of the match

def Structure(matches, year):
    return matches[matches['Year'] == year][['RoundID', 'Stage']].groupby(by=['Stage']).count().sort_values(
        by=['RoundID'], ascending=False).rename(columns={'RoundID': "no of matches played"})


def Overall_data(year, wc):
    temp = wc.drop(columns=['Third', 'Fourth'])
    temp.rename(columns={'Country': 'Host'}, inplace=True)

    host = temp[temp['Year'] == year].values[0][1]
    winner = temp[temp['Year'] == year].values[0][2]
    runners_up = temp[temp['Year'] == year].values[0][3]
    goals_scored = temp[temp['Year'] == year].values[0][4]
    no_of_teams = temp[temp['Year'] == year].values[0][5]
    matches_played = temp[temp['Year'] == year].values[0][6]
    attendance = temp[temp['Year'] == year].values[0][7]

    return host, winner, runners_up, goals_scored, no_of_teams, matches_played, attendance, temp


def win_stats(wc):
    win = wc['Winner'].value_counts().to_frame().reset_index()
    win.rename(columns={"count":'1st',"Winner":"country"},inplace=True)
    st.write(win)
    
    sec = wc['Runners-Up'].value_counts().to_frame().reset_index()
    sec.rename(columns={"count":'2nd',"Runners-Up":"country"},inplace=True)
    sec=win.merge(sec,on='country',how='outer')
    st.write(sec)
    
    
    third = wc['Third'].value_counts().to_frame().reset_index()
    third.rename(columns={"count":'3rd',"Third":"country"},inplace=True)
    st.write(third)
    third=third.merge(sec,on='country',how='outer')
    third=third.fillna(0)
    third[['3rd','1st','2nd']]=third[['3rd','1st','2nd']].astype(int)
    st.write(third)
    
    
   
    third = pd.melt(third, id_vars=['country'], value_vars=["1st", "2nd", "3rd"])
    
    return third


def squad_by_year(df, selected_country, year, ccodes):
    a = df[df['Year'] == year][df['Team Initials'] == ccodes[selected_country]]['Player Name'].unique()
    tmp = pd.DataFrame(a, columns=['Name'])

    return tmp


def popular_matches(matches, year):
    """matches data is used because global df is skewing the data leading to incorrect analysis  """
    tmp = matches[matches['Year'] == year]

    tmp['Match name'] = tmp['Home Team Name'] + " Vs " + tmp['Away Team Name']
    return tmp[['Match name', 'Attendance']]


# _____________________________OVERALL DATA__END____________________________________________________________________________________________


# ____________________________MATCH BY MATCH ANALYSIS____________________________________________________________________________________________
def avg_goals_per_stage(matches, year):
    tmp = matches[matches['Year'] == year]
    tmp['Total Goals'] = np.add(tmp['Home Team Goals'], tmp['Away Team Goals'])
    tmp = tmp.groupby(by=['Stage'])[['Total Goals', 'RoundID']].agg(['mean', 'count']) \
        .drop(columns=['RoundID'])['Total Goals'].sort_values(['count'], ascending=False) \
        .drop(columns=['count']).reset_index().rename(columns={'mean': 'Mean goals per stage'})

    return tmp


def venue_impact(matches, year):
    """returns average goals per stadium , to determine which stadium has a higher tendency to concede more goals """
    tmp = matches[matches['Year'] == year]
    tmp['Total Goals'] = np.add(tmp['Home Team Goals'], tmp['Away Team Goals'])

    match_per_stad = tmp[['Stadium', 'Total Goals']].groupby(by=['Stadium']).count().rename(
        columns={'Total Goals': 'Matches played'})

    avg_goal_per_stad = tmp[['Stadium', 'Total Goals']].groupby(by=['Stadium'])[['Total Goals']].mean() \
        .rename(columns={'Total Goals': 'Avg Goals'}).reset_index()
    return match_per_stad, avg_goal_per_stad


def goals_in_stadium_per_country(matches, year, country):
    tmp = matches[matches['Year'] == year]

    tmp = tmp[(tmp['Home Team Name'] == country) | (tmp['Away Team Name'] == country)]

    new_df = pd.DataFrame()

    new_df['Stadium'] = tmp.Stadium.tolist()
    new_df['City'] = tmp.City.tolist()
    new_df['Stage'] = tmp.Stage.tolist()

    new_df['Goals'] = np.where(tmp['Home Team Name'] == country, tmp['Home Team Goals'], tmp['Away Team Goals'])
    return new_df


# No of goals per country per year
# 0_____________  Total goals per country in a particular Edition ____________

def goal_bycountry_by_year(matches, year, selected_country):
    home_goals = matches[(matches['Year'] == year)][matches['Home Team Name'] == selected_country][
                     'Home Team Goals'].sum() + \
                 matches[(matches['Year'] == year)][matches['Away Team Name'] == selected_country][
                     'Away Team Goals'].sum()

    return home_goals
