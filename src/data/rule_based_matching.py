from collections import defaultdict
from .patterns import NOT_ANNOTATED
from .patterns import NOT_FOUND
from .patterns import SYNONYMS

# do not annotate sentence
def not_annotate_sentence(sentence):
    for word in sentence.rstrip().rstrip('.').lower().split():
        if word in NOT_ANNOTATED:
            return True
    return False
    
# if it is true label as 0 at the begining 
def zero_annotation(annotation):
    for word in NOT_FOUND:
        if word in annotation:
            return True
    return False


def check_splitted_words(value, sentence):
    count_words = 0
    if len(value.split()) > 1:
        for word in value.split():
            if word in sentence:
                count_words += 1
        if count_words == len(value.split()):
            return True

def is_in_synonyms(annotation):
    if annotation in SYNONYMS:
        return True
    return False

def check_synonyms(annotation, sentence): 
    value = SYNONYMS[annotation]
    if '/' in value:
        two_synonyms = value.split('/')
        if two_synonyms[0] in sentence or two_synonyms[1] in sentence:
            return True
        check_splitted_words(two_synonyms[0], sentence) # if there are two words not connected before '/'
        check_splitted_words(two_synonyms[1], sentence) # if there are two words not connected after '/' 
    elif value in sentence: # if it is one word
        return True
    elif annotation in sentence:
        return True
    else:
        check_splitted_words(value, sentence)
    return False