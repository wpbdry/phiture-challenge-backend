import db


def search_by_name(search_term):
    assert (search_term != ''), 'Search string should not be empty'
    query = '''
        SELECT name, age, nationality, club, photo, overall, value
        FROM phiture_challenge.players
        WHERE name LIKE '%{}%'
    '''.format(search_term)
    print(query)
    matches = db.execute_sql(query)
    return matches


def return_results(search_term):
    try:
        matches = search_by_name(search_term)
        return matches
    except AssertionError:
        raise
