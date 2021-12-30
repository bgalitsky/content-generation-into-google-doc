#!/usr/bin/env python
# https://github.com/tanaikech/gdoctableapppy/blob/master/gdoctableapppy/gdoctableapp.py
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from gdoctableapppy import gdoctableapp

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
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

    resource = {
        "oauth2": creds,
        "documentId": "1nhNcAfVLAxxh-fBTgAFVPpSH09mx0o2QGw_0BTZbSCo",
        "rows": 3,
        "columns": 5,
        "createIndex": 1,
        # "append": True,  # When this is used instead of "Index", new table is created to the end of Document.
        "values": [["a1", "b1"], ["a2", "b2"], ["a3", "b3", "c3"]]
    }
    res = gdoctableapp.CreateTable(resource)
    print(res)  # You can see the retrieved responses from Docs API.

    resource = {
        "oauth2": creds,
        "documentId": "1nhNcAfVLAxxh-fBTgAFVPpSH09mx0o2QGw_0BTZbSCo",
        "tableIndex": 0,
        "values": [["a1", "b1", "c1", 1, "", 2], ["a2", "b2", "c2", 1, "", 2]]
    }
    res = gdoctableapp.AppendRow(resource)
    print(res)  # You can see the retrieved responses from Docs API.


if __name__ == '__main__':
    main()