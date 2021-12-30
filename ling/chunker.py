import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import RegexpParser
from nltk import Tree
import pandas as pd
from textblob import TextBlob
from nltk.tokenize import sent_tokenize
import numpy as np
#nltk.download()

#https://docs.aitextgen.io/generate/

# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
chunker = RegexpParser(NP)


def get_continuous_chunks(text, chunk_func=ne_chunk):
    chunked = chunk_func(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []

    for subtree in chunked:
        if type(subtree) == Tree:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    return continuous_chunk

def obtainNounPhrasesFromText(txt):
    blob = TextBlob(txt)
    return blob.noun_phrases

def substituteMainEntity(seed:str, text:str, resList):
    seedEnties = obtainNounPhrasesFromText(seed)
    textEnties = obtainNounPhrasesFromText(text)

def buildPhrases1(texts):
# Defining a grammar & Parser
    NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
    chunkr = nltk.RegexpParser(NP)
    tokens = [nltk.word_tokenize(i) for i in texts]
    tag_list = [nltk.pos_tag(w) for w in tokens]
    phrases = [chunkr.parse(sublist) for sublist in tag_list]
    leaves = [[subtree.leaves() for subtree in tree.subtrees(filter = lambda t: t.label == 'NP')] for tree in phrases]
    leaves = [tupls for sublists in leaves for tupls in sublists]
    return leaves

def splitIntoSentences(text):
    return sent_tokenize(text);

def getFirstFragment(text):
    fragm = splitIntoSentences(text)[0];
    if len(fragm)>100:
        index = np.amax([fragm.find(","), fragm.find("-"), fragm.find(":"), fragm.find("(")])
        return fragm[:index]
    return fragm

def coverPhrase(phrase1, phrase2):
        phraseOverlap = [value for value in phrase1 if value in phrase2]
        if len(phraseOverlap) >0:
            return True
        return False

# we delete all sentences from GPT-generated sequence
#from the last to the one covered by seed (sharing common phrases)
def prune(chainList, seed):
    seedPhrases = obtainNounPhrasesFromText(seed)
    # first search in seed
    i = len(chainList);
    for sent in reversed(chainList):
        chainPhrases = obtainNounPhrasesFromText(sent)
        if coverPhrase(seedPhrases, chainPhrases ):

            return chainList[:i+1]
        i=i-1
     # now try the whole first sentence
    i = len(chainList);
    seedPhrases = obtainNounPhrasesFromText(chainList[0])
    for sent in reversed(chainList):
        chainPhrases = obtainNounPhrasesFromText(sent)
        if coverPhrase(seedPhrases, chainPhrases ):

            return chainList[:i]
        if i < 2:
            break
        i = i - 1
    # now try the whole first sentence
    i = len(chainList);
    seedPhrases = obtainNounPhrasesFromText(chainList[1])
    for sent in reversed(chainList):
        chainPhrases = obtainNounPhrasesFromText(sent)
        if coverPhrase(seedPhrases, chainPhrases):

            return chainList[:i]
        if i < 3:
            break
        i = i - 1
    #all sentrences are way off: reject this generated sequence
    return []


#res = getFirrnstFragment("Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics concerned")
#print(res)

#txt = """Natural language processing (NLP) is a field of computer science, artificial intelligence, and computational linguistics concerned with the inter
#actions between computers and human (natural) languages."""
#result = obtainNounPhrasesFromText(txt)
#print(result)

#df = pd.DataFrame({'text': ['This is a foo, bar sentence with New York city.',
#                            'Another bar foo Washington DC thingy with Bruce Wayne.']})
#df['text'].apply(lambda sent: get_continuous_chunks(sent, chunker.parse))
#print(df);