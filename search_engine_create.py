from tqdm import tqdm
from word_embedder_v1 import WordEmbedderV1
import pandas as pd

def create_ntrs_word_embedder_from_glove(glove_search_engine_v1: WordEmbedderV1, input_ntrs_cdms_results_path:str = "data/ntrs_cdms_results.csv", output_ntrs_word_embedder_with_glove:str='model/ntrs_document_embedder_with_glove.txt'):
    # Obtain document vectors
    # version 1 - concat title + abstract
    ntrs_cdms_results_df = pd.read_csv(input_ntrs_cdms_results_path)
    ntrs_cdms_results_df = ntrs_cdms_results_df.fillna('')
    document_keys = [str(key) for key in ntrs_cdms_results_df.document_id.to_list()]
    document_title = ntrs_cdms_results_df.title.to_list()
    document_abstract = ntrs_cdms_results_df.abstract.to_list()
    document_dict = dict(zip(document_keys, [" ".join(value) for value in zip(document_title, document_abstract)]))

    for key in tqdm(document_dict):
        document_dict[key] = glove_search_engine_v1.get_sum_array_embedding(document_dict[key])
  
    with open(output_ntrs_word_embedder_with_glove, 'w') as f:
        for key in document_dict:
            line = key + " " + " ".join(map(str,document_dict[key].tolist()))
            f.write(line)
            f.write('\n')

if __name__ == '__main__':

    glove_search_engine_v1 = WordEmbedderV1(embedder_file_path='model/glove.6B/glove.6B.100d.txt')
    ## Sample Code to run and obtain similar words
    test_string = 'nasa hackathon space app challenge HBCUs Research Conference Agenda and Abstracts 19-minute'
    emmbedes = glove_search_engine_v1.get_sum_array_embedding(test_string)
    similar_words_list = glove_search_engine_v1.find_similar_word_from_glove_vector(emmbedes)
    
    ## Building a Document Word Embedder based on GloVe
    input_ntrs_cdms_results_path = "data/ntrs_cdms_results.csv"
    output_ntrs_word_embedder_with_glove ='model/ntrs_document_embedder_with_glove.txt'

    create_ntrs_word_embedder_from_glove(glove_search_engine_v1, input_ntrs_cdms_results_path, output_ntrs_word_embedder_with_glove)
