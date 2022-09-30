### Stage 1 - Building Corpus ###
# Plan - query the NTRS

from os.path import exists
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

def create_ntrs_results_table(ntrs_client:NTRS_Client, query:str="", center:str="CDMS", subjectCategory:str="",page_size:int=50, total:int=150, output_ntrs_results_path:str="data/ntrs_cdms_results.csv"):
    #payload customisation
    if query != "":
        base_payload = {"q":query,"center":center, "highlight":True}
    else:
        base_payload = {"center":center, "highlight":True}
    if subjectCategory != "":
        base_payload['subjectCategory'] = subjectCategory

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

    if len(output_ntrs_results) > 0:
        if exists(output_ntrs_results_path):
            file_mode = 'a'
        else:
            file_mode = 'w'
        with open(output_ntrs_results_path, file_mode, newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, output_ntrs_results[0].keys())
            if file_mode == 'w':
                dict_writer.writeheader()
            dict_writer.writerows(output_ntrs_results)
    
    print("1.1. Completed writing file to csv")

def download_file_from_ntrs_results(ntrs_cdms_results_df:pd.DataFrame, format='pdf'):
        if format == 'pdf':
            url_column = 'downloads_pdf_url'
        elif format == 'txt':
            url_column = 'downloads_text_url'
        else:
            print("incorrect format. Expect pdf or txt")
            return
        for _, row in tqdm(ntrs_cdms_results_df.iterrows(), desc="1.2. Downloading PDF files from the downloads url extracted from 1.1."):
            pdf_file_path = 'data/pdf/' + str(row['document_id']) + f'.{format}'
            if not exists(pdf_file_path) and isinstance(row[url_column], str):
                response = ntrs_client.download_file_from_url(row[url_column])
                with open(pdf_file_path, 'wb') as pdf_writer:
                    pdf_writer.write(response.content)
                print(f'{pdf_file_path} downloaded')
            else:
                print(f'{pdf_file_path} exists')

if __name__ == '__main__':
    ntrs_client = NTRS_Client()
    queries = ['']
    output_ntrs_cdms_results_path = "data/ntrs_cdms_results.csv"

    # Metadata Download
    # nasa_scope_subject_to_category_path = "data/nasa_scope_subject_to_category.csv"
    # nasa_scope_subject_to_category_df = pd.read_csv(nasa_scope_subject_to_category_path)
    # subject_list = nasa_scope_subject_to_category_df.category.to_list()
    # for subject in subject_list:
    #     print(f'subject is: {subject}')
    #     create_ntrs_results_table(ntrs_client=ntrs_client, query="", subjectCategory=subject, total=300)

    # PDF Download from Metadata
    ntrs_cdms_results_df = pd.read_csv(output_ntrs_cdms_results_path)
    download_file_from_ntrs_results(ntrs_cdms_results_df, format='pdf')

    print("build_corpus script complete")
