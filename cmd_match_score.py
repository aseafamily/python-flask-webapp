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

def parse_match_string(match_string):
    lines = match_string.strip().split('\n')
    is_doubles = len(lines) == 5
    match_info = {}

    match_info['player1_usta'] = ''
    match_info['player2_usta'] = ''
    match_info['player3_usta'] = ''
    match_info['player4_usta'] = ''
    
    if is_doubles:
        match_info['player1'] = lines[0].replace('/', '').strip()
        match_info['player3'] = lines[1].replace('/', '').strip()
        match_info['player2'] = lines[3].replace('/', '').strip()
        match_info['player4'] = lines[4].replace('/', '').strip()
        
        if '(' in match_info['player1']:
            match_info['player1'], match_info['player1_usta'] = match_info['player1'].split('(')
            match_info['player1_usta'] = match_info['player1_usta'].replace(')', '').strip()
            match_info['player1'] = match_info['player1'].strip()

        if '(' in match_info['player2']:
            match_info['player2'], match_info['player2_usta'] = match_info['player2'].split('(')
            match_info['player2_usta'] = match_info['player2_usta'].replace(')', '').strip()
            match_info['player2'] = match_info['player2'].strip()

        if '(' in match_info['player3']:
            match_info['player3'], match_info['player3_usta'] = match_info['player3'].split('(')
            match_info['player3_usta'] = match_info['player3_usta'].replace(')', '').strip()
            match_info['player3'] = match_info['player3'].strip()

        if '(' in match_info['player4']:
            match_info['player4'], match_info['player4_usta'] = match_info['player4'].split('(')
            match_info['player4_usta'] = match_info['player4_usta'].replace(')', '').strip()
            match_info['player4'] = match_info['player4'].strip()

        team1_won, result = parse_tennis_result(lines[2])
    else:
        match_info['player1'] = lines[0].replace('/', '').strip()
        match_info['player2'] = lines[2].strip()
        
        if '(' in match_info['player1']:
            match_info['player1'], match_info['player1_usta'] = match_info['player1'].split('(')
            match_info['player1_usta'] = match_info['player1_usta'].replace(')', '').strip()
            match_info['player1'] = match_info['player1'].strip()

        if '(' in match_info['player2']:
            match_info['player2'], match_info['player2_usta'] = match_info['player2'].split('(')
            match_info['player2_usta'] = match_info['player2_usta'].replace(')', '').strip()
            match_info['player2'] = match_info['player2'].strip()

        team1_won, result = parse_tennis_result(lines[1])

    match_info.update(result)
    return team1_won, match_info

# Example usage
'''
match_string = """
(2.20)
/Tom Lash (2.12)
6-0; 6-4
Christopher Nunes (2.08)
/Jason Zhong (1.84)
"""
team1_won, match_info = parse_match_string(match_string)
print(f"Team 1 won: {team1_won}")
print(match_info)
'''