from mc_styles import *

def count_valid_sets(match_data):
    valid_sets_count = 0
    for key, value in match_data.items():
        if key.startswith('set') and not key.endswith('_tb') and value.strip():
            valid_sets_count += 1

    if match_data['set3_tb'] and match_data['set3_tb'].strip() and valid_sets_count == 2:
        valid_sets_count = 3
    return valid_sets_count

def parse_set_scores(set_string):
    player1_games = []
    player2_games = []

    lines = set_string.strip().split('\n')
    for line in lines:
        if line.strip():  # Ignore any empty lines
            player1_score, player2_score = line.split('-')
            player1_games.append(int(player1_score))
            player2_games.append(int(player2_score))

    return player1_games, player2_games

def generate_game(games, set_index, is_tb, tie_break_point, tb_final):
    player1_scores, player2_scores = parse_set_scores(games)
    if len(player1_scores) == 0:
        return "", 0, 0
    
    player1_games = player1_scores[-1]
    player2_games = player2_scores[-1]
    is_player_one_won = player1_scores[-1] >= player2_scores[-1]

    if is_tb:
        if is_player_one_won:
            player1_games = tb_final + 1
            player2_games = tb_final
        else:
            player1_games = tb_final
            player2_games = tb_final + 1
        
    
    game_content = game_div_start

    game_header_content = get_game_header_html(str(player1_games), str(player2_games), True, is_player_one_won, True)
    game_content += game_header_content

    game_content += game_scores_div_start
    
    for index, score in enumerate(player1_scores):
        last_player1_score = 0
        last_player2_score = 0
        if index > 0:
            last_player1_score = player1_scores[index - 1]
            last_player2_score = player2_scores[index - 1]
        
        player1_score = int(score)
        player2_score = int(player2_scores[index])
        is_player1_set_point = False
        is_player2_set_point = False
        if player1_score > player2_score and player1_score >= (tie_break_point - 1):
            is_player1_set_point = True
        elif player2_score > player1_score and player2_score >= (tie_break_point - 1):
            is_player2_set_point = True
        score_content = get_game_score_html(str(score), str(player2_scores[index]), last_player1_score, last_player2_score, True, True, is_player1_set_point, is_player2_set_point, False)
        game_content += score_content

    game_content += div_end # game_scores_div_start

    game_content += div_end # game_div_start
    return game_content, player1_games, player2_games

def generate_set(data_dict, set_index, set_length):
    

    set_name = f"{ordinal(set_index)} set"
    set_content = set_div_start
    if set_index < set_length:
        set_content += divider_html
    set_content += get_set_header_html(set_name)
    games_content = ''

    game_content, player1_games, player2_games = generate_game(data_dict[f'set{set_index}'], set_index, False, 6, 0)
    if game_content:
        games_content = game_content + games_content

    tb = data_dict[f'set{set_index}_tb']
    tb_limit = 7 if player1_games and player2_games else 10
    tb_final = player1_games if tb_limit == 7 else 0
    if tb and tb.strip():
        game_content, player1_games, player2_games = generate_game(tb, set_index, True, tb_limit, tb_final)
        if game_content:
            games_content = game_content + games_content
    
    set_content += games_content
    set_content += div_end
    return set_content

def get_scores_html(data_dict):
    html_content = get_styles(True)
    html_content += match_div_start
    sets_html = ''
    set_length = count_valid_sets(data_dict)

    # Loop with index from 1 to 3
    for index in range(1, 4):
        if index <= set_length:
            set_html = generate_set(data_dict, index, set_length)
            sets_html = set_html + sets_html

    html_content += sets_html
    html_content += div_end

    html_content += toggle_script_html
    return html_content