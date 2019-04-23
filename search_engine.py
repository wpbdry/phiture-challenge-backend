import db


def create_regex(search_term):
    words = search_term.split(' ')
    regex = ''
    for item in range(len(words)):
        regex += '(\m'
        regex += words[item]
        regex += '\M)'
        if item < len(words) - 1:
            regex += '|'
    return regex


def search_by_name(search_term):
    assert (search_term != ''), 'Search string should not be empty'
    regex = create_regex(search_term)
    query = '''
        SELECT name, age, nationality, club, photo, overall, value
        FROM phiture_challenge.players
        WHERE name ~* '{0}'
        OR nationality ~* '{0}'
        OR club ~* '{0}';
    '''.format(regex)
    matches = db.execute_sql(query)
    return matches


def return_results(search_term):
    try:
        matches = search_by_name(search_term)
        return matches
    except AssertionError:
        raise
