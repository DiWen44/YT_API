import os
import requests
import json
import sys
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

chanID = sys.argv[1] # Channel ID is passed as a command-line parameter
chanResponse = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={chanID}&key={API_KEY}").json()

if chanResponse['pageInfo']['totalResults'] == 0:
    sys.exit('ERROR: No channel found with provided ID')

chanData = chanResponse["items"][0] # All actual & pertinent channel data is found in "items" array


# Get channel's videos via the uploads playlist assocated with the channel, which contains all of the videos uploaded by the channel
uploadsPlaylistID = chanData['contentDetails']['relatedPlaylists']['uploads']
uploadsPlaylistItems = requests.get(f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails&playlistId={uploadsPlaylistID}&key={API_KEY}").json()['items'] # Get all playlistItems in the upload playlist.

# Get IDs of all uploaded videos from their corresponding playlistItems.
videoIDs = []
for item in uploadsPlaylistItems: 
    videoIDs.append(item['snippet']['resourceId']['videoId'])

videoIDs = ','.join(videoIDs) # Convert array into comma-seperated string (no spaces) so it can be passed as a URL parameter
vids = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={videoIDs}&key={API_KEY}").json()['items'] # Get all videos corresponding to the videoIDs

# Cleaning video data to get only relevant details
vidsCleaned = []
for vid in vids:
    vidCleaned = {
        'name': vid['snippet']['title'],
        'id': vid['id'],
        'uploadDate': vid['snippet']['publishedAt'],

        'views': vid['statistics']['viewCount'],
        'likes': vid['statistics']['likeCount'],
        'commentCount': vid['statistics']['commentCount'],
    }
    vidsCleaned.append(vidCleaned)


# Cleaned & Filtered channel data to be inserted into JSON file
channel = {
    'name': chanData['snippet']['title'],
    'id': chanData['id'],
    'subCount': chanData['statistics']['subscriberCount'],  # YouTube rounds this value to 3 significant figures
    'videos': vidsCleaned
}


# Adding channel data to file
with open("data_test.json", "r+") as file:
    
    data = json.load(file)
    data["channels"].append(channel)

    # Delete all existing data in file before writing updated JSON object
    file.seek(0)
    file.truncate()

    json.dump(data, file, indent=4)


print("Channel has been added")

