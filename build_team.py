import copy

import config, db


def get_players():
    query = """
        SELECT
            {0}.row_number,
            {0}.position,
            {1}.position_score,
            {1}.numeric_value
        FROM {0}, {1}
        WHERE {0}.row_number = {1}.row_number
            AND {1}.position_score IS NOT NULL
            AND {1}.numeric_value IS NOT NULL
            AND {0}.position IS NOT NULL
        ORDER BY {1}.numeric_value ASC    
    """.format(config.db_table_name, config.db_my_data_table_name)
    return db.execute_sql(query)


def find_least_valuable_player(position_players):
    values_for_money = []
    for player in position_players:
        value_for_money = float(player['position_score'] / player['numeric_value'])
        values_for_money.append(value_for_money)
        player['value_for_money'] = value_for_money
    lowest_value = min(values_for_money)
    i = 0
    while i < len(position_players):
        if float(position_players[i]['value_for_money']) == float(lowest_value):
            return i
        i += 1


def build_team(budget):
    team = copy.deepcopy(config.empty_team)
    team['budget'] = budget
    all_players = get_players()
    for new_player in all_players:
        position = new_player['position']
        position = config.position_mapper[position]
        current_player_index = find_least_valuable_player(team[position])
        current_player = team[position][current_player_index]
        new_price_of_team = team['price'] - current_player['numeric_value'] + new_player['numeric_value']
        if new_price_of_team <= budget:  # We can afford to switch them out
            if new_player['position_score'] > current_player['position_score']:  # We want to switch them out
                team[position][current_player_index]['player_id'] = new_player['row_number']
                team[position][current_player_index]['position_score'] = new_player['position_score']
                team[position][current_player_index]['numeric_value'] = new_player['numeric_value']
                team['price'] = new_price_of_team
        else:
            break
    return team


def add_team_info_to_team(team):
    team_with_info = {
        'team_is_complete': True,
        'price': int(team['price']),
        'budget': int(team['budget'])
    }
    for position in config.positions:
        position_players = team[position]
        team_with_info[position] = []
        for i in range(0, len(position_players)):
            if position_players[i]['player_id'] != -1:
                query = """
                    SELECT {0}
                    FROM {1}
                    WHERE row_number = {2}
                """.format(config.db_requested_columns_for_team, config.db_table_name, position_players[i]['player_id'])
                new_info = db.execute_sql(query)
                team_with_info[position].append(new_info[0])
                team_with_info[position][i]['player_id'] = int(position_players[i]['player_id'])
                team_with_info[position][i]['position_score'] = int(position_players[i]['position_score'])
                team_with_info[position][i]['numeric_value'] = int(position_players[i]['numeric_value'])
                # Intentionally throw away value_for_money at this point
            else:
                team_with_info['team_is_complete'] = False
    return team_with_info


def provide_team(budget):
    team = build_team(budget)
    team = add_team_info_to_team(team)
    return team
