import re
import sys
import openai
from googleapiclient.errors import HttpError

from apis.google_know_graph_api import confirmEntityByGoogleKG
from bing_search.bing_call import searchBing
from ling.chunker import *

from google_doc.google_doc_writer import initGoogleDocWriter, insertTable, insertImage, insertVideo, insertText, \
    insertTableRaw

openai.api_key = 'YOUR KEY'
#https://docs.google.com/document/d/1nhNcAfVLAxxh-fBTgAFVPpSH09mx0o2QGw_0BTZbSCo/edit
#https://console.cloud.google.com/apis/credentials?project=utility-braid-334419

def generateText(seed:str):
    return seed + " "+ openai.Completion.create(engine="davinci", prompt=seed, max_tokens=100)['choices'][0]['text']

def cgRun(seed):
    serviceDoc = initGoogleDocWriter()
    insertTable(serviceDoc[2])


    response1 = seed + " "+ openai.Completion.create(engine="davinci", prompt=seed, max_tokens=500)['choices'][0]['text']

    print(response1)

    response2 = openai.Completion.create(engine="davinci", prompt=response1, max_tokens=500)['choices'][0]['text']

    print(response2)
    genText = response1 + " " + response2

    # cleaning auto text
    #fixing boat.Next -> boat. Next
    genText = re.sub('[a-z]\.[A-Z]', '[a-z]\. [A-Z]', genText)

    #split into paragraphs
    paragraphs = genText.split("\n\n")
    mainEntity = obtainNounPhrasesFromText(paragraphs[0])[0]

    for p in paragraphs:
        if len(p)<80 or p.startswith('Written'):
            paragraphs.remove(p)

    for para in paragraphs:
        phrases = obtainNounPhrasesFromText(para)

        backgroundTexts = []
        # shortlist phrases
        reducedPhrases = []
        for p in phrases:
            if (len(re.findall(r'\w+', p)) >= 3 and len(p) > 9):
                reducedPhrases.append(p)
        if len(reducedPhrases) < 2:
            for p in phrases:
                if (len(re.findall(r'\w+', p)) == 2 and len(p) > 9):
                    reducedPhrases.append(p)

        for p in reducedPhrases:
            backgroundText = ""
            result = confirmEntityByGoogleKG(p)
            if result=="":
                bingResponse = searchBing(p+ " " + '\"'+mainEntity+'\"')
                for k in range(4):
                    snippet = bingResponse["webPages"]["value"][k]["snippet"]
                    backgroundText += snippet + "\n"
            else:
                if isinstance(result, str):
                    backgroundText += p + " => " + result
                else:
                    backgroundText += p + " => " + result[0]
                backgroundTexts.append(backgroundText)
            try:
                insertImage(p + " " + mainEntity, serviceDoc[0], serviceDoc[1])
                insertVideo(p + " " + '\"' + mainEntity + '\"', serviceDoc[0], serviceDoc[1])
            except (RuntimeError, TypeError, NameError, ValueError, HttpError) as e:
                print("Problem inserting images and videos")
                print(e)

        insertText(para+"\n\n", serviceDoc[0], 1, serviceDoc[1])
        insertTableRaw(serviceDoc[2], para, '-'.join(phrases),  '\n '.join(backgroundTexts))

    return serviceDoc[0]

if __name__ == '__main__':
    seed = "sup board is good for beach vacation."
    googleDoc = cgRun(seed)
