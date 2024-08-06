import requests
from datetime import datetime
import re

# Define the URL to which you want to send the POST request
url = 'https://bluehousemall.azurewebsites.net/lt/stringing?u=0'

# Given input blocks separated by empty lines
input_data = '''
10/22/2018 (1)
Solinco Hyper G 17 @55LB
'''

# Split the input into blocks by empty lines
blocks = [block.strip() for block in input_data.strip().split('\n\n')]

def parse_block(lines):
    # Initialize variables
    date = ''
    main_string = ''
    main_tension = ''
    main_string_usage = ''
    cross_string = ''
    cross_tension = ''
    cross_string_usage = ''
    break_date = ''

    # Split the block into lines
    lines = lines.split('\n')

    # Parse date and additional info from the first line
    if len(lines) > 0:
        date_str, *rest = lines[0].split(' ')
        date = datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        date_year = date.split('-')[0]

    # Handle different cases based on the number of lines
    if len(lines) > 1:
        # Second line may contain main string and tension
        if '@' in lines[1]:
            main_string, main_tension_usage = lines[1].split('@')
            main_string = main_string.strip()
            main_tension_usage = main_tension_usage.strip()

            # Extract main tension and usage
            main_tension_match = re.match(r'(\d+)LB', main_tension_usage)
            if main_tension_match:
                main_tension = main_tension_match.group(1)

            usage_match = re.search(r'\(([\d.]+)\)', main_tension_usage)
            if usage_match:
                usage_value = usage_match.group(1)
                if re.match(r'^\d+(\.\d+)?$', usage_value):
                    main_string_usage = usage_value

    # Third line may contain cross string and tension if present
    if len(lines) > 2:
        if '@' in lines[2]:
            cross_string, cross_tension_usage = lines[2].split('@')
            cross_string = cross_string.strip()
            cross_tension_usage = cross_tension_usage.strip()

            # Extract cross tension and usage
            cross_tension_match = re.match(r'(\d+)LB', cross_tension_usage)
            if cross_tension_match:
                cross_tension = cross_tension_match.group(1)

            usage_match = re.search(r'\(([\d.]+)\)', cross_tension_usage)
            if usage_match:
                usage_value = usage_match.group(1)
                if re.match(r'^\d+(\.\d+)?$', usage_value):
                    cross_string_usage = usage_value

    # Fourth line may contain break date if present
    if len(lines) > 3:
        break_match = re.match(r'(\d{1,2}/\d{1,2}/\d{4}) broke (\d+)', lines[3])
        if break_match:
            break_date = break_match.group(1)
            if len(break_date.split('/')) == 2:
                    break_date = f"{break_date}/{date_year}"

    # Print the parsed values for debugging
    print(f"date: {date}")
    print(f"main_string: {main_string}")
    print(f"main_tension: {main_tension}")
    print(f"main_string_usage: {main_string_usage}")
    print(f"cross_string: {cross_string}")
    print(f"cross_tension: {cross_tension}")
    print(f"cross_string_usage: {cross_string_usage}")
    print(f"break_date: {break_date}")

    return {
        'date': date,
        'racquet': 'Alex - Burn 95 (32)',  # Assuming static for example
        'stringer': 'Alex',  # Assuming static for example
        'main_string': main_string,
        'main_tension': main_tension,
        'main_string_usage': main_string_usage,
        'cross_string': cross_string,
        'cross_tension': cross_tension,
        'cross_string_usage': cross_string_usage,
        'break_date': break_date
    }

# Process each block and send POST requests
for block in blocks:
    form_data = parse_block(block)

    # Send the POST request
    response = requests.post(url, data=form_data)

    # Check the response status code
    if response.status_code == 200:
        print('POST request was successful')
        #print('Response content:')
        #print(response.text)
    else:
        print(f'Failed to send POST request. Status code: {response.status_code}')
        print('Response content:')
        print(response.text)
