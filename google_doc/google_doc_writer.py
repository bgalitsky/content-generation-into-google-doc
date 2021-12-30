import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from gdoctableapppy import gdoctableapp

#https://github.com/milinddeore/google-docs-example/blob/master/google-docs-example.py
from apis.youtube_searcher import videoSearch
from bing_search.bing_img_searcher import searchBingImages


def initGoogleDocWriter():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/documents']

    # The ID of a sample document.
    DOCUMENT_ID = '1QvOrAIsgDDvLNVR3W2_KH4H12dIyslHg4Gt_XMJ8-4E'
        #'195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE'
    #https://docs.google.com/document/d/195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE/edit
    #https://docs.google.com/document/d/1kb1HCOXFGCr078pdP-gtwJy19E35dntZF5PorT0Yr7E/edit
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
    # Create a document called 'My Document'
    title = 'writing results'
    body = {'title': title}
    documentId = "1nhNcAfVLAxxh-fBTgAFVPpSH09mx0o2QGw_0BTZbSCo"
    doc = "" #service.documents().create(body=body).execute()
    return [service, documentId, creds]

def insertVideo(query, service, documentId):
    requests = []
    hits = videoSearch(query, 2)
    for videoCaption, urlYouTube, urlImage in hits:
        requests.append(
        {
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': "\n"+videoCaption+ "\n\n"
            }
        })
        requests.append(
        {
            "updateTextStyle": {
                "textStyle": {
                    "link": {
                        "url": urlYouTube
                    }
                },
                "range": {
                    "startIndex": len(videoCaption),
                    "endIndex": len(videoCaption)  + len(urlYouTube) +2
                },
                "fields": "link"
            }}
        )
        requests.append(
            {'insertInlineImage': {
                'location': {
                    'index': 1
                },
                'uri': urlImage,
                'objectSize': {
                    'height': {
                        'magnitude': 100,
                        'unit': 'PT'
                    },
                    'width': {
                        'magnitude': 100,
                        'unit': 'PT'
                    }
                }
            }})
    if len(hits)>0:
        result = service.documents().batchUpdate(documentId=documentId, body={'requests': requests}).execute()
        print(result)

def insertTable(creds):
        resource = {
            "oauth2": creds,
            "documentId": "1nhNcAfVLAxxh-fBTgAFVPpSH09mx0o2QGw_0BTZbSCo",
            "rows": 1,
            "columns": 2,
            "createIndex": 1,
            # "append": True,  # When this is used instead of "Index", new table is created to the end of Document.
            "values": [["generated sentence", "key phrases", "ground truth"], ["a2", "b2"], ["a3", "b3", "c3"]]
        }
        res = gdoctableapp.CreateTable(resource)
        print(res)  # You can see the retrieved responses from Docs API.

def insertTableRaw(creds, a1, b1, c1):
        resource = {
            "oauth2": creds,
            "documentId": "1nhNcAfVLAxxh-fBTgAFVPpSH09mx0o2QGw_0BTZbSCo",
            "tableIndex": 0,
            "values": [[a1, b1, c1]]
        }
        res = gdoctableapp.AppendRow(resource)
        print(res)  # You can see the retrieved responses from Docs API.

def insertText ( text:str, service, location:int, documentId:str):
    requests = [];
    req = {'insertText': {
        'location': {
            'index': location,
        },
        'text': text
    }}
    requests.append(req)
    result = service.documents().batchUpdate(documentId=documentId, body={'requests': requests}).execute()
    return len(text)

def insertImage(query, service, documentId):
    requests = []
    urls = searchBingImages(query)
    for u in urls:
        requests.append(
        {'insertInlineImage': {
            'location': {
                'index': 1
            },
            'uri': u,
            'objectSize': {
                'height': {
                    'magnitude': 100,
                    'unit': 'PT'
                },
                'width': {
                    'magnitude': 100,
                    'unit': 'PT'
                }
            }
        }}
        )
    if len(urls)>0:
        result = service.documents().batchUpdate(documentId=documentId, body={'requests': requests}).execute()


if __name__ == '__main__':
    serviceDoc = initGoogleDocWriter()
    #docContent(serviceDoc[0], serviceDoc[1], "text1", "text2", "text3")
    insertTable(serviceDoc[2])
    insertTableRaw(serviceDoc[2], "a11111", "b11111", "c1111111111")
    insertText("text", serviceDoc[0], 1, serviceDoc[1])