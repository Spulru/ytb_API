#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import json
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

APP_TOKEN_FILE = 'client_secret_CLIENTID.json'
USER_TOKEN_FILE = 'token.json'
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.upload'
]


def get_creds():
    creds = None

    if os.path.exists(USER_TOKEN_FILE):
        with open(USER_TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token, encoding='ASCII')

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
            creds = flow.run_local_server(port=3000)

        with open(USER_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token, protocol=3)

    return creds


def get_service_youtube():
    creds = get_creds()
    service = build('youtube', 'v3', credentials=creds)
    return service


def main():
    youtube = get_service_youtube()

    search_v = youtube.search().list(part='snippet', maxResults=25, type='video',
                                     q='Billie Eilish - everything i wanted (Mellen Gi Remix)').execute()

    for key in search_v['items']:
        for k in key:
            if k == 'snippet':
                if key['snippet']['channelTitle'] == 'TrapMusicHDTV':
                    channel_id = key['snippet']['channelId']
                    video_id = key['id']['videoId']

                    get_rating = youtube.videos().getRating(id=video_id).execute()

                    for key_gr in get_rating['items']:
                        if key_gr['rating'] == 'like':
                            pass
                        else:
                            youtube.videos().rate(id=video_id, rating='like').execute()

                    get_comments = youtube.commentThreads().list(part='snippet,replies', videoId=video_id).execute()
                    print(get_comments)


if __name__ == '__main__':
    main()
