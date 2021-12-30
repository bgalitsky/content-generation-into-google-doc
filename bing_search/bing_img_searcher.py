
#https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-images-api-v7-reference
# https://github.com/Azure-Samples/cognitive-services-REST-api-samples/blob/master/java/Language/TextAnalytics/src/main/java/com/microsoft/azure/textanalytics/samples/TextAnalytics.java
from bing_search import bing


def searchBingImages(query:str):
    urls = bing.fetch_image_urls(query, limit=10 ) #, file_type='png', filters='filterui:aspect-square')
    print("{} images.".format(len(urls)))
    counter = 1
#    for url in urls:
#        print("{}: {}".format(counter, url))
#        counter += 1
    return urls
