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
        ORDER BY {1}.numeric_value ASC    
    """.format(config.db_table_name, config.db_my_data_table_name)
    return db.execute_sql(query)


def find_least_valuable_player(position_players):
    values_for_money = []
    for player in position_players:
        value_for_money = player['position_score'] / player['numeric_value']
        values_for_money.append(value_for_money)
        player['value_for_money'] = value_for_money
    lowest_value = min(values_for_money)
    i = 0
    while i < len(position_players):
        if float(position_players[i]['value_for_money']) == float(lowest_value):
            return i


def build_team(budget):
    team = config.empty_team
    all_players = get_players()
    for new_player in all_players:
        position = new_player['position']
        if not position:  # There are about 60 Null values in the dataset. I'm just ignoring those players altogether.
            continue
        position = config.position_mapper[position]
        current_player_index = find_least_valuable_player(team[position])
        current_player = team[position][current_player_index]
        new_price_of_team = team['price'] - current_player['numeric_value'] + new_player['numeric_value']
        print(new_price_of_team)
        print(budget)
        if new_price_of_team < budget:  # We can switch them out
            print("first if")
            print(new_player['position_score'])
            print(current_player['position_score'])
            if new_player['position_score'] > current_player['position_score']:  # We want to switch them out
                print("second if ----------------------------------------------")
                team[position][current_player_index]['player_id'] = new_player['row_number']
                team[position][current_player_index]['position_score'] = new_player['position_score']
                team[position][current_player_index]['numeric_value'] = new_player['numeric_value']
                team['price'] = new_price_of_team
        else:
            break
    return team






print(build_team(2000000000000000))
