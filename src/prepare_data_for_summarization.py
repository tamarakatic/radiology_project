import os
import re
import json
import random
from math import floor
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from collections import OrderedDict
import spacy

from data.definition import TRAIN
from data.definition import PREPROCESSED_REPORTS_JSON
from data.definition import PREPROCESSED_NO_LABEL_REPORTS_JSON

nlp = spacy.load('en_core_web_sm')
TRAIN_SENTENCES = 0

def preprocess_sentence(sent):
    sent = " ".join([w for w in sent.lower().split()])
    sent = sent.translate(str.maketrans('', '', punctuation)) # remove punctuation

    sent = ''.join([i for i in sent if not i.isdigit()]) # remove digits
    sent = sent.replace("+", " ")
    if "xxxx" in sent:
        sent = sent.replace("xxxx", " ")
    
    if sent:
        sent = sent + "."
    return sent

def preprocess_indication(sentence):
    sentence = ' '.join([sent.rstrip("\n") for sent in sentence if sent.strip() != ''])
    sentence = sentence.replace('\t', ': ')

    sentence = sentence.replace("XXXX", "").replace("-", " ")
    sentence = sentence.replace("INDICATION:", "")
    prepr_sent = []

    tokens = nlp(sentence)
    for sent in tokens.sents:
        prepr_sent.append(preprocess_sentence(sent.string))
    
    sentence = " ".join(prepr_sent)

    splitted_sentences = word_tokenize(sentence)
    return splitted_sentences

def preprocess_annotation(annotations):
    annotation = []
    keys = []
    annotation.append("ANNOTATION")
    annotation.append(":")
  
    for sent in annotations:
        sentence = sent.rstrip('\n')
        key = sentence.split(': ')[1]
        keys.append(key)
        value = sentence.split(': ')[0]
        value = value + "."
        value = value.replace("/", " / ")
        annotation += word_tokenize(value)
        
    return annotation, keys

def preprocess_labeled_sentences(sentences, keys, label):
    global TRAIN_SENTENCES
    fidings = []
    fidings.append("SENTENCES")
    fidings.append(":")
    if label:
        for key in keys:
            for sent in sentences:
                sentence = sent.rstrip('\n')
                sent_key = sentence.split('[label]:')[1]
                value = sentence.split('[label]:')[0]
                if key in sent_key:
                    fidings += word_tokenize(value)
    else:
        for sent in sentences:
            TRAIN_SENTENCES += 1
            sentence = sent.rstrip('\n')
            sent_key = sentence.split('[label]:')[1]
            value = sentence.split('[label]:')[0]
            value = preprocess_sentence(value)
            fidings += word_tokenize(value)     

    return fidings

def extract_sentence_and_annotation(labeled_reports, train, test):
    test_files = OrderedDict()
    total_indication = 0
    filltered_sentences = 0
    test_sentencens = 0
    idx = 1
    for filename in sorted(os.listdir(labeled_reports), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        with open(labeled_reports+filename, 'r') as fp:
            fp.seek(0)
            searchlines = fp.readlines()

            findingIdx = 0
            indicationIdx = 0
            label_findingIdx = 0
            end_of_label_findingIdx = 0
            annotationIdx = 0

            indication = []
            labeled_sentences = []
            annotation = []
            
            for i, line in enumerate(searchlines):
                if "INDICATION" in line:
                    indicationIdx = i
            
                if "FINDINGS" in line:
                    findingIdx = i

                if "SENTENCE LABEL" == line.rstrip('\n'):
                    label_findingIdx = i

                if "ANNOTATION WITH SENTENCE LABEL" in line:
                    end_of_label_findingIdx = i
        
                if "ANNOTATION WITH SENTENCE WITH LABELS" in line:
                    annotationIdx = i

            if filename in train:   
                if indicationIdx != 0:
                    if findingIdx != 0:
                        indication += preprocess_indication(searchlines[indicationIdx:findingIdx])
                else:
                    continue

                if indication:
                    total_indication += 1
                
                preprocess_annotations, keys = preprocess_annotation(searchlines[annotationIdx+1:])
                annotation += preprocess_annotations
                
                if label_findingIdx != 0 and end_of_label_findingIdx != 0:
                    labeled_sentences += preprocess_labeled_sentences(searchlines[label_findingIdx+1:end_of_label_findingIdx-1], keys, False)

                    
                    filltered_sentences += len(labeled_sentences)
                    report_dict = {"background": indication,
                                    "findings": labeled_sentences,
                                    "impression": annotation}

                    with open(PREPROCESSED_REPORTS_JSON, "a+") as jf:
                        json.dump(report_dict, jf)
                        jf.write('\n')
            else:
                if filename in test:
                    test_files[idx] = filename
                    idx += 1
                    if indicationIdx != 0:
                        if findingIdx != 0:
                            indication += preprocess_indication(searchlines[indicationIdx:findingIdx])
                    else:
                        continue
                    if indication:
                        total_indication += 1
                    preprocess_annotations, keys = preprocess_annotation(searchlines[annotationIdx+1:])
                    annotation += preprocess_annotations

                    if label_findingIdx != 0 and end_of_label_findingIdx != 0:
                        labeled_sentences += preprocess_labeled_sentences(searchlines[label_findingIdx+1:end_of_label_findingIdx-1], keys, False)
            
                        test_sentencens += len(searchlines[label_findingIdx+1:end_of_label_findingIdx-1])
                        report_dict_no_Lb = {"background": indication,
                                            "findings": labeled_sentences,
                                            "impression": annotation}

                        with open(PREPROCESSED_NO_LABEL_REPORTS_JSON, "a+") as jf_no_lb:
                            json.dump(report_dict_no_Lb, jf_no_lb)
                            jf_no_lb.write('\n')
    import pdb; pdb.set_trace()
                            
    print(f"---- total train sentences: {TRAIN_SENTENCES}")
    print(f"---- total FILTERED train sentences: {filltered_sentences}")
    print(f"---- total test sentences: {test_sentencens}")
    print(f"---- total indication examples: {total_indication}")                     

def randomize_files(file_list):
    random.Random(1000).shuffle(file_list)    

def get_train_test_sets(file_list):
    split = 0.90
    split_index = floor(len(file_list) * split)
    train = file_list[:split_index]

    test = file_list[split_index:]

    return train, test                      

if __name__ == '__main__':
    filename_list = []
    for filename in sorted(os.listdir(TRAIN), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        filename_list.append(filename)

    randomize_files(filename_list)
    train, test = get_train_test_sets(filename_list)
    
    preprocessed_sent = extract_sentence_and_annotation(TRAIN, train, test)