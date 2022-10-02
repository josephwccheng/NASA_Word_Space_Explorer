# Used for Progress Bar
from word_embedder_v1 import WordEmbedderV1
class SearchEngineV1:
    def __init__(self, glove_embedder_file_path:str= 'model/glove.6B/glove.6B.100d.txt', document_embedder_file_path:str='model/ntrs_document_embedder_with_glove.txt'):
        self.glove_search_engine_v1 = WordEmbedderV1(embedder_file_path=glove_embedder_file_path)
        self.document_search_engine_v1 = WordEmbedderV1(embedder_file_path=document_embedder_file_path)

    def recommend_top_documents_from_query(self, input_text:str, top_n:int=10):
        emmbedes = self.glove_search_engine_v1.get_sum_array_embedding(input_text)
        document_id_list = self.document_search_engine_v1.find_similar_word_from_glove_vector(emmbedes)
        return document_id_list[:top_n]