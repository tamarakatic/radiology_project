import re
from collections import defaultdict
from .patterns import NOT_ANNOTATED
from .patterns import NOT_FOUND
from .patterns import SYNONYMS


# do not annotate sentence
def not_annotate_sentence(sentence):
    for word in NOT_ANNOTATED:
        if len(word.split()) > 1:
            if word in sentence.lower():
                return True
        else:
            if re.search(r'\b' + word + r'\b', sentence.lower()):
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
        more_synonyms = value.split('/')
        for syn in more_synonyms:
            if syn in sentence:
                return True
            if check_splitted_words(syn, sentence): # if there are two words not connected before/after '/'
                return True
    elif value in sentence: # if it is one word
        return True
    elif annotation in sentence:
        return True
    else: 
        if check_splitted_words(value, sentence):
            return True
                
    return False

def is_sub_word_in_synonyms(annotation):
    if len(annotation.split()) > 1:
        for word in annotation.split():
            if word in SYNONYMS:
                return True
    return False

def check_splitted_annotation(annotation, sentence):
    if len(annotation.split()) > 1:
        count_words = 0
        for word in annotation.split():
            if is_in_synonyms(word):
                if word in sentence:
                    count_words += 1
                elif check_synonyms(word, sentence):
                    count_words += 1
                else:
                    pass
        if count_words == len(annotation.split()):
            return True
    return False