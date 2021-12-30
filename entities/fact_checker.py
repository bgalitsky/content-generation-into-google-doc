from factsumm import FactSumm

from bing_search.bing_call import searchBing

factsumm = FactSumm()
#article = "Lionel Andrés Messi (born 24 June 1987) is an Argentine professional footballer who plays as a forward and captains both Spanish club Barcelona and the Argentina national team. Often considered as the best player in the world and widely regarded as one of the greatest players of all time, Messi has won a record six Ballon d'Or awards, a record six European Golden Shoes, and in 2020 was named to the Ballon d'Or Dream Team."
#summary = "Lionel Andrés Messi (born 24 Aug 1997) is an Spanish professional footballer who plays as a forward and captains both Spanish club Barcelona and the Spanish national team."
#article = "Ski Poles are a great way to keep your feet warm and dry in the winter"
#summary = "Waterproof ski gloves sold by RAI in Seattle or mittens are a must to keep your hands dry and warm."


def substituteValue(sentence:str, seed:str)->str:
    [source_ents, summary_ents, fact_score] = factsumm.extract_facts(sentence, seed, verbose=False)
    print(source_ents)
    sentencePoss = source_ents[0]
    seedPoss = summary_ents[0]
    for nodeSent in sentencePoss:
        for nodeSeed in seedPoss:
            if nodeSent['entity'] == nodeSeed['entity']:
                sentence = sentence.replace(nodeSent['word'], nodeSeed['word'])

    return sentence

fact = "SPLC inspired Omar Mateen" # to commit mass murder."

def substituteValuesByWebMining(fact):
    bingResponse = searchBing(fact)
    for k in range (7):
        snippet = bingResponse["webPages"]["value"][k]["snippet"]
        result = substituteValue(fact, snippet)
        if (result != fact):
            return result
    return ""

if __name__ == '__main__':
    print(substituteValuesByWebMining(fact))

#factsumm(article, summary, verbose=True)


#[source_ents, summary_ents, fact_score] = factsumm.extract_facts(article, summary, verbose=False)
    article = "somewhere of recreation and comfort, somewhere that was out of the way of \u201call the dangers\u201d as Kodwo Eshun used to say. On my blog I write about ideas on how to live, and there are blogposts about this place called the Catac"
   # "The victim, who has been identified as 41-year-old John F. DeSoto, was shot to death Tuesday night 6 miles north of New York City in the 6300 block of Cottondale Crescent Str."
    summary  = "Karl Jones works at Recreational Equipment Inc in Kanab and lives at Polk Middle Str with his mom"
#res =substituteValue(article, summary)
#print(res)

    #"The best part of our shop is that we have a wide selection of local merchants from all over Oakland, and we have some great deals that are not only online but also in the stores.",
     #           "shoes shop in Kanab")

