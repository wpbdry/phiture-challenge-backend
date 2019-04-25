import db, config


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


def generate_query_string_match_any_whole_word(search_term):
    regex = create_regex(search_term)
    match_any_whole_word_query = '''
        SELECT {0}
        FROM {1}
        WHERE name ~* '{2}'
        OR nationality ~* '{2}'
        OR club ~* '{2}'
    '''.format(config.db_requested_columns, config.db_table_name, regex)
    return match_any_whole_word_query


def generate_query_string_match_any_part_word(search_term):
    match_any_part_word_query = '''
        SELECT {0}
        FROM {1}
        WHERE UPPER(name) LIKE UPPER('%{2}%')
        OR UPPER(nationality) LIKE UPPER('%{2}%')
        OR UPPER(club) LIKE UPPER('%{2}%')
    '''.format(config.db_requested_columns, config.db_table_name, search_term)
    return match_any_part_word_query


def generate_query_string_match_both_whole_words(search_term):
    if len(search_term.split(' ')) != 2:
        return False
    regex = create_regex(search_term)
    match_both_whole_words_query = '''
        SELECT {0}
        FROM {1}
        WHERE (
            name ~* '{2}'
            AND nationality ~* '{2}'
        ) OR (
            nationality ~* '{2}'
            AND club ~* '{2}'
        ) OR (
            club ~* '{2}'
            AND name ~* '{2}'
        )
    '''.format(config.db_requested_columns, config.db_table_name, regex)
    return match_both_whole_words_query


def search(search_term):
    assert (search_term != ''), 'Search string should not be empty'
    words_count = len(search_term.split(' '))
    if words_count == 2:
        exact_matches_query_string = '{} ORDER BY overall DESC;'.format(
            generate_query_string_match_both_whole_words(search_term)
        )
        try:
            exact_matches = db.execute_sql(exact_matches_query_string)
        except Exception:
            raise
        close_matches_query_string = '{} EXCEPT {} ORDER BY overall DESC;'.format(
            generate_query_string_match_any_whole_word(search_term),
            generate_query_string_match_both_whole_words(search_term)
        )
        try:
            close_matches = db.execute_sql(close_matches_query_string)
        except Exception:
            raise
    else:
        exact_matches_query_string = '{} ORDER BY overall DESC;'.format(
            generate_query_string_match_any_whole_word(search_term)
        )
        try:
            exact_matches = db.execute_sql(exact_matches_query_string)
        except Exception:
            raise
        if words_count == 1:
            close_matches_query_string = '{} EXCEPT {} ORDER BY overall DESC;'.format(
                generate_query_string_match_any_part_word(search_term),
                generate_query_string_match_any_whole_word(search_term)
            )
            try:
                close_matches = db.execute_sql(close_matches_query_string)
            except Exception:
                raise
        else:
            close_matches = []

    return {
        'results': exact_matches,
        'moreresults': close_matches
    }


def return_results(search_term):
    function_return = {
        'search': search_term,
        'results': [],
        'moreresults': [],
        'exitcode': 0
    }
    try:
        search_results = search(search_term)
        function_return['results'] = search_results['results']
        function_return['moreresults'] = search_results['moreresults']
    except AssertionError as e:
        print(str(e))
        function_return['exitcode'] = 1
    except Exception as e:
        if str(e)[0:29] == 'could not translate host name' or str(e)[0:6] == 'FATAL:':
            function_return['exitcode'] = 2
        else:
            print(str(e))
            function_return['exitcode'] = 3
    return function_return

