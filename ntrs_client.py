# Nasa Technical Reports Server API CLient #
# Author: Joseph Cheng #
# Date: 27/09/2022
# Purpose: to extract research articles from the report servers that contains pdf files

import requests

class NTRS_Client():
    def __init__(self):
        self.base_url = "https://ntrs.nasa.gov"

    def citations_search(self, payload):
        ''' Payload Information:
            Example: {"center": "CDMS"}
            Center: "center": "CDMS"
            Pagination: "page": {"size":50,"from":0}
            Query: "q": "mars"
            Keyword: "keyword": "SUPERHETERODYNE RECEIVER"
        '''
        response = requests.post(self.base_url + '/api/citations/search', json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(
                "Recieved response code: {}. Error body: {}".format(response.status_code, response.json())
            )
    def download_file_from_url(self, download_url:str):
        response = requests.get(self.base_url + download_url + "?attachment=true")
        if response.status_code == 200:
            return response
        else:
            raise ValueError(
                "Recieved response code: {}. Error body: {}".format(response.status_code, response.json())
            )
    