import re
import pandas as pd
from nltk.tokenize import word_tokenize
from gensim.models import FastText
from gensim.models import Phrases


from data.definition import PREPROCESSED_OPENI, PREPROCESSED_MIMIC_CXR
from data.definition import OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_BIGRAM


def preprocess_text(sentence):
    tokens = word_tokenize(sentence)
    return tokens

def develop_w2v(radiology_words):
    bigram_transformer = Phrases(radiology_words)
    # trigram_transformer = Phrases(bigram_transformer[radiology_words])
    # w2v_model = FastText(trigram_transformer[bigram_transformer[radiology_words]])
    w2v_model = FastText(bigram_transformer[radiology_words], iter=10)

    w2v_model.save(OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_BIGRAM)
    print(w2v_model)

# from nltk.corpus import stopwords
# stopwords = stopwords.words('english')

if __name__ == '__main__':
    radio_senteces = open(PREPROCESSED_OPENI)
    mimic_sentences = open(PREPROCESSED_MIMIC_CXR)
    
    preprocess_corpus = []
    for sentence in radio_senteces:
        preprocess_sent = preprocess_text(sentence.rstrip())
        preprocess_corpus.append(preprocess_sent)

    for sent in mimic_sentences:
        # sentence = [w for w in sent.split() if w not in stopwords]
        preprocess_sent = preprocess_text(sent)
        preprocess_corpus.append(preprocess_sent)

    develop_w2v(preprocess_corpus)
