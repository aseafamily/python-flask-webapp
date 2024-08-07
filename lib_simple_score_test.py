import json
from lib_simple_score import get_scores_html, parse_string_to_dict


data = {
    "set1" : '''
0-1
1-1
1-2
2-2
3-2
4-2
4-3
4-4
4-5
5-5
6-6
''',
    "set1_tb" : '''
0-1
1-1
1-2
2-2
2-3
3-3
3-4
4-4
4-5
4-6
5-6
5-7
''',
    "set2" : '''
1-0
1-1
1-2
2-2
2-3
2-4
3-4
3-5
3-6
''',
    "set2_tb" : '''
''',
    "set3" : '''
''',
    "set3_tb" : '''
'''
}


def generate_json(data):
    with open('simple.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


generate_json(data)



# Open and read the JSON file
with open('simple.json', 'r') as json_file:
    json_content = json_file.read()

data_dict = json.loads(json_content)
print(data_dict)

new_string = '''
1
1-1
2-2
2
1-1
2-2
3t
1-0
10-0
'''
data_dict = parse_string_to_dict(new_string)

html_content = get_simple_scores_html(data_dict)

# Write the string to the file
file_name = "test.html"
with open(file_name, "w") as file:
    file.write(html_content)

print(f"{file_name} has been created with the provided HTML content.")



# Example usage:
#player1_games, player2_games = parse_set_scores(set1)
#print("Player 1 games:", player1_games)
#print("Player 2 games:", player2_games)
