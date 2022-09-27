### Stage 1 - Building Corpus ###
# Plan - query the NTRS


from ntrs_client import NTRS_Client

# Used for Date Extraction from String
from datetime import datetime

# Used for Progress Bar
from tqdm import tqdm

def process_citations_search_result(result):
    '''
    Data flatten the search result into a dictionary of values
    '''
    output = {
        'document_id': result['id'],
        'subjectCategories': result['subjectCategories'][0],
        'title': result['title'],
        'abstract': result['abstract'],
        'createDate': result['created'].split('T')[0],
        'publicationDate': result['publications'][0]['publicationDate'].split('T')[0],
        'downloads_pdf': "",
        'center': result['center']['code']
    }
    
    if result['downloadsAvailable'] and len(result['downloads']) > 0:
        output['downloads_pdf'] = result['downloads'][0]['links']['pdf']

    return output


if __name__ == '__main__':
    ntrs_client = NTRS_Client()

    page_size = 50
    response = ntrs_client.citations_search(
        {"center": "CDMS", "highlight": True})

    total = int(response['stats']['total'] / 1000)
    output = []
    for page_index in tqdm(range(0, total, page_size), desc="Sending through mutiple API requests to obtain document metadata"):
        if page_index + page_size > total:
            page_size = total - page_index
        payload =  {"center": "CDMS", "page": {"from": page_index, "size": page_size}, "highlight":True}
        response = ntrs_client.citations_search(payload)
        results = response['results']
        for result in results:
            output.append(process_citations_search_result(result))

    print("completed")