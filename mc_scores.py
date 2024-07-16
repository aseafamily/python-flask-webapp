from mc_styles import *

# HTML RENDER FUNCTIONS
def find_one_set_point(player_one_game, player_two_game, is_ad_scoring, player1_score, player2_score, set_games_play):
    is_set_point = False
    pot_last_game = False

    if player1_score == "A":
        player_one_score = 100
    else:
        player_one_score = int(player1_score)

    if player2_score == "A":
        player_two_score = 100
    else:
        player_two_score = int(player2_score)

    if player_one_game > player_two_game:
        if set_games_play == 4:
            if (player_one_game == 3 and player_two_game < 3) or (player_two_game == 3) or (player_one_game == 4 and player_two_game < 4):
                pot_last_game = True
        if set_games_play == 6:
            if (player_one_game == 5 and player_two_game < 5) or (player_two_game == 7) or (player_one_game == 6 and player_two_game < 6):
                pot_last_game = True
        if set_games_play == 8:
            if (player_one_game == 7 and player_two_game < 7) or (player_two_game == 7) or (player_one_game == 8 and player_two_game < 8):
                pot_last_game = True
    elif player_one_game == player_two_game:
        if player_one_game == set_games_play:
            pot_last_game = True

    if pot_last_game:
        if is_ad_scoring:
            if player_one_score == 100 or (player_one_score == 40 and player_two_score < 40):
                is_set_point = True
        else:
            if player_one_score == 40:
                is_set_point = True
    return is_set_point

def find_set_point(player_one_game_str, player_two_game_str, is_ad_scoring, player1_score, player2_score, is_player_one_won, set_games_play):
    player_one_game = int(player_one_game_str)
    player_two_game = int(player_two_game_str)

    if is_player_one_won:
        player_one_game -= 1
    else:
        player_two_game -= 1

    is_player1_set_point = find_one_set_point(player_one_game, player_two_game, is_ad_scoring, player1_score, player2_score, set_games_play)
    is_player2_set_point = find_one_set_point(player_two_game, player_one_game, is_ad_scoring, player2_score, player1_score, set_games_play)

    return is_player1_set_point, is_player2_set_point

def did_player1_won_game(player_one_scores, player_two_scores, player_one_game, player_two_game, game_number, set_number, games):
    is_player_one_won = True
    is_player_one_won = did_player_one_win(player_one_scores[-1], player_two_scores[-1])
    if player_one_scores[-1] == '40' and player_two_scores[-1] == '40':
        player1_game = int(player_one_game)
        player2_game = int(player_two_game)
        if game_number == 1:
            is_player_one_won = True if player1_game > player2_game else False
        else:
            prev_player1_game = 0
            if game_number > 1:
                prev_game = games[(set_number, game_number - 1)]
                if prev_game:
                    for point in prev_game:
                        if (point[5] == '0' and point[6] == '0'):
                            prev_player1_game = int(point[3])
                            break
                if player1_game > prev_player1_game:
                    is_player_one_won = True
                else:
                    is_player_one_won = False
    return is_player_one_won

