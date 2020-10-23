# Program that deletes videos in a music playlist on YouTube that are not songs.

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "C:/Users/Olga/Downloads/client_secrets.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)

credentials = flow.run_console()

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

# my 'Music' playlist
playlist_source = 'PLcCEEReoDqaq8gV6qjZscoFg7yWgnJq4_'
# gets contentDetails(video ids) for videos in my my music playlist
response = youtube.playlistItems().list(
    part='contentDetails',
    playlistId=playlist_source,
    maxResults=50
).execute()

# YouTube Data API's playlistItems can only list a max of 50
# nextPageToken is used get all the videos in the playlist
playlistItems = response['items']
nextPageToken = response.get('nextPageToken')

while nextPageToken:
    response = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_source,
        maxResults=50,
        pageToken=nextPageToken
    ).execute()

    playlistItems.extend(response['items'])
    nextPageToken = response.get('nextPageToken')


def search_for_keywords(tags, title, description):
    key_words = ['lyric', 'Lyric', 'song', 'music']
    # tags = list   title = str description = str

    for word in key_words:
        try:
            if word in tags:
                return 1
            elif word in title:
                return 1
            elif word in description:
                return 1
            else:
                pass
        except KeyError:
            pass

    return -1


for video in playlistItems:
    vid_id = video['contentDetails']['videoId']
    video_id = video['id']
    # 'response1' used to get category for each video pulled from 'response'
    response1 = youtube.videos().list(
        part='snippet',
        id=vid_id
    ).execute()

    category_id = response1['items'][0]['snippet']['categoryId']
    # try - except is used in case video does not have tags, KeyError will be caught
    try:
        tags = response1['items'][0]['snippet']['tags']
        title = response1['items'][0]['snippet']['title']
        description = response1['items'][0]['snippet']['description']
    except KeyError:
        pass

    if category_id == '10' or search_for_keywords(tags, title, description) == 1:
        # if vid is not in category 10(music), delete it from the music playlist
        print(response1['items'][0]['snippet']['title'])
    else:
        print("VIDEO NOT A SONG  ***  " + response1['items'][0]['snippet']['title'])
        response2 = youtube.playlistItems().delete(
            id=video_id
        ).execute()
        print('DELETED: ' + response1['items'][0]['snippet']['title'])