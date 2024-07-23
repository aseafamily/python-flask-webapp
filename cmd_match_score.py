import re
from datetime import datetime


def parse_tennis_result(result_string):
    sets = [s.strip() for s in result_string.split(';')]
    result = {
        'team1_set1': '', 'team1_set1_tb': '',
        'team2_set1': '', 'team2_set1_tb': '',
        'team1_set2': '', 'team1_set2_tb': '',
        'team2_set2': '', 'team2_set2_tb': '',
        'team1_set3': '', 'team1_set3_tb': '',
        'team2_set3': '', 'team2_set3_tb': ''
    }

    team1_wins = 0
    team2_wins = 0

    for i, set_result in enumerate(sets):
        set_index = i + 1
        set_key_team1 = f'team1_set{set_index}'
        set_key_team2 = f'team2_set{set_index}'
        tb_key_team1 = f'team1_set{set_index}_tb'
        tb_key_team2 = f'team2_set{set_index}_tb'
        
        # Extract main scores and tiebreak scores using regex
        match = re.match(r'(\d+)(?:\((\d+)\))?-(\d+)(?:\((\d+)\))?', set_result)
        if match:
            team1_score = int(match.group(1))
            team1_tb = match.group(2)
            team2_score = int(match.group(3))
            team2_tb = match.group(4)

            result[set_key_team1] = str(team1_score)
            result[set_key_team2] = str(team2_score)

            if team1_tb is not None:
                result[tb_key_team1] = team1_tb
                if team2_tb is None:
                    result[tb_key_team2] = str(int(team1_tb) + 2)
            if team2_tb is not None:
                result[tb_key_team2] = team2_tb
                if team1_tb is None:
                    result[tb_key_team1] = str(int(team2_tb) + 2)

            if team1_score > team2_score:
                team1_wins += 1
            else:
                team2_wins += 1

    team1_won = team1_wins > team2_wins
    return team1_won, result

def parse_match_string(match_string, rank_types):
    def extract_rankings(player_string):
        player_string = player_string.replace('/', '').strip()
        rankings = {}

        # Extract seed if present
        seed_match = re.search(r'\[(\d+)\]', player_string)
        seed = ""
        if seed_match:
            seed = seed_match.group(1)
            player_string = re.sub(r'\[\d+\]', '', player_string).strip()

        if '(' in player_string:
            player_name, rank_str = player_string.split('(', 1)
            rank_str = rank_str.replace(')', '').strip()
            rank_values = re.split('[,;]', rank_str)
            for i, rank_value in enumerate(rank_values):
                if i < len(rank_types):
                    rank_type = rank_types[i]
                    rankings[f"{rank_type}"] = re.sub(r'[^\d.]+', '', rank_value)
            player_name = player_name.strip()
        else:
            player_name = player_string
        return player_name, rankings, seed

    lines = match_string.strip().split('\n')
    lines_len = len(lines)
    is_doubles = (lines_len == 5 or lines_len == 4)
    match_info = {}

    player_keys = ['player1', 'player2', 'player3', 'player4']
    for key in player_keys:
        for rank_type in rank_types:
            match_info[f"{key}_{rank_type}"] = ''

    player1_seed = player2_seed = player3_seed = player4_seed = None

    if is_doubles:
        if lines_len == 5:
            match_info['player1'], player1_ranks, player1_seed = extract_rankings(lines[0])
            match_info['player3'], player3_ranks, player3_seed = extract_rankings(lines[1])
            match_info['player2'], player2_ranks, player2_seed = extract_rankings(lines[3])
            match_info['player4'], player4_ranks, player4_seed = extract_rankings(lines[4])
            match_info.update({f'player1_{k}': v for k, v in player1_ranks.items()})
        else:
            match_info['player3'], player3_ranks, player3_seed = extract_rankings(lines[0])
            match_info['player2'], player2_ranks, player2_seed = extract_rankings(lines[2])
            match_info['player4'], player4_ranks, player4_seed = extract_rankings(lines[3])
        
        match_info.update({f'player2_{k}': v for k, v in player2_ranks.items()})
        match_info.update({f'player3_{k}': v for k, v in player3_ranks.items()})
        match_info.update({f'player4_{k}': v for k, v in player4_ranks.items()})

        team1_won, result = parse_tennis_result(lines[2] if lines_len == 5 else lines[1])
    else:
        if lines_len == 3:
            match_info['player1'], player1_ranks, player1_seed = extract_rankings(lines[0])
            match_info['player2'], player2_ranks, player2_seed = extract_rankings(lines[2])
            match_info.update({f'player1_{k}': v for k, v in player1_ranks.items()})
        else:
            match_info['player2'], player2_ranks, player2_seed = extract_rankings(lines[1])
        
        match_info.update({f'player2_{k}': v for k, v in player2_ranks.items()})

        match_info["player1_seed"] = player1_seed if player1_seed is not None else None
        match_info["player2_seed"] = player2_seed if player2_seed is not None else None
        match_info["player3_seed"] = player3_seed if player3_seed is not None else None
        match_info["player4_seed"] = player4_seed if player4_seed is not None else None

        team1_won, result = parse_tennis_result(lines[1] if lines_len == 3 else lines[0])

    match_info.update(result)
    return team1_won, match_info, (not is_doubles)

# Example usage
match_string = """
7-9
[1] Elise Roe (2)
"""

rank_types = ["usta", "utr"]
team1_won, match_info, is_singles = parse_match_string(match_string, rank_types)
# print(match_info)

def parse_title(input_str):
    # Extract and reformat the date
    date_str = input_str.split()[0]
    date = datetime.strptime(date_str, '%m/%d/%Y')
    formatted_date = date.strftime('%Y-%m-%d')
    
    # Extract the second string
    parts = input_str.split()
    second_string = parts[1].lower() if len(parts) > 1 else None
    
    # Extract the third string (inside the brackets), check for null
    third_string_match = re.search(r'\((.*?)\)', input_str)
    third_string = third_string_match.group(1) if third_string_match else None
    
    # Check if the third string is in the format (number)h(number)m
    if third_string:
        match = re.match(r'(\d+)h(\d+)m', third_string)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            total_minutes = hours * 60 + minutes
        else:
            total_minutes = 0
    else:
        total_minutes = 0
    
    return formatted_date, second_string, total_minutes

# Example usage
input_str = "1/27/2018 ETC (O)"
result = parse_title(input_str)
#print(result)

input_str = "4-2; 4-1 "
result = parse_tennis_result(input_str)
#print(result)