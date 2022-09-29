### Stage 1 - Building Corpus ###
# Plan - query the NTRS


from ntrs_client import NTRS_Client
# Used for Date Extraction from String
from datetime import datetime
# Used for Progress Bar
from tqdm import tqdm
# Saving data in CSV
import csv

# Dataframe
import pandas as pd

def process_citations_search_result(result):
    '''
    Data flatten the search result into a dictionary of values
    '''
    output = {
        'document_id': result['id'],
        'subjectCategories': "",
        'title': result['title'],
        'abstract': "",
        'createDate': result['created'].split('T')[0],
        'publicationDate': "",
        'downloads_pdf_url': "",
        'downloads_text_url': "",
        'center': result['center']['code'],
        'copyright': result['copyright']['determinationType'],
        'related': ""
    }
    if result['downloadsAvailable'] and len(result['downloads']) > 0:
        output['downloads_pdf_url'] = result['downloads'][0]['links']['pdf']
        output['downloads_text_url'] = result['downloads'][0]['links']['fulltext']
    related_list = []
    if len(result['related']) > 0:
        for related in result['related']:
            if 'id' in list(related.keys()):
                related_list.append(related['id'])
    output['related'] = ','.join(map(str, related_list))
    if 'abstract' in list(result.keys()):
        output['abstract'] = result['abstract']
    if 'publications' in list(result.keys()) and len(result['publications']) > 0:
        output['publicationDate'] = result['publications'][0]['publicationDate'].split('T')[0]
    if 'subjectCategories' in list(result.keys()) and len(result['subjectCategories']) > 0:
        output['subjectCategories'] = result['subjectCategories'][0]
    return output

def create_ntrs_results_table(ntrs_client:NTRS_Client, query="", center="CDMS",page_size:int=50, total:int=5000):
    # output file location
    if query != "":
        output_ntrs_results_path = f'data/ntrs_{query}_{center.lower()}_results.csv'
        base_payload = {"q":query,"center":center, "highlight":True}
    else:
        output_ntrs_results_path = f'data/ntrs_{center.lower()}_results.csv'
        base_payload = {"center":center, "highlight":True}

    # Response Total Check
    response = ntrs_client.citations_search(base_payload)
    if int(response['stats']['total']) < total:
        total = int(response['stats']['total'])
        print("total from query filter is less than input value")
    output_ntrs_results = []
    for page_index in tqdm(range(0, total, page_size), desc="1.1. Sending through mutiple API requests to obtain document metadata"):
        if page_index + page_size > total:
            page_size = total - page_index
        base_payload['page'] =  {"from": page_index, "size": page_size}
        response = ntrs_client.citations_search(base_payload)
        results = response['results']
        for result in results:
            output_ntrs_results.append(process_citations_search_result(result))

    with open(output_ntrs_results_path, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, output_ntrs_results[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(output_ntrs_results)
    
    print("1.2. Completed writing file to csv")

def download_pdf_from_ntrs_results(ntrs_cdms_results_df:pd.DataFrame):
    for _, row in tqdm(ntrs_cdms_results_df.iterrows(), desc="1.2. Downloading PDF files from the downloads url extracted from 1.1."):
        pdf_file_path = 'data/pdf/' + str(row['document_id']) + '.pdf'
        if isinstance(row['downloads_pdf_url'], str): 
            response = ntrs_client.download_file_from_url(row['downloads_pdf_url'])
            with open(pdf_file_path, 'wb') as pdf_writer:
                pdf_writer.write(response.content)

if __name__ == '__main__':
    ntrs_client = NTRS_Client()
    output_ntrs_cdms_results_path = "data/ntrs_cdms_results.csv"
    queries = ['']
    create_ntrs_results_table(ntrs_client=ntrs_client, query="")
    #ntrs_cdms_results_df = pd.read_csv(output_ntrs_cdms_results_path)
    #download_pdf_from_ntrs_results(ntrs_cdms_results_df)

    print("build_corpus script complete")
