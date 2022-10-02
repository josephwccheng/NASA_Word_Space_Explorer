import os
import tensorflow as tf
from gensim.parsing.preprocessing import remove_stopwords
from tqdm import tqdm

def tokenize(input_text:str):
    # remove all the numbers first
    filtered_text = ''.join(i for i in input_text if not i.isdigit())
    # remove all stop words
    filtered_text = remove_stopwords(filtered_text)

    # tokenise using keras
    filtered_text = tf.keras.preprocessing.text.text_to_word_sequence(
        filtered_text,
        filters='!"#$%&()*+,./:;<=>?@[\\]^_`{|}~-•™\t\n',
        lower=True,
        split=' '
    )
    # filter out all single letter words
    filtered_text = [i for i in filtered_text if len(i) > 1]

    return filtered_text

extension = 'data/txt/'
output_text = 'data/ntrs_txt.txt'
entries = os.listdir(extension)

distinct_vocab_set = set() #Set data structure


for entry in tqdm(entries):
    with open(extension + entry) as f:
        lines = f.readlines()

    result = tokenize(" ".join(lines))

    if len(result) > 0:
        distinct_vocab_set.update(result)

    result = " ".join(result)

    with open(output_text, "a") as f:
        f.write(result + "\n")

print(f'lengh of distinct vocab is {len(distinct_vocab_set)}')