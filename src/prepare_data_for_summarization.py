import os
import re
import json
from nltk.tokenize import word_tokenize
from collections import OrderedDict

from data.definition import ALL_LABELED_REPORTS, TRAIN
from data.definition import UPDATED_ALL_LABELED_REPORTS_JSON

def preprocess_sent(sentence):
    sentence = ' '.join([sent.rstrip("\n") for sent in sentence if sent.strip() != ''])
    sentence = sentence.replace('\t', ': ')

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

def preprocess_labeled_sentences(sentences, keys):
    fidings = []
    fidings.append("SENTENCES")
    fidings.append(":")
    for key in keys:
        for sent in sentences:
            sentence = sent.rstrip('\n')
            sent_key = sentence.split('[label]:')[1]
            value = sentence.split('[label]:')[0]
            if key in sent_key:
                fidings += word_tokenize(value)

    return fidings

def extract_sentence_and_annotation(labeled_reports):
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
                # if "SENTENCE LABEL" in line:
                    label_findingIdx = i

                if "ANNOTATION WITH SENTENCE LABEL" in line:
                    end_of_label_findingIdx = i
        
                if "ANNOTATION WITH SENTENCE WITH LABELS" in line:
                    annotationIdx = i
                
            if indicationIdx != 0:
                if findingIdx != 0:
                    indication += preprocess_sent(searchlines[indicationIdx:findingIdx])
            else:
                continue

            if indication:
                preprocess_annotations, keys = preprocess_annotation(searchlines[annotationIdx+1:])
                annotation += preprocess_annotations
                
                if label_findingIdx != 0 and end_of_label_findingIdx != 0:
                    labeled_sentences += preprocess_labeled_sentences(searchlines[label_findingIdx+1:end_of_label_findingIdx-1], keys)

                    report_dict = {"background": indication,
                                    "findings": labeled_sentences,
                                    "impression": annotation}

                    with open(UPDATED_ALL_LABELED_REPORTS_JSON, "a+") as jf:
                        json.dump(report_dict, jf)
                        jf.write('\n')
                            

if __name__ == '__main__':
    preprocessed_sent = extract_sentence_and_annotation(TRAIN)