from dataclasses import dataclass, field
from io import StringIO
import csv
from mc_scores import get_scores_html
from mc_logs import get_logs_html
from mc_statistics import get_statistics_html
import re

@dataclass
class Player:
    name: str = ""
    double_name: str = ""
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
    data: dict = field(default_factory=dict)
    is_old_format: bool = False

service_points_won_base = 13

sets = {}
games = {}

# PARSING FUNCTIONS
def parse_csv_string(csv_string, is_doubles):
    player1 = Player()
    player2 = Player()

    player1d = Player()
    player2d = Player()

    global sets
    global games
    sets = {}
    games = {}

    is_ad_scoring = False

    score_start_line = 6 if is_doubles else 4

    line_no = 0
    header_row = ''
    # Create a file-like object from the CSV string
    csv_file = StringIO(csv_string)
    
    reader = csv.reader(csv_file)
    for row in reader:
        if line_no > score_start_line:
            result = parse_row(row, player1, player2)
            if result:
                is_ad_scoring = True
        else:
            if line_no == 0:
                header_row = row
            else:
                if is_doubles:
                        if line_no == 1:
                            parse_overall_row(row, player1, header_row)
                        elif line_no == 2:
                            player1.double_name = row[1]
                            parse_overall_row(row, player1d, header_row)
                        elif line_no == 3:
                            parse_overall_row(row, player2, header_row)
                        elif line_no == 4:
                            player2.double_name = row[1]
                            parse_overall_row(row, player2d, header_row)
                else:
                    if line_no == 1:
                        parse_overall_row(row, player1, header_row)
                    elif line_no == 2:
                        parse_overall_row(row, player2, header_row)

        line_no += 1

    if is_doubles:
        merge_doubles(player1, player1d)
        merge_doubles(player2, player2d)

    process_players(player1, player2)

    return sets, games, is_ad_scoring, player1, player2

def merge_doubles(player: Player, playerd: Player):
    player.aces += playerd.aces
    player.double_faults += playerd.double_faults
    player.total_points_won += playerd.total_points_won
    player.winners +=  playerd.winners
    player.forced_errors += playerd.forced_errors
    player.unforced_errors += playerd.unforced_errors
    player.data = merge_dictionaries(player.data, playerd.data)

def merge_dictionaries(dict1, dict2):
    merged_dict = dict1.copy()  # Start with a copy of dict1

    for key in dict1:
        if key in dict2:
            # Convert strings containing only digits to integers
            val1 = dict1[key]
            val2 = dict2[key]
            
            if isinstance(val1, str) and val1.isdigit():
                val1 = int(val1)
            if isinstance(val2, str) and val2.isdigit():
                val2 = int(val2)

            # Handle integers
            if isinstance(val1, int) and isinstance(val2, int):
                merged_dict[key] = val1 + val2
            # Handle strings with the "number1/number2 90%" format
            elif isinstance(val1, str) and isinstance(val2, str):
                match1 = re.match(r"(\d+)/(\d+)", val1)
                match2 = re.match(r"(\d+)/(\d+)", val2)
                if match1 and match2:
                    num1_1, num2_1 = int(match1.group(1)), int(match1.group(2))
                    num1_2, num2_2 = int(match2.group(1)), int(match2.group(2))
                    new_num1 = num1_1 + num1_2
                    new_num2 = num2_1 + num2_2
                    merged_dict[key] = f"{new_num1}/{new_num2}"
    
    return merged_dict

        
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
    is_ad_scoring = False

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
    if (player1.name in desc or (player1.double_name in desc if player1.double_name else False)):
        if ("loses" in desc):
            firstWon = False
    
    if (player2.name in desc or (player2.double_name in desc if player2.double_name else False)):
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

    return is_ad_scoring

def parse_percent(string):
    parts = string.split('/')
    return int(parts[0])

def insert_zero_at_tenth_position(arr):
    # Check if the array length is more than 10
    if len(arr) > 10:
        # Insert "0" as the 10th element
        arr.insert(10, '0')
    return arr

def parse_overall_row(row, player: Player, header_row):
    player.is_old_format = len(row) < 50
    if player.is_old_format:
        row.insert(10, '0')

    data_dict = {header.strip(): value.strip() for header, value in zip(header_row, row)}
    
    player.data = data_dict
    #for key, value in data_dict.items():
    #    print(f"{key}: {value}")

    if player.is_old_format:
        player.aces = row[8]
        player.double_faults = row[9]
    else:
        player.aces = data_dict["Aces"]
        player.double_faults = data_dict["Double Faults"]

    player.name = row[1]
    player.first_serve_percent = convert_to_integer(row[7])
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

def get_scores_html_by_csv(csv_content, firstServe, include_var, is_doubles):
    sets, games, is_ad_scoring, player1, player2 = parse_csv_string(csv_content, is_doubles)
    html_content = get_statistics_html(player1, player2) if not is_doubles else ''
    html_content += get_scores_html(sets, games, firstServe, include_var, is_ad_scoring)
    html_content += get_logs_html(sets, games, player1, player2)
    return html_content