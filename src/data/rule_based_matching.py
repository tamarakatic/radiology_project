from collections import defaultdict
from .patterns import NOT_ANNOTATED
from .patterns import NOT_FOUND
from .patterns import SYNONYMS

# do not annotate sentence
def annotate_sentence(sentence):
    for word in sentence.lower().split():
        if word in NOT_ANNOTATED:
            return False
    return True
    
# if it is true label as 0 at the begining 
def zero_annotation(sentence):
    for word in NOT_FOUND:
        if word in sentence:
            return True
    return False


def check_splitted_words(value, sentence):
    count_words = 0
    if len(value.split()) > 1:
        for word in value.split():
            if word in sentence:
                count_words += 1
        if count_words == len(value.split()):
            return sentence


def check_synonyms(annotation, sentence):
    for key, value in SYNONYMS:
        if annotation == key:
            if '/' in value:
                two_synonyms = value.split('/')
                if two_synonyms[0] in sentence or two_synonyms[1] in sentence:
                    return sentence
                check_splitted_words(two_synonyms[0], sentence) # if there are two words before '/'
                check_splitted_words(two_synonyms[1], sentence) # if there are two words after '/'
            elif value in sentence: # if it is one word
                return sentence
            else:
                check_splitted_words(value, sentence)