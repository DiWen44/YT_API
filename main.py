import os
import requests
import json
import sys
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

chanID = sys.argv[1] # Channel ID is passed as a command-line parameter
response = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={chanID}&key={API_KEY}").json() # Get JSON response for channel ID

if response['pageInfo']['totalResults'] == 0:
    sys.exit('ERROR: No channel found with provided ID')

channel = response["items"][0] # Actual channel data is found in "items" array

# Adding channel data to file
with open("data_test.json", "r+") as file:
    
    data = json.load(file)
    data["channels"].append(channel)

    # Delete all existing data in file before writing updated JSON object
    file.seek(0)
    file.truncate()

    json.dump(data, file, indent=4)


print("Channel has been added")