from aitextgen import aitextgen

#factsumm = FactSumm()
#https://stackoverflow.com/questions/49440282/python-3-tkinter-notepad-cut-and-copy
#https://www.youtube.com/watch?v=8uaDoMuDK6E
from bing_search.bing_call import searchBing
from entities.fact_checker import substituteValue
from ling.chunker import splitIntoSentences, prune


def generateByAItextGen(seed: str):
    ai = aitextgen()
    return ai.generate_one(prompt=seed)

def contentGen(seed, locationAttr):
    # Without any parameters, aitextgen() will download, cache, and load the 124M GPT-2 "small" model
    ai = aitextgen()

    #seed = "brush makeup for blonds"

    #ai.generate()
    #ai.generate(n=3, max_length=100)
    reducedVerified=[]
    while len(reducedVerified)<1:
        text = ai.generate_one(prompt=seed)
        #result1 = ai.generate_to_file(n=10, prompt="brush makeup for blonds", max_length=100, temperature=1.2)

        resList = splitIntoSentences(text)
        for i, sent in enumerate(resList):
            resList[i] =  substituteValue( resList[i], locationAttr)
        reducedVerified =prune(resList , seed)


    resPlusBingList = resList.copy()
    for sent in reducedVerified:
        bingResponse = searchBing(sent)
        for k in range(4):
            snippet = bingResponse["webPages"]["value"][k]["snippet"]

            for i in range(len(resPlusBingList)):
                if resPlusBingList[i] == sent:
                    resPlusBingList.insert(i+1, snippet)
                    break
    return  '.\n'.join(resPlusBingList)
if __name__ == '__main__':
    contentGen("red shoes for girls", "Karl Jones works at Recreational Equipment Inc in Kanab ")