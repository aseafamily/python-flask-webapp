import json
from lib_simple_score import get_scores_html


data = {
    "set1" : '''
1-0
2-0
2-1
3-1
3-2
4-2
4-3
5-3
6-3
''',
    "set1_tb" : '''
1-0
2-0
3-0
3-1
3-2
4-2
10-2
''',
    "set2" : '''
0-1
1-1
1-2
2-2
2-3
3-3
4-3
5-3
6-3
''',
    "set2_tb" : '''
''',
    "set3" : '''
6-6
''',
    "set3_tb" : '''
1-0
2-0
10-0
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

html_content = get_scores_html(data_dict)

# Write the string to the file
file_name = "test.html"
with open(file_name, "w") as file:
    file.write(html_content)

print(f"{file_name} has been created with the provided HTML content.")



# Example usage:
#player1_games, player2_games = parse_set_scores(set1)
#print("Player 1 games:", player1_games)
#print("Player 2 games:", player2_games)
