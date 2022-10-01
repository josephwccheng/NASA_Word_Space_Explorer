# Used for Progress Bar
from tqdm import tqdm
from os.path import exists

from word_embedder_v1 import WordEmbedderV1
import pandas as pd

class SearchEngineV1:
    def __init__(self, glove_embedder_file_path:str= 'model/glove.6B.100d.txt', document_embedder_file_path:str='data/ntrs_word_embedder_with_glove.txt'):
        self.glove_search_engine_v1 = WordEmbedderV1(embedder_file_path=glove_embedder_file_path)
        self.document_search_engine_v1 = WordEmbedderV1(embedder_file_path=document_embedder_file_path)

    def recommend_top_documents_from_query(self, input_text:str, top_n:int=100):
        emmbedes = self.glove_search_engine_v1.get_sum_array_embedding(input_text)
        document_id_list = self.document_search_engine_v1.find_similar_word_from_glove_vector(emmbedes)
        return document_id_list[:top_n]
if __name__ == '__main__':
    glove_embedder_file_path= 'model/glove.6B.100d.txt'
    document_embedder_file_path='data/ntrs_word_embedder_with_glove.txt'
    search_engine_v1 = SearchEngineV1(glove_embedder_file_path=glove_embedder_file_path, document_embedder_file_path=document_embedder_file_path)

    test_string = 'Preliminary Results of Flight Tests of a Conventional Three-Blade Propeller at High Speeds'
    recommended_document_list = search_engine_v1.recommend_top_documents_from_query(test_string)

    # Validate the Recommder
    # input_ntrs_cdms_results_path = "data/ntrs_cdms_results.csv"
    # ntrs_cdms_results_df = pd.read_csv(input_ntrs_cdms_results_path)
    # validate_list = []
    # count = 0
    # for document_id, title, abstract in tqdm(zip(ntrs_cdms_results_df.document_id.tolist(),ntrs_cdms_results_df.title.tolist(), ntrs_cdms_results_df.abstract.tolist())):
    #     recommended_document_list = search_engine_v1.recommend_top_documents_from_query(title + " " + abstract)
    #     if str(document_id) in recommended_document_list:
    #         validate_list.append(recommended_document_list.index(str(document_id)))
    #     count = count + 1
    #     if count > 100:
    #         break
    print("test")