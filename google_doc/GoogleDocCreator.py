from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents']

# The ID of a sample document.
DOCUMENT_ID = '195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'
#https://docs.google.com/document/d/195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE/edit


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
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

    service = build('docs', 'v1', credentials=creds)

# Retrieve the documents contents from the Docs service.
    # document = service.documents().get(documentId=DOCUMENT_ID).execute()

    # print('The title of the document is: {}'.format(document.get('title')))


    # Create a document called 'My Document'
    title = 'My Document'
    body = {'title': title}
    doc = service.documents().create(body=body).execute()
    #docContent(service, '1mgfVE9MVe3v3ln20_dX9cMKMoF7sZYAz01kKnHzw1LE')
    createDocSection(service, '1mgfVE9MVe3v3ln20_dX9cMKMoF7sZYAz01kKnHzw1LE', "plainText", "extraText")
    print('Created document with title: {0}'.format(doc.get('title')))

def docContent(service, DOCUMENT_ID):
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': "text1"
            }
        },
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': "text2"
            }
        },
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': "text3"
            }
        },
    ]

    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()

def createDocSection(service, DOCUMENT_ID, plainText, extraText):
    requests = [
    {
        "startIndex": 1,
        "endIndex": 31,
        "paragraph": {
            "elements": [
                {
                    "startIndex": 1,
                    "endIndex": 31,
                    "textRun": {
        #                "content": "\"" +plainText+"\"\n",
                        "content": "plainText",
                        "textStyle": {
                        }
                    }
                }
            ],
            "paragraphStyle": {
                "namedStyleType": "NORMAL_TEXT",
                "direction": "LEFT_TO_RIGHT"
            }
        }
    },
    {
        "startIndex": 31,
        "endIndex": 51,
        "paragraph": {
            "elements": [
                {
                    "startIndex": 31,
                    "endIndex": 50,
                    "textRun": {
                      #  "content": "\""+extraText+"\"",
                        "content": "extraText",
                        "suggestedInsertionIds": [
                            "suggest.vcti8ewm4mww"
                        ],
                        "textStyle": {
                        }
                    }
                },
                {
                    "startIndex": 50,
                    "endIndex": 51,
                    "textRun": {
                        "content": "\n",
                        "textStyle": {
                        }
                    }
                }
            ],
            "paragraphStyle": {
                "namedStyleType": "NORMAL_TEXT",
                "direction": "LEFT_TO_RIGHT"
            }
        }
    },
    {
        "startIndex": 51,
        "endIndex": 81,
        "paragraph": {
            "elements": [
                {
                    "startIndex": 51,
                    "endIndex": 81,
                    "textRun": {
                        "content": "Text following the suggestion\n",
                        "textStyle": {
                        }
                    }
                }
            ],
            "paragraphStyle": {
                "namedStyleType": "NORMAL_TEXT",
                "direction": "LEFT_TO_RIGHT"
            }
        }
    }
    ]
    SUGGEST_MODE = "PREVIEW_WITHOUT_SUGGESTIONS"
    #result = service.documents().get(documentId=DOCUMENT_ID, suggestion_mode=SUGGEST_MODE).execute()
    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()


if __name__ == '__main__':
    main()