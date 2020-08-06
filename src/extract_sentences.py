import os
import re
import random
import pandas as pd
from math import floor
from data.definition import MATCHED_SENTENCES_CHECKED, SENTENCE_SIMILARITY
from data.definition import TRAIN_SENTENCE_SIMILARITY, TEST_SENTENCE_SIMILARITY, DEV_SENTENCE_SIMILARITY
from collections import OrderedDict
from nltk.corpus import stopwords
from string import punctuation
from collections import defaultdict

punctuation.replace("-", "")

def preprocess_sentence(sent):
    sent = " ".join([w for w in sent.split()])
    sent = sent.translate(str.maketrans('', '', punctuation)) # remove punctuation
    sent = ''.join([i for i in sent if not i.isdigit()]) # remove digits
    sent = sent.replace("+", " ")
    if "XXXX" in sent:
        sent = sent.replace("XXXX", " ")
    sent = re.sub(r'\s+', ' ', sent, flags=re.I)
    if sent:
        sent = sent + "."
    return sent

def randomize_files(dict_list):
    random.Random(1000).shuffle(dict_list)

def filter_sent_dict(sentence_dictionary, finding, anot_key):
    filtered_sentences = OrderedDict()
    shuffled_sentences = OrderedDict()
    if finding:
        for sk in sentence_dictionary:
            if "F-" in sk:
                if sk not in anot_key:
                    filtered_sentences[sk] = sentence_dictionary[sk]
    else:
        for sk in sentence_dictionary:
            if "I-" in sk:
                if sk not in anot_key:
                    filtered_sentences[sk] = sentence_dictionary[sk]
    keys = list(filtered_sentences.keys())
    randomize_files(keys)
    for key in keys:
        shuffled_sentences[key] = filtered_sentences[key]
    return shuffled_sentences

def preprocess_sentences_and_annotations(annotations, sentences, filename):
    keys = []
    score = []
    preprocessed_findings = []
    preprocessed_annotation = []
    sentence_dict = OrderedDict()
    annotation_dict = []

    unsimilar_sentence = []
    unsimilar_annotation = []
    
    for annot in annotations:
        annotation = annot.rstrip('\n')
        annot_key = annotation.split(': ')[1].rstrip()
        keys.append(annot_key)
        annot_value = annotation.split(': ')[0].rstrip()
        annot_value = annot_value + "."
        annot_value = annot_value.replace("/", " ")
        preprocessed_annotation.append(annot_value)
        annotation_dict.append(annot_value)
        
    for sent in sentences:
        sentence = sent.rstrip('\n')
        try:
            sent_key = sentence.split('[label]:')[1]
            value = sentence.split('[label]:')[0]
            value = preprocess_sentence(value)
            sentence_dict[sent_key] = value
        except IndexError:
            import pdb; pdb.set_trace()
            

    for idx_1, k in enumerate(keys):
        if k == "0":
            preprocessed_findings.append(annotation_dict[idx_1])
            score.append(1)
        else:
            preprocessed_findings.append(sentence_dict[k])
            score.append(1)

    for idx_2, k in enumerate(keys):
        if "F-" in k:
            for f_idx, fsk in enumerate(filter_sent_dict(sentence_dict, True, k)):
                if f_idx < 2:
                    unsimilar_sentence.append(sentence_dict[fsk])
                    unsimilar_annotation.append(annotation_dict[idx_2])
                    score.append(0)
        else:
            for i_idx, isk in enumerate(filter_sent_dict(sentence_dict, False, k)):
                if i_idx < 2:
                    unsimilar_sentence.append(sentence_dict[isk])
                    unsimilar_annotation.append(annotation_dict[idx_2])
                    score.append(0)

    preprocessed_annotation += unsimilar_annotation
    preprocessed_findings += unsimilar_sentence
    return preprocessed_annotation, preprocessed_findings, score 

def get_train_test_sets(file_list):
    split = 0.80
    dev_split = 0.1
    
    split_index = floor(len(file_list) * split)
    train = file_list[:split_index]

    split_dev_index = floor(len(file_list) * dev_split) + split_index

    dev = file_list[split_index:split_dev_index]
    test = file_list[split_dev_index:]
    return train, dev, test

def extract_sentence_and_annotation(labeled_reports):
    results = defaultdict(list)
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
 
            
            if label_findingIdx != 0 and end_of_label_findingIdx != 0:
                try:
                    prep_annotations, prep_sentences, score = preprocess_sentences_and_annotations(searchlines[annotationIdx+1:], 
                                                                                            searchlines[label_findingIdx+1:end_of_label_findingIdx-1],
                                                                                            filename)
                    assert len(prep_annotations) == len(prep_sentences)
                    assert len(prep_annotations) == len(score)
                    results["s1_col_idx"] += prep_sentences
                    results["s2_col_idx"] += prep_annotations
                    results["score_col_idx"] += score
                except IndexError:
                    import pdb; pdb.set_trace()
    
    df = pd.DataFrame(results)
 
    positive = df[df.score_col_idx == 1].reset_index(drop=True)
    negative = df[df.score_col_idx == 0].reset_index(drop=True)
    negative = negative.drop_duplicates(subset=['s1_col_idx','s2_col_idx'], keep='first').reset_index(drop=True)

    new_df = pd.concat([positive,negative],axis=0,ignore_index=True)
    df_shuffled = new_df.sample(frac=1, random_state=1).reset_index(drop=True)
    train, dev, test = get_train_test_sets(df_shuffled)

    train.to_csv(TRAIN_SENTENCE_SIMILARITY, sep="\t", index=False, header = False)
    dev.to_csv(DEV_SENTENCE_SIMILARITY, sep="\t", index=False, header = False)
    test.to_csv(TEST_SENTENCE_SIMILARITY, sep="\t", index=False, header = False)

if __name__ == "__main__":
    extract_sentence_and_annotation(MATCHED_SENTENCES_CHECKED)