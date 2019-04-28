import secret

# Flask
flask_host = "0.0.0.0"
flask_port = 80

# Database
db_host = "balarama.db.elephantsql.com"
db_port = "5432"
db_name = "stcyqqal"
db_user = "stcyqqal"
db_password = secret.elephantsql_dbpassword

db_table_name = "phiture_challenge.players"
db_my_data_table_name = "phiture_challenge.my_data"
db_requested_columns = "name, age, nationality, club, photo, overall, value"
db_requested_columns_for_team = "name, age, nationality, photo, value, height, preferred_foot, jersey_number"

# Team constellation
positions = ['goalkeeper', 'fullback', 'halfback', 'forward playing']

position_mapper = {
    'GK': 'goalkeeper',
    'LB': 'fullback',
    'RB': 'fullback',
    'LWB': 'fullback',
    'RWB': 'fullback',
    'CB': 'halfback',
    'LCB': 'halfback',
    'RCB': 'halfback',
    'CDM': 'halfback',
    'LDM': 'halfback',
    'RDM': 'halfback',
    'CM': 'halfback',
    'LCM': 'halfback',
    'RCM': 'halfback',
    'LM': 'halfback',
    'RM': 'halfback',
    'CAM': 'forward playing',
    'LAM': 'forward playing',
    'RAM': 'forward playing',
    'LW': 'forward playing',
    'RW': 'forward playing',
    'CF': 'forward playing',
    'LF': 'forward playing',
    'RF': 'forward playing'
}

empty_team = {
    'price': 11,
    'goalkeeper': [
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        }
    ],
    'fullback': [
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        },
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        }
    ],
    'halfback': [
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        },
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        },
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        }
    ],
    'forward playing': [
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        },
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        },
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        },
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        },
        {
            'player_id': -1,
            'position_score': 0,
            'numeric_value': 1
        }
    ]
}
