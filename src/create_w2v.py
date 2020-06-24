import re
import pandas as pd
from nltk.tokenize import word_tokenize
from gensim.models import FastText
from gensim.models import Phrases


from data.definition import PREPROCESSED_MIMIC_CXR
from data.definition import FASTTEXT_RADIOLOGY_TRIGRAM


def preprocess_text(sentence):
    tokens = word_tokenize(sentence)
    return tokens

def develop_w2v(radlex_words):
    bigram_transformer = Phrases(radlex_words)
    trigram_transformer = Phrases(bigram_transformer[radlex_words])
    w2v_model = FastText(trigram_transformer[bigram_transformer[radlex_words]])

    w2v_model.save(FASTTEXT_RADIOLOGY_TRIGRAM)
    print(w2v_model)


if __name__ == '__main__':
    radio_senteces = open(PREPROCESSED_MIMIC_CXR)
    preprocess_corpus = []
    for sentence in radio_senteces:
        preprocess_sent = preprocess_text(sentence)
        preprocess_corpus.append(preprocess_sent)

    develop_w2v(preprocess_corpus)
