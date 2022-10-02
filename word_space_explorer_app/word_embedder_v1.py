import numpy as np
from scipy import spatial
from gensim.parsing.preprocessing import remove_stopwords
import tensorflow as tf

class WordEmbedderV1:
    def __init__(self, embedder_file_path:str= 'model/glove.6B/glove.6B.100d.txt'):
        self.embeddings_index = self.load_glove_word_embedding(embedder_file_path)
    
    # Load the pre-trained word embeddings and make a dict mapping words to their numpy vector representation
    def load_glove_word_embedding(self, embedder_file_path:str):
        embeddings_index = {}
        with open(embedder_file_path) as f:
            for line in f:
                word, coefs = line.split(maxsplit=1)
                coefs = np.fromstring(coefs, "f", sep=" ")
                embeddings_index[word] = coefs
        print("Word Embedder created with %s word vectors." % len(embeddings_index))
        return embeddings_index

    def get_sum_array_embedding(self, input_text:str):
        result_array = []
        unique_tokenised_text = set(self.tokenize(input_text))
        # analysis_total = len(unique_tokenised_text)
        # analysis_not_found = 0
        for word in unique_tokenised_text:
            if word in self.embeddings_index.keys():
                result_array.append(self.embeddings_index[word])
            else:
                # TODO - Track the words that couldnt be captured from the GloVe model -> i.e. print(f'{word} was not found in the glove model')
                # analysis_not_found = analysis_not_found + 1
                continue
        # print(f'not found percentage is {analysis_not_found/analysis_total}')
        return sum(result_array)

    def find_similar_word_from_glove_vector(self, emmbedes, distance_algo='cosine', top_n = 30):
        if distance_algo == 'euclidean':
            nearest = sorted(self.embeddings_index.keys(), key=lambda word: spatial.distance.euclidean(self.embeddings_index[word], emmbedes))
        else:
            nearest = sorted(self.embeddings_index.keys(), key=lambda word: spatial.distance.cosine(self.embeddings_index[word], emmbedes))
        if len(nearest) < top_n:
            top_n = len(nearest)
        return nearest[:top_n]

    # Helper Functions
    def get_embeddings_index(self):
        return self.embeddings_index

    def tokenize(self, input_text:str):
        filtered_text = remove_stopwords(input_text)
        return tf.keras.preprocessing.text.text_to_word_sequence(
            filtered_text,
            filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~\t\n',
            lower=True,
            split=' '
        )
