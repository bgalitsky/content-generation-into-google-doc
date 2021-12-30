from __future__ import print_function
import json
import urllib

def confirmEntityByGoogleKG(query:str):
    api_key = 'YOUR KEY'
    #open('.api_key').read()

    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 1,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read())
    for element in response['itemListElement']:
        print(element['result']['name'] + ' (' + str(element['resultScore']) + ')')
        print(element['result']['@type'] )
        if (element['result']['@type'] == 'EntitySearchResult'):
            return ""
        typeNorm = None
        type = element['result']['@type']
        if isinstance(type, str):
            typeNorm = type
        else:
            typeNorm = " ".join(type)

        if 'detailedDescription' in element['result']:
            listOfDescs = element['result']['detailedDescription']['articleBody']
            descr = None
            if isinstance(listOfDescs, str):
                descr = listOfDescs
            else:
                descr = " ".join(listOfDescs)
            return  descr + " " + typeNorm
        else:
            return typeNorm
    return ""
#res = confirmEntityByGoogleKG('editorial board member')