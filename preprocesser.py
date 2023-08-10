

def preprocess(matches, players):
    matches.dropna(inplace=True)
    players = players.drop(columns=['Position'])

    matches.drop_duplicates(keep='last', inplace=True)
    matches.reset_index(inplace=True)
    #  merging dataset by matchid

    df = matches.merge(players, on='MatchID', how='left')
    df['Year'] = df['Year'].astype(int)
    return df
