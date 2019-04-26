# -*- coding: utf-8 -*-

import db, config


def get_all_players_from_db():
    query = """
        SELECT *
        FROM {}
    """.format(config.db_table_name)
    return db.execute_sql(query)


def calculate_value_for_money_per_position(players):
    for player in players:

        # Get position score
        pos = player['position']
        if not pos:
            position_score = player['overall']  # Good enough for now
        elif pos == 'LS' or pos == 'RS' or pos == 'ST':  # These positions exist in the dataset but not in teams
            position_score = None
        elif pos == 'GK':  # GK has multiple score columns in dataset
            position_score = (  # Take average. I have no idea about football so it's fine.
                    player['gk_diving']
                    + player['gk_handling']
                    + player['gk_kicking']
                    + player['gk_positioning']
                    + player['gk_reflexes']
            ) / 5
        else:
            position_score = player[pos.lower()]
        if isinstance(position_score, str):  # Convert scores to number, ignoring + values
            for i in range(0, len(position_score) - 1):
                if position_score[i] == '+':
                    position_score = position_score[0:i]
                    position_score = int(position_score, 10)

        # Get value as a sensible number
        val = player['value']
        if val == '€0':
            numeric_value = None
        else:
            # Value usually looks like '€200K'
            try:
                multiplier = val[len(val)-1:len(val)]
                numeric_value = val[1:len(val)-1]
                numeric_value = int(numeric_value, 10)
                if multiplier == 'K':
                    numeric_value = numeric_value * 1000
                elif multiplier == 'M':
                    numeric_value = numeric_value * 1000000
                else:
                    numeric_value = None
            except Exception:
                numeric_value = None

        # Calculate value for money and add to object
        if position_score and numeric_value:
            value_for_money = position_score / numeric_value
        else:
            value_for_money = None
        player['value_for_money'] = value_for_money
    return players


players = get_all_players_from_db()
print(calculate_value_for_money_per_position(players))
