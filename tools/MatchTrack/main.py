import os
import csv
from dataclasses import dataclass
from styles import *


# ['Date', 'Player', 'SetOneScore', 'SetTwoScore', 'SetThreeScore', 'SetFourScore', 'SetFiveScore', '1st Serve %', '2nd Serve %', 'Aces', 'Double Faults', 'Winners', 'Unforced Errors', 'Forced Errors', 'Deuce Points Won', '1st Serve Points Won', '2nd Serve Points Won', 'Break Points Saved', '1st Return Points Won', '2nd Return Points Won', 'Forehand Winner', 'Forehand Slice Winner', 'Forehand Volley Winner', 'Forehand Return Winner', 'Backhand Winner', 'Backhand Slice Winner', 'Backhand Volley Winner', 'Backhand Return Winner', 'Approach Winner', 'Overhead Winner', 'Forehand Error', 'Forehand Slice Error', 'Forehand Volley Error', 'Forehand Return Error', 'Backhand Error', 'Backhand Slice Error', 'Backhand Volley Error', 'Backhand Return Error', 'Approach Error', 'Overhead Error']
# ['2023-06-17 19:21:12 +0000', 'Emily Ma', '7', '3', '5', '', '', '61.84%', '0', '9', '16', '43', '3', '4', '23/47', '9/29', '5/13', '25/48', '12/19', '7/15', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']



@dataclass
class Player:
    name: str = ""
    first_serve_percent: int = 0
    aces: int = 0
    double_faults: int = 0
    winners: int = 0
    unforced_errors: int = 0
    forced_errors: int = 0
    total_points_won: int = 0
    percent_points_won: int = 0
    touch_0_4: int = 0
    touch_5_8: int = 0
    touch_9_plus: int = 0
    service_points_won: int = 0
    receiver_points_won: int = 0
    max_points_in_a_row: int = 0
    current_points_in_a_row: int = 0
    first_serve_points_won: str = ""
    second_serve_points_won: str = ""
    break_points_saved: str = ""
    first_return_points_won: str = ""
    second_return_points_won: str = ""
    break_points_won: str = ""


# PARSING FUNCTIONS
def convert_to_integer(string):
    parts = string.split('.')
    integer_value = parts[0]
    return integer_value

def get_integer_before_shot_rally(string):
    words = string.split()
    if "shot" in words:
        index = words.index("shot") - 1
        if index >= 0 and words[index].isdigit():
            return int(words[index])
    return 0

def parse_details(desc, playerWon: Player, playerLose: Player):
    if ("loses" in desc):
        if ("unforced error" in desc):
            playerLose.unforced_errors = playerLose.unforced_errors + 1
        if (" forced error" in desc):
            playerLose.forced_errors = playerLose.forced_errors + 1
    if ("winner" in desc):
        playerWon.winners = playerWon.winners + 1

    playerWon.total_points_won = playerWon.total_points_won + 1

    shots = get_integer_before_shot_rally(desc)
    if (shots <= 4):
        playerWon.touch_0_4 = playerWon.touch_0_4 + 1
    elif (shots >= 9):
        playerWon.touch_9_plus = playerWon.touch_9_plus + 1
    else:
        playerWon.touch_5_8 = playerWon.touch_5_8 + 1

def parse_row(row, player1: Player, player2: Player):
    global is_ad_scoring  # Declare is_ad_scoring as global

    # for details
    set_number = int(row[0])
    game_number = int(row[1])
    point_number = int(row[2])

    if set_number not in sets:
        sets[set_number] = {}

    if game_number not in sets[set_number]:
        sets[set_number][game_number] = []

    game = sets[set_number][game_number]
    game.append(row)

    games[(set_number, game_number)] = game

    if row[5] == 'A' or row[6] == 'A':
        is_ad_scoring = True

    desc = row[8]
    firstWon = True
    if (player1.name in desc):
        if ("loses" in desc):
            firstWon = False
    
    if (player2.name in desc):
        if ("winner" in desc):
            firstWon = False
        if ("won" in desc):
            firstWon = False
    
    # print(firstWon)

    if (firstWon):
        parse_details(desc, player1, player2)
        player1.current_points_in_a_row = player1.current_points_in_a_row + 1
        if (player2.current_points_in_a_row > player2.max_points_in_a_row):
            player2.max_points_in_a_row = player2.current_points_in_a_row
        player2.current_points_in_a_row = 0
    else:
        parse_details(desc, player2, player1)
        player2.current_points_in_a_row = player2.current_points_in_a_row + 1
        if (player1.current_points_in_a_row > player1.max_points_in_a_row):
            player1.max_points_in_a_row = player1.current_points_in_a_row
        player1.current_points_in_a_row = 0

def parse_percent(string):
    parts = string.split('/')
    return int(parts[0])

def parse_overall_row(row, player: Player):
    player.name = row[1]
    player.first_serve_percent = convert_to_integer(row[7])
    player.aces = row[8]
    player.double_faults = row[9]
    player.service_points_won = parse_percent(row[service_points_won_base]) + parse_percent(row[service_points_won_base+1])
    player.first_serve_points_won = row[service_points_won_base]
    player.second_serve_points_won = row[service_points_won_base+1]
    player.break_points_saved = row[service_points_won_base+2]
    player.first_return_points_won = row[service_points_won_base+3]
    player.second_return_points_won = row[service_points_won_base+4]
    player.break_points_won = row[service_points_won_base+5]

