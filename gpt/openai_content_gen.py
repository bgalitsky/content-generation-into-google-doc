import re
import openai

# Load your API key from an environment variable or secret management service
#https://github.com/OthersideAI/chronology
from apis.google_know_graph_api import confirmEntityByGoogleKG
from bing_search.bing_call import searchBing
from ling.chunker import obtainNounPhrasesFromText

openai.api_key = 'YOUR KEY'
 #"A makeup for slim blonds with a dog on a leash"
 # "state of california is an extremist organization"

seed = "sup board is good for beach vacation."
response1 = seed + " "+ openai.Completion.create(engine="davinci", prompt=seed, max_tokens=500)['choices'][0]['text']

print(response1)

response2 = openai.Completion.create(engine="davinci", prompt=response1, max_tokens=500)['choices'][0]['text']

print(response2)
phrases = obtainNounPhrasesFromText(response1 + " " + response2)

print(phrases)
mainEntity = phrases[0]
for p in phrases:
    if (len(re.findall(r'\w+', p))==3):
       result = confirmEntityByGoogleKG(p)
       if result=="":
           bingResponse = searchBing(p+ " " + '\"'+mainEntity+'\"')
           for k in range(4):
               snippet = bingResponse["webPages"]["value"][k]["snippet"]
               print(snippet)
       else:
           print (p )
           print(" => ")
           print(result)