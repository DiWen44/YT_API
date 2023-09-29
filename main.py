import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

chanID = input("ENTER CHANNEL ID: ")
channel = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={chanID}&key={API_KEY}").json() # Get channel JSON object

# Adding channel data to file
with open("data.json", "r+") as file:
    
    data = json.load(file)
    data["channels"].append(channel)

    # Delete all existing data in file before writing updated JSON object
    file.seek(0)
    file.truncate()

    json.dump(data, file, indent=4)


print("Channel has been added")