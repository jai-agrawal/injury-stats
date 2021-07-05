from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, leaguedashplayerstats
import pandas as pd
import time

class Player():
    def __init__(self, **kwargs):
        self.name = kwargs.get('player_name')
        self.players_dict = players.get_active_players()
        self.all_players_dict = players.get_players()

    def get_players_for_a_season(self, season):
        stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season).get_data_frames()[0]
        players_dict = []
        for i in range(len(stats)):
            if stats['PLAYER_NAME'][i] != None:
                players_dict.append({'id':stats['PLAYER_ID'][i], 'full_name': stats['PLAYER_NAME'][i], 'team':
                stats['TEAM_ABBREVIATION'][i]})
        return players_dict

    def get_player_log(self, id, period='1y'):
        if period == '1y':
            date_from_nullable = '05/22/2020'
        else:
            date_from_nullable = '11/22/2020'
        season_types = ['Regular Season', 'Playoffs']
        dfs = []
        for season_type in season_types:
            df = playergamelog.PlayerGameLog(player_id=id, season='2020-21', season_type_all_star=season_type)
            time.sleep(.600)
            dfs.append(df.get_data_frames()[0])
        for season_type in season_types:
            df = playergamelog.PlayerGameLog(player_id=id, season='2019-20', season_type_all_star=season_type,
                                             date_from_nullable=date_from_nullable)
            time.sleep(.600)
            dfs.append(df.get_data_frames()[0])
        total_df = pd.concat(dfs,ignore_index=True)
        return total_df

    def get_player_log_2(self, id, period='1y'):
        if period == '1y':
            date_from_nullable = '04/13/2018'
        else:
            date_from_nullable = '10/13/2018'
        season_types = ['Regular Season', 'Playoffs']
        dfs = []
        for season_type in season_types:
            df = playergamelog.PlayerGameLog(player_id=id, season='2018-19', season_type_all_star=season_type)
            dfs.append(df.get_data_frames()[0])
        for season_type in season_types:
            df = playergamelog.PlayerGameLog(player_id=id, season='2017-18', season_type_all_star=season_type,
                                             date_from_nullable=date_from_nullable)
            dfs.append(df.get_data_frames()[0])
        total_df = pd.concat(dfs,ignore_index=True)
        return total_df

    def get_total_mins(self, log):
        return log['MIN'].sum()

def main():
    all = Player()
    # GET PLAYER DATA FOR 365 DAYS PERIOD PRIOR TO 2021 PLAYOFFS
    player_logs_1 = []
    for player in all.players_dict:
        log = all.get_player_log(player['id'])
        total_mins = all.get_total_mins(log)
        player_logs_1.append(
            {'name': player['full_name'], 'id': player['id'], 'minsPlayed': total_mins}
        )
    df1 = pd.DataFrame(player_logs_1)
    print(df1['minsPlayed'].mean())
    df1.to_csv('logs_season1921.csv')

    # GET PLAYER DATA FOR 365 DAYS PERIOD PRIOR TO 2019 PLAYOFFS
    player_logs_2 = []
    season_players_dict = all.get_players_for_a_season('2018-19')
    for player in season_players_dict:
        log = all.get_player_log_2(player['id'])
        total_mins = all.get_total_mins(log)
        player_logs_1.append(
            {'name': player['full_name'], 'id': player['id'], 'minsPlayed': total_mins}
        )
    df2 = pd.DataFrame(player_logs_2)
    print(df2['minsPlayed'].mean())
    df2.to_csv('logs_season1719.csv')

    # 2021 BUBBLE ADJUSTMENT
    players_opting_out = ['Spencer Dinwiddie', 'DeAndre Jordan', 'Wilson Chandler', 'Bradley Beal', 'Davis Bertans',
                          'Willie Cauley-Stein', 'Avery Bradley', 'Trevor Ariza', 'Taurean Prince', 'Thabo Sefalosha']
    # teams_out = [
    #     'Cleveland Cavaliers', 'Golden State Warriors', 'Minnesota Timberwolves', 'Detroit Pistons',
    #     'Atlanta Hawks', 'New York Knicks', 'Chicago Bulls', 'Charlotte Hornets']
    teams_out = ['ATL', 'CHA', 'CHI', 'CLE', 'DET', 'GSW', 'NYK','MIN']

    all = Player()
    players = all.get_players_for_a_season('2019-20')
    print(players)
    players_in_bubble = []
    for player in players:
        if player['team'] not in teams_out and player['full_name'] not in players_opting_out:
            players_in_bubble.append(player['full_name'])
    df = df1
    indeces_to_drop = []
    for i in range(len(df)):
        if df['name'][i] in players_in_bubble:
            pass
        else:
            indeces_to_drop.append(i)
    df = df.drop(labels=indeces_to_drop, axis=0)
    print(f"Average mins (bubble-adjusted):{df['minsPlayed'].mean()}")

    # GET PLAYER DATA FOR 6 MONTHS PERIOD PRIOR TO 2021 PLAYOFFS
    player_logs_3 = []
    for player in all.players_dict:
        log = all.get_player_log(player['id'], period='6m')
        total_mins = all.get_total_mins(log)
        player_logs_3.append(
            {'name': player['full_name'], 'id': player['id'], 'minsPlayed': total_mins}
        )
    df3 = pd.DataFrame(player_logs_3)
    print(df3['minsPlayed'].mean())
    df3.to_csv('logs_season1921_2.csv', index=False)

    # GET PLAYER DATA FOR 6 MONTHS PERIOD PRIOR TO 2019 PLAYOFFS
    player_logs_4 = []
    for player in all.players_dict:
        log = all.get_player_log_2(player['id'], period='6m')
        total_mins = all.get_total_mins(log)
        player_logs_4.append(
            {'name': player['full_name'], 'id': player['id'], 'minsPlayed': total_mins}
        )
    df4 = pd.DataFrame(player_logs_4)
    print(df4['minsPlayed'].mean())
    df4.to_csv('logs_season1719_2.csv', index=False)

    # PLAYER ANALYSIS
    player_list = [
        'James Harden', 'Kyrie Irving', 'Kawhi Leonard',
        'Anthony Davis', 'Joel Embiid', 'Donovan Mitchell',
        'Chris Paul', 'Jaylen Brown', 'Mike Conley',
        'Giannis Antetokounmpo'
    ]
    # for player in player_list:
    player_mins_played = []
    for player in player_list:
        for i in range(len(df1)):
            if df1['name'][i] == player:
                totalMins_1920_1y = df1['minsPlayed'][i]
        for i in range(len(df2)):
            if df2['name'][i] == player:
                totalMins_1719_1y = df2['minsPlayed'][i]
        for i in range(len(df3)):
            if df3['name'][i] == player:
                totalMins_1920_6m = df3['minsPlayed'][i]
        for i in range(len(df4)):
            if df4['name'][i] == player:
                totalMins_1719_6m = df4['minsPlayed'][i]
        player_mins_played.append(
            {
                'name': player,
                'totalMins_1920_1y': totalMins_1920_1y,
                'totalMins_1719_1y': totalMins_1719_1y,
                'totalMins_1920_6m': totalMins_1920_6m,
                'totalMins_1719_6m': totalMins_1719_6m
            }
        )

    players = pd.DataFrame(player_mins_played)
    players.to_csv('players.csv', index=False)
main()
