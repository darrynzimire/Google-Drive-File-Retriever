from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import argparse
from datetime import datetime
import output
import io
import time


parser = argparse.ArgumentParser(description='Retrieval of raw FASTQ files from Google drive')
parser.add_argument('-fl',      type=str, required=False, help='A list of file names to search and retrieve')
parser.add_argument('-outdir',  type=str, required=False, default=os.getcwd(), help='the path to the desired output directory')

args = parser.parse_args()
filenames = args.fl
outdir = args.outdir


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
DRIVE = build('drive', 'v3', http=creds.authorize(Http()))


def authentication():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


def connect_api(creds):

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API

        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        results = service.files().list(
            pageSize=20, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        # print('Files:')
        # for item in items:
        #     print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


def download_file(id, filename):

    request = parser.files().get_media(fileId=id)
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
        time.sleep(2)


def main():

    output.search_files(filenames)
    output.output_dir()


if __name__ == '__main__':
    main()