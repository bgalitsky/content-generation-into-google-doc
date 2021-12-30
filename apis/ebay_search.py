
import os
import datetime
import sys
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
#https://svcs.sandbox.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=BorisGal-products-SBX-4b0de65e6-bd594cdd&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD&keywords=iphone
#https://github.com/Brat-Pit/eBay/blob/master/eBay_api.py
#https://stackoverflow.com/questions/32198411/ebaysdk-python-authentication-failed-invalid-application
#config_file='/Users/bgalitsky/PycharmProjects/dl1/ebay.yaml',

API_KEY = "YOUR KEY"


class EbaySearchAPI(object):
    def __init__(self, api_key):
        self.api_key = API_KEY


    def fetch(self, st):
        try:
            api = Connection(appid="BorisGal-products-SBX-4b0de65e6-bd594cdd", domain = 'svcs.sandbox.ebay.com',  siteid="EBAY-US")
            response = api.execute('findItemsByKeywords', {'keywords': st})

            # The total number of items found that match the search criteria in your request
            print(f"Total items {response.reply.paginationOutput.totalEntries}\n")
            res = response.reply.searchResult._count
            if res=="0":
                return ""
            for item in response.reply.searchResult.item:
                    print(f"Title: {item.title}, Price: {item.sellingStatus.currentPrice.value}")
                    print(f"Buy it now available : {item.listingInfo.buyItNowAvailable}")
                    print(f"Country : {item.country}")
                    print(f"End time :{item.listingInfo.endTime}")
                    print(f"URL : {item.viewItemURL}")
                    try:
                        print(f"Watchers : {item.listingInfo.watchCount}\n")
                    except:
                        pass
                    return item.title
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
            return ""

    def parse(self):
        pass


# main driver
if __name__ == '__main__':




    e =  EbaySearchAPI("")
    res = e.fetch("sup board")
    e.parse()
    print(res)