def parse_csv_file(file_path, player1: Player, player2: Player):
    line_no: int = 0
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # print(row)
            if (line_no == 1):
                parse_overall_row(row, player1)
            if (line_no == 2):
                parse_overall_row(row, player2)
            if (line_no > 4):
                parse_row(row, player1, player2)
            line_no = line_no + 1

def process_players(player1, player2):
    total_points = player1.total_points_won + player2.total_points_won
    percent_points_won1: float = player1.total_points_won / total_points
    percent_points_won1_str = f"{float(percent_points_won1) * 100:.2f}%"
    player1.percent_points_won = convert_to_integer(percent_points_won1_str)
    percent_points_won2: float = player2.total_points_won / total_points
    percent_points_won2_str = f"{float(percent_points_won2) * 100:.2f}%"
    player2.percent_points_won = convert_to_integer(percent_points_won2_str)

    player1.receiver_points_won = player1.total_points_won - player1.service_points_won
    player2.receiver_points_won = player2.total_points_won - player2.service_points_won

# CONSOLE PRINT FUNCTIONS
def print_property_table(instance1, instance2):
    properties = [
        "total_points_won",
        "touch_0_4", 
        "touch_5_8", 
        "touch_9_plus",
        "service_points_won",
        "receiver_points_won",
        "max_points_in_a_row",
        "-",
        "winners", 
        "unforced_errors", 
        "forced_errors", 
        "-",
        "first_serve_percent", 
        "aces", 
        "double_faults",
        "first_serve_points_won",
        "second_serve_points_won",
        "first_return_points_won",
        "second_return_points_won",
        "break_points_won",
        "break_points_saved",
    ]

    #max_alias_length = max(len(prop) for prop in properties)
    #max_value_length = max(len(str(getattr(instance1, prop))) for prop in properties)
    max_value_length = 10

    for prop in properties:
        if (prop == "-"):
            print("-" * 40)
            continue

        alias = prop.replace("_", " ").capitalize()
        value1 = str(getattr(instance1, prop))
        value2 = str(getattr(instance2, prop))
        padding2 = " " * (max_value_length - len(value1))
        padding3 = " " * (max_value_length - len(value2))
        if (len(value1) == 1):
            padding2 += " "
        if (len(value2) == 1):
            padding3 += " "

        print(f"{value1}{padding2}{value2}{padding3}{alias}")

def align_element(elem):
    if (len(elem) == 1):
        elem = elem + "  "
    return elem

def align_arrays(array1, array2):
    # Get the maximum length among the arrays
    padded_array1 = [align_element(element) for element in array1]
    padded_array2 = [align_element(element) for element in array2]
    
    # Create aligned strings for each element in the arrays
    aligned_array1 = '  '.join(padded_array1)
    aligned_array2 = '  '.join(padded_array2)

    # Return the aligned arrays
    return aligned_array1, aligned_array2


def print_game_score(set_number, game_number, sets, games, firstServe):
    if (set_number == 3 and game_number != 1):
        return
    
    game = games[(set_number, game_number)]
    player_one_scores = []
    player_two_scores = []

    game_score = ""

    for point in game:
        if (point[5] == '0' and point[6] == '0'):
            if (firstServe):
                game_score = f"{point[3]} * - {point[4]}"
            else:
                game_score = f"{point[3]} - {point[4]} *"
            continue
        player_one_scores.append(point[5])
        player_two_scores.append(point[6])

    if (game_number != 1):
        print('--------')

    if (set_number != 3):
        print(game_score)
    #print(' '.join(player_one_scores))
    #print(' '.join(player_two_scores))
    aligned_array1, aligned_array2 = align_arrays(player_one_scores, player_two_scores)
    print(aligned_array1)
    print(aligned_array2)

def print_scores(sets, firstServe):
    print('\n========')

    for set in sets:
        for game_number in range(1, len(sets[set]) + 1):
            print_game_score(set, game_number, sets, games, firstServe)
            if (firstServe):
                firstServe = False
            else:
                firstServe = True
        print('========')

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

    is_player_one_won = did_player_one_win(player_one_scores[-1], player_two_scores[-1])
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

def generate_set(set, sets, firstServe, set_index, is_ad_scoring):
    set_name = f"{ordinal(set_index)} set"
    set_content = set_div_start
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
    return set_content

def generate_html(sets, firstServe, include_var, is_ad_scoring):
    
    # Define the file name
    file_name = "test.html"
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)

    html_content = get_styles(include_var)
    html_content += match_div_start
    sets_html = ''

    for index, set in enumerate(sets, start=1):
        set_html = generate_set(set, sets, firstServe, index, is_ad_scoring)
        sets_html = set_html + sets_html

    html_content += sets_html
    html_content += div_end

    # Write the string to the file
    with open(file_path, "w") as file:
        file.write(html_content)

    print(f"{file_name} has been created with the provided HTML content.")

# Main

player1 = Player()
player2 = Player()
sets = {}
games = {}
is_ad_scoring = False

script_dir = os.path.dirname(__file__)
# file_path = 'C:\\code\\pyMatchTrack\\data.csv'
file_name = "data.csv"
file_name = 'matchtrackexport2024-07-05 211525 +0000.csv'
file_path = os.path.join(script_dir, file_name)
firstServe = False
service_points_won_base = 13

#file_path = 'data.csv'  # Replace with the path to your CSV file
parse_csv_file(file_path, player1, player2)

process_players(player1, player2)

#print(player1)
#print(player2)

# Print the table of properties
#print_property_table(player1, player2)

print_scores(sets, firstServe)

include_var = True
generate_html(sets, firstServe, include_var, is_ad_scoring)



