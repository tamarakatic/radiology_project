import re
from nltk.tokenize import word_tokenize
from gensim.models import FastText, Word2Vec
from gensim.models import Phrases
from glove import Corpus, Glove
from scipy import spatial
import numpy as np


def preprocess_text(sentence):
    tokens = word_tokenize(sentence)
    return tokens

def develop_fasstext_embeddings(openI_words):
    bigram_transformer = Phrases(openI_words)
    trigram_transformer = Phrases(bigram_transformer[openI_words])

    fastText_model = FastText(trigram_transformer[bigram_transformer[openI_words]])
    fastText_model.save('models/radiology_trigram_fastText_model.txt')

def develop_word2vec_embeddings(openI_words):
    bigram_transformer = Phrases(openI_words)
    trigram_transformer = Phrases(bigram_transformer[openI_words])
    
    word2vec_model = Word2Vec(trigram_transformer[bigram_transformer[openI_words]])
    word2vec_model.save('results/openI_bigram_word2vec_model.txt')

def loadGloveModel(model_path):
    print("Loading Glove Model")
    embeddings_dict = {}
    with open(model_path, 'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    print(len(embeddings_dict)," words loaded!")
    return embeddings_dict

def find_closest_embeddings(embedding):
    return sorted(embeddings_dict.keys(), key=lambda word: spatial.distance.euclidean(embeddings_dict[word], embedding))

def get_related_terms(word2vec, token, topn=10):
    for word, similarity in word2vec.wv.most_similar(token, topn=topn):
        print("{:35} {}".format(word, round(similarity, 4)))

if __name__ == '__main__':
    # openI_sentences = open('results/radiology_sentences.txt')
    # preprocess_corpus = []
    # for sentence in openI_sentences:
    #     preprocess_sent = preprocess_text(sentence)
    #     preprocess_corpus.append(preprocess_sent)

    # develop_fasstext_embeddings(preprocess_corpus)
    # embeddings_dict = loadGloveModel("models/glove.6B/glove.6B.300d.txt")
    # print(find_closest_embeddings(embeddings_dict["lobe"])[:5])

    fastText = FastText.load('models/radiology_mimic/trigram_fasstext/radiology_trigram_fasttext_3_20_100_model.txt')
    fastText.wv.init_sims()

    import pdb; pdb.set_trace()

    # word2vec = Word2Vec.load('models/radiology_mimic/trigram_word2vec/radiology_trigram_word2vec_3_100_model.txt')
    # word2vec.wv.init_sims()

    # words = ["opacity", "lung", "cardiomegaly", "pulmonary atelectasis", "pulmonary_atelectasis", "calcinosis",
    #          "calcified granuloma", "calcified_granuloma", "thoracic vertebrae", "thoracic_vertebrae", "cicatrix", 
    #          "pleural effusion", "pleural_effusion"]


    # with open("results/similar_words_fastText_mimic.txt", 'a+') as f:
    #     for word in words:
    #         print(" *********** FastText Mimic: related terms for '{}' **********".format(word), file=f)
    #         get_related_terms(fastText, word, f)

            # print(" *********** Word2Vec Mimic: related terms for '{}' **********".format(word), file=f)
            # get_related_terms(word2vec, word, f)
