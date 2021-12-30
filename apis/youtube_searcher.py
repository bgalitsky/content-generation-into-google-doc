from youtubesearchpython import VideosSearch
from difflib import ndiff

from gpt.ai_textgen import generateByAItextGen
from ling.chunker import splitIntoSentences


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

def videoSearch(query:str, count:int):
    videosSearch = VideosSearch(query, limit = count)
    results = videosSearch.result()
    r = results['result']
    output = []


    for k in range(count):
        if k>=len(r):
            break
        title = r[k]['title']
        generatedText = generateByAItextGen(title)
        # ai.generate_one(prompt=title) + "\n"

        paras =  splitIntoSentences(generatedText)

        if len(paras)>=2:
            dist = calculate_levenshtein_distance(paras[0], paras[1])+0.0
            if (dist) / len(paras[0])+0.0 < 0.3:
                generatedText = title # no generation

        videoCaption = generatedText  + "\n "+r[k]['descriptionSnippet'][0]['text']

        image = r[k]['thumbnails'][0]['url']
        posEnd = image.find("?")
        if posEnd>-1:
            image = image[:posEnd]


        print('channel = '+r[k]['channel']['name'])
        output.append([videoCaption, r[k]['link'],  image])
    return output

if __name__ == '__main__':
    results = videoSearch('sup board', 2)
    print(results)