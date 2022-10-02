# Used for Progress Bar
from word_embedder_v1 import WordEmbedderV1

class TagRecommenderV1(WordEmbedderV1):
    def __init__(self, ntrs_trained_glove_model_path:str = 'model/ntrs_trained_glove_model.txt'):
        super().__init__(ntrs_trained_glove_model_path)