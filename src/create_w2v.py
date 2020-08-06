import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from gensim.models import FastText
from gensim.models import Phrases
import re
from nltk.stem import WordNetLemmatizer
import nltk

from data.definition import PREPROCESSED_OPENI, PREPROCESSED_MIMIC_CXR
from data.definition import PREPROCESSED_OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_UNIGRAM

# nltk.download('punkt')
# nltk.download('wordnet')

stopwords = stopwords.words('english')
stopwords.remove("not")
stopwords.remove("no")

stemmer = WordNetLemmatizer()

def preprocess_sentence(document):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', str(document))

    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)

    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)

    # Converting to Lowercase
    document = document.lower()

    # Lemmatization
    tokens = document.split()
    tokens = [stemmer.lemmatize(word) for word in tokens]
    tokens = [word for word in tokens if word not in set(stopwords)]
    # tokens = [word for word in tokens if len(word) > 2]

    preprocess_text = ' '.join(tokens)

    return preprocess_text

def preprocess_text(sentence):
    sent = sentence.translate(str.maketrans('', '', punctuation)) # remove punctuation
    sent = ''.join([i for i in sentence if not i.isdigit()]) # remove digits
    sent = preprocess_sentence(sent)

    tokens = word_tokenize(sentence)
    return tokens

def develop_w2v(radiology_words):
    # bigram_transformer = Phrases(radiology_words)
    # trigram_transformer = Phrases(bigram_transformer[radiology_words])
    # w2v_model = FastText(trigram_transformer[bigram_transformer[radiology_words]])
    w2v_model = FastText(radiology_words,
                         sg=1,
                         iter=100)

    w2v_model.save(PREPROCESSED_OPENI_AND_MIMIC_FASTTEXT_RADIOLOGY_UNIGRAM)
    print(w2v_model)


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
