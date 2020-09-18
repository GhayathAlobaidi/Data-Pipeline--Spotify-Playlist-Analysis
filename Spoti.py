"""
Spoti allows you to connect to Spotify's Web API and retrieve 
audio features of songs in a Spotify playlist
"""
import sys
import spotipy
import spotipy.util as util
import methods
import pandas as pd

with open('ID.txt', 'r') as f:           # Part 1 Authorization #
    CID = f.readline().strip()
    Secret = f.readline().strip()
    URI = f.readline().strip()
username= ""
scope= 'user-library-read playlist-read-private'

# Prompt the user to login and return access Token 
token = util.prompt_for_user_token(username, scope, client_id=CID, 
                                   client_secret=Secret, redirect_uri=URI)
if token:   
    sp = spotipy.Spotify(auth=token)    # Create Spotify API Object 
else:
    print("Can't retrieve token")
   
playlist_uri = sys.argv[1]              # Part 2- Data Retrieval #

# Use playlist URI provided by user and make connection 
playlist = sp.user_playlist_tracks(username, playlist_uri)
Total = playlist['total']
print('This playlist has this {} songs'.format(Total))    

API_Calls = methods.number_of_calls(Total)
print("Spoti will make {} call(s) to Spotiy's web API".format(API_Calls))

Final_list = []              # Final list of songs and their features
for t in range(API_Calls):   # For every 100 songs, the for loop increases
    offset = t * 100         # offset number by 100 and gets song IDs
    print('Retrieving audio features for tracks {}-'.format(offset))
    playlist = sp.user_playlist_tracks(username, playlist_uri, offset=offset)
    songs = playlist["items"] 
    song_ids = []           
    for i in range(len(songs)): 
        song_ids.append(songs[i]["track"]["id"])    
    features = sp.audio_features(song_ids) 
    Final_list += features   # Add features of 100 songs to Final_list
    
df = pd.DataFrame(Final_list)      # Part 3- Data Analyzing/Visualization #
csv = methods.create_csv(df)       # Convert DataFrame to csv file
charts = methods.plotdata('features.csv', Total)  # Plot data 

