# Used for Progress Bar
from tqdm import tqdm
import pandas as pd

from word_embedder_v1 import WordEmbedderV1

class TagRecommenderV1(WordEmbedderV1):
    def __init__(self, ntrs_trained_glove_model_path:str = 'model/ntrs_trained_glove_model.txt'):
        super().__init__(ntrs_trained_glove_model_path)

if __name__ == '__main__':
    # Example of how Search Engine is loaded and run
    ntrs_trained_glove_model_path= 'model/ntrs_trained_glove_model.txt'
    tag_recommender_v1 = TagRecommenderV1(ntrs_trained_glove_model_path= ntrs_trained_glove_model_path)

    test_string = 'electrical engineering motors and currents'
    recommended_word_embed = tag_recommender_v1.get_sum_array_embedding(test_string)
    recommended_words = tag_recommender_v1.find_similar_word_from_glove_vector(recommended_word_embed)

    print(f'test string is: {test_string}')
    print(f' output is: {recommended_words}')