### Stage 1 - Building Corpus ###
# Plan - query the NTRS


from ntrs_client import NTRS_Client
# Used for Date Extraction from String
from datetime import datetime
# Used for Progress Bar
from tqdm import tqdm
# Saving data in CSV
import csv

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
        'center': result['center']['code'],
        'copyright': result['copyright']['determinationType'],
        'related': ""
    }
    
    if result['downloadsAvailable'] and len(result['downloads']) > 0:
        output['downloads_pdf'] = result['downloads'][0]['links']['pdf']

    related_list = []
    if len(result['related']) > 0:
        for related in result['related']:
            if 'id' in list(related.keys()):
                related_list.append(related['id'])
    output['related'] = ','.join(map(str, related_list))

    return output


if __name__ == '__main__':
    ntrs_client = NTRS_Client()
    # Constants 
    page_size = 50
    response = ntrs_client.citations_search(
        {"center": "CDMS", "highlight": True})
    total = int(response['stats']['total'] / 1000)
    output_ntrs_cdms_results = []
    output_ntrs_cdms_results_path = "data/ntrs_cdms_results.csv"

    for page_index in tqdm(range(0, total, page_size), desc="1.1. Sending through mutiple API requests to obtain document metadata"):
        if page_index + page_size > total:
            page_size = total - page_index
        payload =  {"center": "CDMS", "page": {"from": page_index, "size": page_size}, "highlight":True}
        response = ntrs_client.citations_search(payload)
        results = response['results']
        for result in results:
            output_ntrs_cdms_results.append(process_citations_search_result(result))

    with open(output_ntrs_cdms_results_path, 'w') as f:
        dict_writer = csv.DictWriter(f, output_ntrs_cdms_results[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(output_ntrs_cdms_results)
    print("1.2. Completed writing file to csv")