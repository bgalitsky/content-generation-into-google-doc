import tensorflow as tf
from transformers import GPT2LMHeadModel, GPT2Tokenizer


from bing_search.bing_call import searchBing
from ling.chunker import obtainNounPhrasesFromText, getFirstFragment

tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
#https://github.com/nicknochnack/Generating-Blog-Posts-with-GPT-2-Large/find/main
model = GPT2LMHeadModel.from_pretrained("gpt2-large", pad_token_id=tokenizer.eos_token_id)

def isNotBlank (myString):
    if myString and myString.strip():
        #myString is not None AND myString is not empty or blank
        return True
    #myString is None OR myString is empty or blank
    return False




def gpt2generate(seed):
    input_ids = tokenizer.encode(seed, return_tensors='pt')
    # generate text until the output length (which includes the context length) reaches 50
    output = model.generate(input_ids, max_length=50, num_beams=5, no_repeat_ngram_size=2, early_stopping=True)

    sentenceGener = tokenizer.decode(output[0], skip_special_tokens=True)
    sentenceGener = sentenceGener.replace('\n', ' ').strip()
    return  sentenceGener

seedSentence = 'this ski pole is good for tall guys'
#  This eye shadow brush set for active lifestyle ladies

#'this brush is good for blonds and brunettes. I have a few of these brushes and I love them '
def run():
    for i in range(1):

        sentenceGener = gpt2generate(seedSentence)
        print(sentenceGener)

        nounPhrases = obtainNounPhrasesFromText(seedSentence);
        phrase1 =  nounPhrases[0];
        bingResponse = searchBing(phrase1)
        for k in range(4):
            snippet = bingResponse["webPages"]["value"][k]["snippet"]
            snippet0 = getFirstFragment(snippet);
            snippet0Gener = gpt2generate(snippet0)
            snippet0Gener = snippet0Gener.replace(snippet0, "")
            if (isNotBlank(snippet0Gener.strip())):
                print('sn = ' +snippet)
                print(snippet0Gener)

        phrase2 =  nounPhrases[1];
        bingResponse = searchBing(phrase2)
        for k in range(4):
            snippet = bingResponse["webPages"]["value"][k]["snippet"]

            snippet0 = getFirstFragment(snippet);
            snippet0Gener = gpt2generate(snippet0)
            snippet0Gener = snippet0Gener.replace(snippet0, "")
            if (isNotBlank(snippet0Gener.strip())):
                 print('sn = '+snippet)
                 print(snippet0Gener)

#run()