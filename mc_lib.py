from dataclasses import dataclass
from io import StringIO
import csv
from mc_scores import get_scores_html

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

service_points_won_base = 13

sets = {}
games = {}
is_ad_scoring = False

# PARSING FUNCTIONS
def parse_csv_string(csv_string):
    player1 = Player()
    player2 = Player()

    line_no = 0
    # Create a file-like object from the CSV string
    csv_file = StringIO(csv_string)
    
    reader = csv.reader(csv_file)
    for row in reader:
        if line_no == 1:
            parse_overall_row(row, player1)
        elif line_no == 2:
            parse_overall_row(row, player2)
        elif line_no > 4:
            parse_row(row, player1, player2)
        line_no += 1

    process_players(player1, player2)

    return sets, games, is_ad_scoring, player1, player2
        
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

def get_scores_html_by_csv(csv_content, firstServe, include_var):
    sets, games, is_ad_scoring, player1, player2 = parse_csv_string(csv_content)
    html_content = get_scores_html(sets, games, firstServe, include_var, is_ad_scoring)
    return html_content