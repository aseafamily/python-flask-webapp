import re

def parse_tennis_result(result_string):
    sets = result_string.split('; ')
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
        return player_name, rankings

    lines = match_string.strip().split('\n')
    is_doubles = len(lines) == 5
    match_info = {}

    player_keys = ['player1', 'player2', 'player3', 'player4']
    for key in player_keys:
        for rank_type in rank_types:
            match_info[f"{key}_{rank_type}"] = ''

    if is_doubles:
        match_info['player1'], player1_ranks = extract_rankings(lines[0])
        match_info['player3'], player3_ranks = extract_rankings(lines[1])
        match_info['player2'], player2_ranks = extract_rankings(lines[3])
        match_info['player4'], player4_ranks = extract_rankings(lines[4])
        
        match_info.update({f'player1_{k}': v for k, v in player1_ranks.items()})
        match_info.update({f'player2_{k}': v for k, v in player2_ranks.items()})
        match_info.update({f'player3_{k}': v for k, v in player3_ranks.items()})
        match_info.update({f'player4_{k}': v for k, v in player4_ranks.items()})

        team1_won, result = parse_tennis_result(lines[2])
    else:
        match_info['player1'], player1_ranks = extract_rankings(lines[0])
        match_info['player2'], player2_ranks = extract_rankings(lines[2])
        
        match_info.update({f'player1_{k}': v for k, v in player1_ranks.items()})
        match_info.update({f'player2_{k}': v for k, v in player2_ranks.items()})

        team1_won, result = parse_tennis_result(lines[1])

    match_info.update(result)
    return team1_won, match_info

# Example usage
match_string = """
(2.73) (A)
/Yuan Wang (2.69, UTR4)
6-2; 6-3
Stuart Howe (3.0S, UTR3)
/CRAIG MONTGOMERY (2.5S, UTR3)
"""

rank_types = ["usta", "utr"]
team1_won, match_info = parse_match_string(match_string, rank_types)
#print(match_info)