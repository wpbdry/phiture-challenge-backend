import secret

# Flask
flask_host = "0.0.0.0"
flask_port = 5000

# Database
db_host = "balarama.db.elephantsql.com"
db_port = "5432"
db_name = "stcyqqal"
db_user = "stcyqqal"
db_password = secret.elephantsql_dbpassword
db_table_name = "phiture_challenge.players"
db_requested_columns = "name, age, nationality, club, photo, overall, value"
db_requested_columns_team = "name, photo, position, overall, position, preferred_foot, jersey_number, height"
