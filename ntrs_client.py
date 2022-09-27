import os
import requests


class NTRS_Client():
    def __init__(self):
        self.base_url = "https://ntrs.nasa.gov"

    def search_citations(self, payload):
        requests.post()

if __name__ == '__main__':
    ntrs_client = NTRS_Client()