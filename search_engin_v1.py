# Prerequisit Download GloVe Model
# !wget http://nlp.stanford.edu/data/glove.6B.zip
# !unzip -q glove.6B.zip
# tutorial: https://keras.io/examples/nlp/pretrained_word_embeddings/
# https://analyticsindiamag.com/hands-on-guide-to-word-embeddings-using-glove/
# https://www.analyticsvidhya.com/blog/2019/07/how-get-started-nlp-6-unique-ways-perform-tokenization/#:~:text=NLTK%20contains%20a%20module%20called,document%20or%20paragraph%20into%20sentences
import numpy as np
from scipy import spatial
import pandas as pd

# Using Keras to perform tokenisation as it does to_lower and removes unnecessary punctuations
# Note: tokenize function has to be created to remove - from the reggex filter list because glove uses it
import tensorflow as tf

# Used for Progress Bar
from tqdm import tqdm

class SearchEngineV1:
    def __init__(self, glove_file_path:str= 'model/glove.6B.100d.txt'):
        self.embeddings_index = self.load_glove_word_embedding(glove_file_path)
    
    # Load the pre-trained word embeddings and make a dict mapping words to their numpy vector representation
    def load_glove_word_embedding(self, glove_file_path:str):
        embeddings_index = {}
        with open(glove_file_path) as f:
            for line in f:
                word, coefs = line.split(maxsplit=1)
                coefs = np.fromstring(coefs, "f", sep=" ")
                embeddings_index[word] = coefs
        print("Found %s word vectors." % len(embeddings_index))
        return embeddings_index

    def get_sum_array_glove_embedding(self, input_text:str):
        result_array = []
        for word in self.tokenize(input_text):
            if word in self.embeddings_index.keys():
                result_array.append(self.embeddings_index[word])
            else:
                # TODO - Track the words that couldnt be captured from the GloVe model -> i.e. print(f'{word} was not found in the glove model')
                continue
        return sum(result_array)

    def find_similar_word_from_glove_vector(self, emmbedes):
        nearest = sorted(self.embeddings_index.keys(), key=lambda word: spatial.distance.euclidean(self.embeddings_index[word], emmbedes))
        return nearest

    # Helper Functions
    def get_embeddings_index(self):
        return self.embeddings_index

    def tokenize(self, input_text:str):
        return tf.keras.preprocessing.text.text_to_word_sequence(
            input_text,
            filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n',
            lower=True,
            split=' '
        )

if __name__ == '__main__':

    search_engine_v1 = SearchEngineV1(glove_file_path='model/glove.6B.100d.txt')
    # ## Sample Code to run and obtain similar words
    test_string = 'nasa hackathon space app challenge HBCUs Research Conference Agenda and Abstracts 19-minute'
    emmbedes = search_engine_v1.get_sum_array_glove_embedding(test_string)
    similar_words_list = search_engine_v1.find_similar_word_from_glove_vector(emmbedes)
    
    # Obtain document vectors
    # version 1 - concat title + abstract
    output_ntrs_cdms_results_path = "data/ntrs_cdms_results.csv"
    ntrs_cdms_results_df = pd.read_csv(output_ntrs_cdms_results_path)
    ntrs_cdms_results_df = ntrs_cdms_results_df.fillna('')
    document_keys = [str(key) for key in ntrs_cdms_results_df.document_id.to_list()]
    document_title = ntrs_cdms_results_df.title.to_list()
    document_abstract = ntrs_cdms_results_df.abstract.to_list()
    document_dict = dict(zip(document_keys, [" ".join(value) for value in zip(document_title, document_abstract)]))

    for key in tqdm(document_dict):
        document_dict[key] = search_engine_v1.get_sum_array_glove_embedding(document_dict[key])

    print("test")