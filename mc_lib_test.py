import os
import csv
from dataclasses import dataclass
from mc_scores import get_scores_html
from io import StringIO
from mc_lib import parse_csv_string, get_scores_html_by_csv



# ['Date', 'Player', 'SetOneScore', 'SetTwoScore', 'SetThreeScore', 'SetFourScore', 'SetFiveScore', '1st Serve %', '2nd Serve %', 'Aces', 'Double Faults', 'Winners', 'Unforced Errors', 'Forced Errors', 'Deuce Points Won', '1st Serve Points Won', '2nd Serve Points Won', 'Break Points Saved', '1st Return Points Won', '2nd Return Points Won', 'Forehand Winner', 'Forehand Slice Winner', 'Forehand Volley Winner', 'Forehand Return Winner', 'Backhand Winner', 'Backhand Slice Winner', 'Backhand Volley Winner', 'Backhand Return Winner', 'Approach Winner', 'Overhead Winner', 'Forehand Error', 'Forehand Slice Error', 'Forehand Volley Error', 'Forehand Return Error', 'Backhand Error', 'Backhand Slice Error', 'Backhand Volley Error', 'Backhand Return Error', 'Approach Error', 'Overhead Error']
# ['2023-06-17 19:21:12 +0000', 'Emily Ma', '7', '3', '5', '', '', '61.84%', '0', '9', '16', '43', '3', '4', '23/47', '9/29', '5/13', '25/48', '12/19', '7/15', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']



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

def parse_csv_file(file_path):
    sets = games = is_ad_scoring = player1 = player2 = None

    try:
        with open(file_path, 'r') as file:
            csv_content = file.read()  # Read entire file content as string
            sets, games, is_ad_scoring, player1, player2 = parse_csv_string(csv_content)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

    return sets, games, is_ad_scoring, player1, player2


def generate_html_file(sets, games, firstServe, include_var, is_ad_scoring):
    
    # Define the file name
    file_name = "scores.html"
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file_name)

    html_content = get_scores_html(sets, games, firstServe, include_var, is_ad_scoring)

    # Write the string to the file
    with open(file_path, "w") as file:
        file.write(html_content)

    print(f"{file_name} has been created with the provided HTML content.")

def generate_html_file_by_csv(csv_file_path, firstServe, include_var):
    
    # Define the file name
    file_name = "scores.html"
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(f"{script_dir}\\tools\\MatchTrack", file_name)

    csv_content = None

    with open(csv_file_path, 'r') as file:
            csv_content = file.read()  # Read entire file content as string

    html_content = get_scores_html_by_csv(csv_content, firstServe, include_var)

    # Write the string to the file
    with open(file_path, "w") as file:
        file.write(html_content)

    print(f"{file_name} has been created with the provided HTML content.")

# Main

firstServe = False

script_dir = os.path.dirname(__file__)
# file_path = 'C:\\code\\pyMatchTrack\\data.csv'
file_name = 'matchtrackexport2024-07-06 172742.csv'
file_path = os.path.join(f"{script_dir}\\tools\\MatchTrack", file_name)

#file_path = 'data.csv'  # Replace with the path to your CSV file
sets, games, is_ad_scoring, player1, player2 = parse_csv_file(file_path)

#print(player1)
#print(player2)

# Print the table of properties
print_property_table(player1, player2)

print_scores(sets, firstServe)

include_var = True
# generate_html_file(sets, games, firstServe, include_var, is_ad_scoring)

generate_html_file_by_csv(file_path, firstServe, include_var)



