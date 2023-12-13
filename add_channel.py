import os
import requests
import json
import sys
from dotenv import load_dotenv


"""
Returns an array of dicts representing provided channel's videos

PARAMETERS:
    channel - Dictionary for API object for pertinent channel
    numVids - No. of videos to get
Returned video dicts have fields:
    name - name of video
    id - video ID
    uploadDateTime - date & time of video publication. Stored in a string (In ISO 8601 format) in the JSON file and in the JSON response from the YouTube API, so should be converted to datetime when used.
    duration - Video's duration. Stored in a string (In ISO 8601 format) in the JSON file and in the JSON response from the YouTube API, so should be converted to datetime when used.
    views - No. of views
    likes - No. of likes
    commentCount - No. of comments
"""
def getVideos(channel, numVids):

    # A "playlist" object contains "playlistItem" objects, each of which is associated with a video in that playlist.
    # The "uploads" playlist contains playlistItems for all videos posted by the channel
    uploadsPlaylistID = channel['contentDetails']['relatedPlaylists']['uploads']
    try:
        uploadsPlaylistItems = requests.get(f"https://www.googleapis.com/youtube/v3/playlistItems?maxResults={numVids}&part=snippet,contentDetails&playlistId={uploadsPlaylistID}&key={API_KEY}").json()['items'] # Get all playlistItems in the upload playlist.
    except KeyError: # Thrown if 'items' key does not exist i.e channel has no videos
        sys.exit('ERROR: Channel has no videos')

    # Get IDs of all uploaded videos from their corresponding playlistItems.
    videoIDs = []
    for item in uploadsPlaylistItems: 
        videoIDs.append(item['snippet']['resourceId']['videoId'])

    videoIDs = ','.join(videoIDs) # Convert array into comma-seperated string (no spaces) so it can be passed as a URL parameter
    vids = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={videoIDs}&key={API_KEY}").json()['items'] # Get all videos corresponding to the videoIDs

    if len(vids) != numVids:
        print(f"Channel {channel['snippet']['title']} has less than {numVids} videos.\nReturning the channel's {len(vids)} published videos")

    # Cleaning video data to get only relevant details
    vidsCleaned = []
    for vid in vids:
        vidCleaned = {
            'name': vid['snippet']['title'],
            'id': vid['id'],
            'uploadDateTime': vid['snippet']['publishedAt'],
            'duration': vid['contentDetails']['duration'],
            
            'views': int(vid['statistics']['viewCount']),
            'likes': int(vid['statistics']['likeCount']),
            'commentCount': int(vid['statistics']['commentCount']),
        }
        vidsCleaned.append(vidCleaned)

    return vidsCleaned


load_dotenv()
API_KEY = os.getenv("API_KEY")

# Opening & loading JSON from file
file = open("data_test.json", "r+")
channels = json.load(file)

try:
    chanID = sys.argv[1]
except IndexError: # If no first command-line param was passed
    sys.exit('ERROR: No channel ID was provided')

try:     
    numVids = int(sys.argv[2])
    if numVids < 0 or numVids > 50: # Max no. of playlistItems that can be returned from 1 API query is 50
        sys.exit('ERROR: Requested number of videos out of range (Valid range: 0-50 inclusive)')
except IndexError: # If no second command-line param was passed
    numVids = 25

# Check if user has entered channel that is already in file
for i in channels:
    if i['id'] == chanID:
        sys.exit('Channel is already saved')

response = requests.get(f"https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id={chanID}&key={API_KEY}").json()

if response['pageInfo']['totalResults'] == 0:
    sys.exit('ERROR: No channel found with provided ID')

chanData = response["items"][0] # response is actually a search response, and since we searched by ID, the first and only search result is desired.


# Cleaned & Filtered channel data to be inserted into JSON file
channel = {
    'name': chanData['snippet']['title'],
    'id': chanData['id'],
    'subCount': int(chanData['statistics']['subscriberCount']),  # YouTube rounds this value to 3 significant figures
    'videos': getVideos(chanData, numVids)
}


# Adding new data to file
channels.append(channel)

# Delete all existing data in file before writing updated JSON object
file.seek(0)
file.truncate()

json.dump(channels, file, indent=4)
file.close()

print("Channel has been added")

