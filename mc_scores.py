from mc_styles import *

# HTML RENDER FUNCTIONS
def find_one_set_point(player_one_game, player_two_game, is_ad_scoring, player1_score, player2_score):
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

    if player_one_game > player_two_game and ((player_one_game == 5 and player_two_game < 5) or player_one_game == 6 or (player_one_game == 7 and player_two_game < 7) or player_one_game == 8):
        pot_last_game = True
    elif player_one_game == player_two_game and ((player_one_game == 6) or (player_one_game == 8)):
        pot_last_game = True

    if pot_last_game:
        if is_ad_scoring:
            if player_one_score == 100 or (player_one_score == 40 and player_two_score < 40):
                is_set_point = True
        else:
            if player_one_score == 40:
                is_set_point = True
    return is_set_point

def find_set_point(player_one_game_str, player_two_game_str, is_ad_scoring, player1_score, player2_score, is_player_one_won):
    player_one_game = int(player_one_game_str)
    player_two_game = int(player_two_game_str)

    if is_player_one_won:
        player_one_game -= 1
    else:
        player_two_game -= 1

    is_player1_set_point = find_one_set_point(player_one_game, player_two_game, is_ad_scoring, player1_score, player2_score)
    is_player2_set_point = find_one_set_point(player_two_game, player_one_game, is_ad_scoring, player2_score, player1_score)

    return is_player1_set_point, is_player2_set_point

def generate_game(set_number, game_number, sets, games, firstServe, is_ad_scoring):
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

    is_player_one_won = True
    is_player_one_won = did_player_one_win(player_one_scores[-1], player_two_scores[-1])
    if player_one_scores[-1] == '40' and player_two_scores[-1] == '40':
        player1_game = int(player_one_game)
        player2_game = int(player_two_game)
        if player1_game == player2_game:
            next_game = games[(set_number, game_number + 1)]
            if next_game:
                next_player1_game = '0'
                next_player2_game = '0'
                for point in next_game:
                    if (point[5] == '0' and point[6] == '0'):
                        next_player1_game = str(point[3])
                        next_player2_game = str(point[4])
                        break
                if player_one_game != next_player1_game:
                    is_player_one_won = True
                else:
                    is_player_one_won = False
        else:
            is_player_one_won = True if player1_game > player2_game else False

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
            is_player1_set_point, is_player2_set_point = find_set_point(player_one_game, player_two_game, is_ad_scoring, score, player_two_scores[index], is_player_one_won)
        else:
            tie_break_point = 10 if set_number == 3 and game_number == 1 else 7
            player1_score = int(score)
            player2_score = int(player_two_scores[index])
            if player1_score > player2_score and player1_score >= (tie_break_point - 1):
                is_player1_set_point = True
            elif player2_score > player1_score and player2_score >= (tie_break_point - 1):
                is_player2_set_point = True
        score_content = get_game_score_html(score, player_two_scores[index], last_player1_score, last_player2_score, is_ad_scoring, is_player_one_serve, is_player1_set_point, is_player2_set_point)
        game_content += score_content

    game_content += div_end # game_scores_div_start

    game_content += div_end # game_div_start
    return game_content

def generate_set(set, sets, games, firstServe, set_index, is_ad_scoring):
    set_name = f"{ordinal(set_index)} set"
    set_content = set_div_start
    if set_index < len(sets):
        set_content += divider_html
    set_content += get_set_header_html(set_name)
    games_content = ''

    for game_number in range(1, len(sets[set]) + 1):
        game_content = generate_game(set, game_number, sets, games, firstServe, is_ad_scoring)
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
        set_html, firstServe = generate_set(set, sets, games, firstServe, index, is_ad_scoring)
        sets_html = set_html + sets_html

    html_content += sets_html
    html_content += div_end

    html_content += toggle_script_html
    return html_content