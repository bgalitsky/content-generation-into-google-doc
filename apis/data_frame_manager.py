import pandas as pd
import json
from textblob import TextBlob
from difflib import ndiff

# needed for search / from third party
def calculate_levenshtein_distance(str_1, str_2):
    """
        The Levenshtein distance is a string metric for measuring the difference between two sequences.
        It is calculated as the minimum number of single-character edits necessary to transform one string into another
    """
    distance = 0
    buffer_removed = buffer_added = 0
    for x in ndiff(str_1, str_2):
        code = x[0]
        # Code ? is ignored as it does not translate to any modification
        if code == ' ':
            distance += max(buffer_removed, buffer_added)
            buffer_removed = buffer_added = 0
        elif code == '-':
            buffer_removed += 1
        elif code == '+':
            buffer_added += 1
    distance += max(buffer_removed, buffer_added)
    return distance

#needed for question formulation
def obtainNounPhrasesFromText(txt):
    blob = TextBlob(txt)
    return blob.noun_phrases


# search is based on levenshtein_distance between questions and full records
def search(question, answerDict):
    bestKey = ""
    bestScore = 10000.0
    for k in keys:
        dist = calculate_levenshtein_distance(question, k)
        currScore = (dist+0.0)/(len(k)+0.0)
        if (currScore < bestScore):
            bestScore = currScore
            bestKey = k

    answer = answerDict[bestKey]
    print("Full answer for question: " + question)
    print(" => " + bestKey)
    print("Product name for question: " + question)
    print(" => " + answer)
    return answer

# match questions with every lookup


answerQuestions = []
df =pd.read_csv('/Users/bgalitsky/Downloads/linc-ml/product_catalog.tsv', sep='\t', header=0)

data_top = df.head()
#first get entity name
entities = pd.unique(df['category_name'])

names =  pd.unique(df['name'])
# random rows
random_rows_of_interest = [2, 53, 67]
# form questions from selected rows
for row in random_rows_of_interest:
    questions = []
    for h in data_top:
        attribute_name = h.replace('.', ' ').replace('_', ' ')
        # counting unique values
        uniq = pd.unique(df[h])
        n = len(uniq)
        #only form questions when neither too few nor too many values for this attribute
        if (n>2 & n<10):
            cellValue = df.at[row,h]
            if isinstance(cellValue, str):
                question = "Which "+entities[0]+ " have " + attribute_name + " " + cellValue + " ?"
                questions.append(question)
    # answers are product names
    answer = df.at[row, 'name']
    answerQuestions.append({ answer : questions })

# trying to get bonus points: extracting noun phrases from 'attribute.fittext', 'attribute.description'
# and forming questions from them
for row in random_rows_of_interest:
    for h in ['attribute.fittext', 'attribute.description']:
        cellValue = df.at[row, h]
        phrases = obtainNounPhrasesFromText(cellValue)
        questions = []
        for phrase in phrases:
           question = "Can you recommend a jeans with "+phrase + " ?"
        answer = df.at[row, 'name']
        answerQuestions.append({answer: questions})
# save questions
json_dump = json.dumps(answerQuestions)
with open('answersQuestions.json', 'w') as outfile:
    json.dump(json_dump, outfile)

# do indexing
keys = []
answerDict = { 'dummy': 'dummy'}
for index, row in df.iterrows():
    lookup = "";
    for h in data_top:
        cellValue = row[h]
        if isinstance(cellValue, str):
            lookup = lookup + " "+ cellValue
    keys.append(lookup)
    answerDict[lookup] = row['name']

# do four searches to demonstrate the concept of similarity between q and a
for s in range(4):
    questionAnsPairs = answerQuestions[s].items();
    ansQs = list(questionAnsPairs)[0]
    ans = ansQs[0]
    for q in range(len(ansQs[1])):
        que = ansQs[1][q] # take all questions in the list of questions. should be below the number of attributes used
        ans = search(que, answerDict)




#data_set = {"what is size?": [{"answer":["what is size", "how large"]}]}

