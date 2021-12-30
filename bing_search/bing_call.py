#Copyright (c) Microsoft Corporation. All rights reserved.
#Licensed under the MIT License.

# -*- coding: utf-8 -*-

import json
import os
from pprint import pprint
import requests

def searchBing(query):

# Add your Bing Search V7 subscription key and endpoint to your environment variables.
    subscription_key = 'YOUR KEY'
    endpoint = "https://api.bing.microsoft.com/v7.0/search"

# Query term(s) to search for.
# query = "deepest cave in the world"

# Construct a request
    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt }
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }

# Call the API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        #print("\nHeaders:\n")
        #print(response.headers)

        #print("\nJSON Response:\n")
        #pprint(response.json())
        return response.json()
    except Exception as ex:
        raise ex

# rows = "\n".join(["""<tr>
#                           <td><a href=\"{0}\">{1}</a></td>
#                           <td>{2}</td>
#                         </tr>""".format(v["url"], v["name"], v["snippet"])
 #                     for v in bingResponse ["webPages"]["value"]])
#    HTML("<table>{0}</table>".format(rows))
#    print(rows)