def generate_game(set_number, game_number, sets, games, firstServe, is_ad_scoring, set_games_play):
    if (set_number == 3 and game_number != 1):
        return
    
    game = games[(set_number, game_number)]
    player_one_scores = []
    player_two_scores = []

    player_one_game = '0'
    player_two_game = '0'
    is_player_one_serve = True
    is_player_one_won = True

    for point in game:
        if (point[5] == '0' and point[6] == '0'):
            player_one_game = str(point[3])
            player_two_game = str(point[4])
            is_player_one_serve = firstServe
            continue
        player_one_scores.append(point[5])
        player_two_scores.append(point[6])

    is_player_one_won = did_player1_won_game(player_one_scores, player_two_scores, player_one_game, player_two_game, game_number, set_number, games)

    is_tie_break = '1' in player_one_scores or '1' in player_two_scores
    if is_tie_break and game_number == 1:
        if is_player_one_won:
            player_one_game = '1'
        else:
            player_two_game = '1'
    
    game_content = game_div_start

    game_header_content = get_game_header_html(player_one_game, player_two_game, is_player_one_serve, is_player_one_won, is_tie_break)
    game_content += game_header_content

    game_content += game_scores_div_start
    
    for index, score in enumerate(player_one_scores):
        last_player1_score = 0
        last_player2_score = 0
        if index > 0:
            last_player1_score = player_one_scores[index - 1]
            last_player2_score = player_two_scores[index - 1]
        is_player1_set_point = False
        is_player2_set_point = False
        if not is_tie_break:
            is_player1_set_point, is_player2_set_point = find_set_point(player_one_game, player_two_game, is_ad_scoring, score, player_two_scores[index], is_player_one_won, set_games_play)
        else:
            tie_break_point = 10 if set_number == 3 and game_number == 1 else 7
            player1_score = int(score)
            player2_score = int(player_two_scores[index])
            if player1_score > player2_score and player1_score >= (tie_break_point - 1):
                is_player1_set_point = True
            elif player2_score > player1_score and player2_score >= (tie_break_point - 1):
                is_player2_set_point = True
        is_match_point = find_match_point(set_number, sets, games, is_player1_set_point, is_player2_set_point)

        score_content = get_game_score_html(score, player_two_scores[index], last_player1_score, last_player2_score, is_ad_scoring, is_player_one_serve, is_player1_set_point, is_player2_set_point, is_match_point)
        game_content += score_content

    game_content += div_end # game_scores_div_start

    game_content += div_end # game_div_start
    return game_content

def find_match_point(set_number, sets, games, is_player1_set_point, is_player2_set_point):
    if not (is_player1_set_point or is_player2_set_point):
        return False
    
    if set_number == 3:
        return True
    
    set_count = len(sets)

    if set_count == 1:
        return True
    elif (set_count == 3 or set_count == 2) and set_number == 1:
        return False
    
    last_game = find_last_game_in_set(games, 1)
    last_point = last_game[-1]
    player1_game = int(last_point[3])
    player2_game = int(last_point[4])
    player1_won_first_set = player1_game > player2_game

    if player1_won_first_set and is_player1_set_point:
        return True
    elif (not player1_won_first_set) and is_player2_set_point:
        return True
    else:
        return False


def find_last_game_in_set(games, set_number):
    # Filter games to only those in the given set_number
    games_in_set = {key: value for key, value in games.items() if key[0] == set_number}
    
    # If no games found for the set_number, return None
    if not games_in_set:
        return None
    
    # Find the game with the highest game_number in the filtered games
    last_game_key = max(games_in_set.keys(), key=lambda x: x[1])
    
    return games_in_set[last_game_key]

def find_set_games_play(games, set_number):
    last_game = find_last_game_in_set(games, set_number)
    last_point = last_game[-1]
    player1_game = int(last_point[3])
    player2_game = int(last_point[4])
    result = max(player1_game, player2_game)
    if (result == 7):
        result = 6
    elif (result == 9):
        result = 8
    elif (result == 5):
        result = 4
    
    return result

def generate_set(set, sets, games, firstServe, set_index, is_ad_scoring, set_games_play):
    set_name = f"{ordinal(set_index)} set"
    set_content = set_div_start
    if set_index < len(sets):
        set_content += divider_html
    set_content += get_set_header_html(set_name)
    games_content = ''

    for game_number in range(1, len(sets[set]) + 1):
        game_content = generate_game(set, game_number, sets, games, firstServe, is_ad_scoring, set_games_play)
        if game_content:
            games_content = game_content + games_content
        if (firstServe):
            firstServe = False
        else:
            firstServe = True

    set_content += games_content
    set_content += div_end
    return set_content, firstServe

def get_scores_html(sets, games, firstServe, include_var, is_ad_scoring):
    html_content = get_styles(include_var)
    html_content += match_div_start
    sets_html = ''

    for index, set in enumerate(sets, start=1):
        set_games_play = find_set_games_play(games, set)
        set_html, firstServe = generate_set(set, sets, games, firstServe, index, is_ad_scoring, set_games_play)
        sets_html = set_html + sets_html

    html_content += sets_html
    html_content += div_end

    html_content += toggle_script_html
    return html_content