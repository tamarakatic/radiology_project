import os
import re
import json
import random
from math import floor
from collections import Counter
from nltk.tokenize import word_tokenize
from collections import OrderedDict

from data.definition import TEST
from data.definition import SIAMESE_SEQ_FILLTERED_LABELED_REPORTS_JSON
from data.definition import SIAMESE_FILLTERED_NO_LABELED_REPORTS_JSON
from nltk.corpus import stopwords
from string import punctuation
import spacy

nlp = spacy.load('en_core_web_sm')
TRAIN_SENTENCES = 0
ZERO_COUNTERS = 0
MORE_THAN_ONE_ANOT = 0
ZERO_FILES = []

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
    
    tokenize_sent = word_tokenize(sentence)
    return tokenize_sent

def preprocess_sentences_and_annotations(annotations, sentences, train, filename):
    global TRAIN_SENTENCES
    global ZERO_COUNTERS
    global ZERO_FILES
    global MORE_THAN_ONE_ANOT
    all_annotations = []
    annot_more_than_one = 0
    keys = []
    preprocessed_findings = []
    preprocessed_annotation = []

    if not train:
        preprocessed_findings.append("SENTENCES")
        preprocessed_findings.append(":")

        preprocessed_annotation.append("ANNOTATION")
        preprocessed_annotation.append(":")

    for annot in annotations:
        annotation = annot.rstrip('\n')
        annot_key = annotation.split(': ')[1].rstrip()
        if annot_key != "0":
            keys.append(annot_key)
            annot_value = annotation.split(': ')[0]
            annot_value = annot_value + "."
            annot_value = annot_value.replace("/", " / ")
            all_annotations.append(annot_value)
    
            if not train:
                preprocessed_annotation += word_tokenize(annot_value)


    for sent in sentences:
        TRAIN_SENTENCES += 1
        sentence = sent.rstrip('\n')
        sent_key = sentence.split('[label]:')[1]
        value = sentence.split('[label]:')[0]
        value = preprocess_sentence(value)

        if not train:
            preprocessed_findings += word_tokenize(value)

        else:
            finding_sent = []
            finding_sent.append("SENTENCES")
            finding_sent.append(":")
            finding_sent += word_tokenize(value)
              
            if sent_key in keys:
                preprocessed_findings.append(finding_sent)
                annot_sent = []
                annot_sent.append("ANNOTATION")
                annot_sent.append(":")
                for idx, k in enumerate(keys):
                    if k in sent_key:
                        annot_more_than_one += 1
                        annot_sent += word_tokenize(all_annotations[idx])
                    else:
                        if k == "0":
                            if not any("Technical Quality of Image Unsatisfactory" in s for s in annotations):
                                if not any("No Indexing" in s for s in annotations):    
                                    ZERO_COUNTERS += 1
                                    ZERO_FILES.append(filename)
                preprocessed_annotation.append(annot_sent)
    if train:
        res = [k for k, v in Counter(keys).items() if v > 1]
        if res:
            MORE_THAN_ONE_ANOT += len(res)

    if ['ANNOTATION', ':'] == preprocessed_annotation:
        preprocessed_annotation = None
    return preprocessed_annotation, preprocessed_findings 


def extract_sentence_and_annotation(labeled_reports, train, test):
    filltered_sentences = 0
    test_sentencens = 0
    len_annot = []
    test_files = []
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

                if label_findingIdx != 0 and end_of_label_findingIdx != 0:
                    prep_annotations, prep_sentences = preprocess_sentences_and_annotations(searchlines[annotationIdx+1:], 
                                                                                            searchlines[label_findingIdx+1:end_of_label_findingIdx-1], 
                                                                                            True, 
                                                                                            filename)
                    filltered_sentences += len(prep_sentences)
                    assert len(prep_annotations) == len(prep_sentences)
                    for idx, sent in enumerate(prep_sentences): 
                        report_dict = {"background": indication,
                                        "findings": prep_sentences[idx],
                                        "impression": prep_annotations[idx]}
                        
                        with open(SIAMESE_SEQ_FILLTERED_LABELED_REPORTS_JSON, "a+") as jf:
                            json.dump(report_dict, jf)
                            jf.write('\n')
            else:
                if filename in test:
                    if indicationIdx != 0:
                        if findingIdx != 0:
                            indication += preprocess_indication(searchlines[indicationIdx:findingIdx])
                    else:
                        continue

                    if label_findingIdx != 0 and end_of_label_findingIdx != 0:
                        prep_annotations, prep_sentences = preprocess_sentences_and_annotations(searchlines[annotationIdx+1:], 
                                                                                                searchlines[label_findingIdx+1:end_of_label_findingIdx-1], 
                                                                                                False, 
                                                                                                filename)
                        if prep_annotations:
                            test_files.append(filename)
                            test_sentencens += len(searchlines[label_findingIdx+1:end_of_label_findingIdx-1])
                            report_dict_no_Lb = {"background": indication,
                                                "findings": prep_sentences,
                                                "impression": prep_annotations}

                            with open(SIAMESE_FILLTERED_NO_LABELED_REPORTS_JSON, "a+") as jf_no_lb:
                                json.dump(report_dict_no_Lb, jf_no_lb)
                                jf_no_lb.write('\n')

    print(test_files)
    print(sorted(list(set(ZERO_FILES)), key=lambda x: int(os.path.splitext(x)[0])))
    print(f"---- total zero label in test set: {len(list(set(ZERO_FILES)))}")
    print(f"---- total sentences with more than one annotation: {MORE_THAN_ONE_ANOT}")
    print(f"---- total train sentences: {TRAIN_SENTENCES}")
    print(f"---- total FILTERED train sentences: {filltered_sentences}")
    print(f"---- total test sentences: {test_sentencens}")

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
    for filename in sorted(os.listdir(TEST), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        filename_list.append(filename)

    randomize_files(filename_list)
    train, test = get_train_test_sets(filename_list)

    preprocessed_sent = extract_sentence_and_annotation(TEST, train, test)