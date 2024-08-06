import requests

rac = '''
<select id="racquet" name="racquet" class="form-control" placeholder="Select the racquet">
   <option value="Alex - Clash 100L (1)">Alex - Clash 100L (1)</option>
   <option value="Emily - VCore 98 Blue (2)">Emily - VCore 98 Blue (2)</option>
   <option value="Emily - VCore 98 Black (3)">Emily - VCore 98 Black (3)</option>
   <option value="Alex - ClashR 100 (4)">Alex - ClashR 100 (4)</option>
   <option value="Andrew - PA 2023 White (5)">Andrew - PA 2023 White (5)</option>
   <option value="Andrew - PA 2023 Orange (6)">Andrew - PA 2023 Orange (6)</option>
   <option value="Andrew - PA 2023 Black (7)">Andrew - PA 2023 Black (7)</option>
   <option value="Emily - VCore 98 7th (8)">Emily - VCore 98 7th (8)</option>
   <option value="Andrew - PA Lite (9)">Andrew - PA Lite (9)</option>
   <option value="Andrew - PA Rafa Lite (10)">Andrew - PA Rafa Lite (10)</option>
   <option value="Emily - VCORE 100 6th (11)">Emily - VCORE 100 6th (11)</option>
   <option value="Alex - PA Play (12)">Alex - PA Play (12)</option>
   <option value="Emily - VCore 100L 6th Black (13)">Emily - VCore 100L 6th Black (13)</option>
   <option value="Emily - VCore 100L 6th White (14)">Emily - VCore 100L 6th White (14)</option>
   <option value="Andrew - Burn ULS (15)">Andrew - Burn ULS (15)</option>
   <option value="Emily - Gravity Lite (16)">Emily - Gravity Lite (16)</option>
   <option value="Emily - Graphene Instinct Lite (17)">Emily - Graphene Instinct Lite (17)</option>
   <option value="Alex - Miss Chris (18)">Alex - Miss Chris (18)</option>
   <option value="Alex - Speed Flex (19)">Alex - Speed Flex (19)</option>
   <option value="Alex - Clash Tour 100 (20)">Alex - Clash Tour 100 (20)</option>
   <option value="Alex - EZone 100 (21)">Alex - EZone 100 (21)</option>
   <option value="Andrew - Clash 100UL (22)">Andrew - Clash 100UL (22)</option>
   <option value="Emily - Instinct Lite White (23)">Emily - Instinct Lite White (23)</option>
   <option value="Emily - Instinct Lite (24)">Emily - Instinct Lite (24)</option>
   <option value="Alex - Pure Drive Play (25)">Alex - Pure Drive Play (25)</option>
   <option value="Alex - Prince Force (26)">Alex - Prince Force (26)</option>
   <option value="Andrew - Burn ULS 2 (27)">Andrew - Burn ULS 2 (27)</option>
   <option value="Andrew - Burn 26S Black (28)">Andrew - Burn 26S Black (28)</option>
   <option value="Andrew - Burn 26S Orange (29)">Andrew - Burn 26S Orange (29)</option>
   <option value="Emily - Pure Strike 26 (30)">Emily - Pure Strike 26 (30)</option>
   <option value="Alex - nFury Hybrid (31)">Alex - nFury Hybrid (31)</option>
   <option value="Alex - Burn 95 (32)">Alex - Burn 95 (32)</option>
   <option value="Andrew - Pure Aero 25 (33)">Andrew - Pure Aero 25 (33)</option>
   <option value="Andrew - Pure Drive 23 Junior (34)">Andrew - Pure Drive 23 Junior (34)</option>
   <option value="Emily - Pure Drive 25 Pink Junior (35)">Emily - Pure Drive 25 Pink Junior (35)</option>
   <option value="Andrew - Instinct Junior 21 (36)">Andrew - Instinct Junior 21 (36)</option>
   <option value="Emily - Instinct Junior 21 (37)">Emily - Instinct Junior 21 (37)</option>
   <option value="Andrew - Speed Junior 21 (38)">Andrew - Speed Junior 21 (38)</option>
</select>
'''

# Define the URL to which you want to send the POST request
url = 'https://bluehousemall.azurewebsites.net/lt/stringing?u=0'

# Define the form data as a dictionary
form_data = {
    'field1': 'value1',
    'field2': 'value2',
    'field3': 'value3'
    # Add more fields as required
}

# Send the POST request
response = requests.post(url, data=form_data)

# Check the response status code
if response.status_code == 200:
    print('POST request was successful')
    print('Response content:')
    print(response.text)
else:
    print(f'Failed to send POST request. Status code: {response.status_code}')
    print('Response content:')
    print(response.text)
