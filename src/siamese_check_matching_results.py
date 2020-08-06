import os
import re
import pandas as pd
from math import floor
from data.definition import TRAIN
from collections import OrderedDict
from nltk.corpus import stopwords
from string import punctuation
from collections import defaultdict
from sentence_transformers import SentenceTransformer, util
from data.definition import RESULTS_MATCHED_SENTENCES
from data.check_files import CHECK_FILES

# punctuation.replace("-", "")
model_save_path = RESULTS_MATCHED_SENTENCES + "Bio_ClinicalBERT-2020-07-28_20-03-24"

def preprocess_sentence(sent):
    sent = " ".join([w for w in sent.split()])
    # sent = sent.translate(str.maketrans('', '', punctuation)) # remove punctuation
    sent = ''.join([i for i in sent if not i.isdigit()]) # remove digits
    sent = sent.replace("+", " ")
    if "XXXX" in sent:
        sent = sent.replace("XXXX", " ")
    sent = re.sub(r'\s+', ' ', sent, flags=re.I) # remove empty space
    # if sent:
    #     sent = sent + "."
    return sent

def find_most_similar_sentences(corpus, queries, filename):
    embedder =  SentenceTransformer(model_save_path)
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    similar_sentences = []

    closest_n = 1
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)
        scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]

        results = zip(range(len(scores)), scores)
        results = sorted(results, key=lambda x: x[1], reverse=True)

        # print("\n\n======================\n\n")
        # print("Query:", query)
        # print("\nTop 1 most similar sentence in corpus:")
        if 'No Indexing' in query or "Technical Quality of Image Unsatisfactory" in query:
            similar_sentences.append(query)
        else:
            for idx, score in results[0:closest_n]:
                similar_sentences.append(corpus[idx].strip())
            # print(corpus[idx].strip(), f"(Score: {score:.4f})")
    return similar_sentences

def check_sentences_and_annotations(annotations, sentences, filename):
    keys = []
    score = []
    sentence_dict = OrderedDict()
    annotation_dict = []
    matched_sentence = []
    all_annotations = []
    all_sentences = []

    for sent in sentences:
        sentence = sent.rstrip('\n')
        sent_key = sentence.split('[label]:')[1]
        value = sentence.split('[label]:')[0]
        value = preprocess_sentence(value).strip()
        sentence_dict[sent_key] = value
        all_sentences.append(value)

    for annot in annotations:
        annotation = annot.rstrip('\n')
        annot_key = annotation.split(': ')[1].rstrip()
        keys.append(annot_key)
        annot_value = annotation.split(': ')[0]
        annot_value = annot_value + "."
        annot_value = annot_value.replace("/", " ")
        all_annotations.append(annot_value)
        if "0" in annot_key:
            matched_sentence.append(annot_value)
        else:
            matched_sentence.append(sentence_dict[annot_key])

    similar_sentences = find_most_similar_sentences(all_sentences, all_annotations, filename)
    if matched_sentence != similar_sentences:
        import pdb; pdb.set_trace()

def extract_sentence_and_annotation(labeled_reports, check_files):
    for filename in sorted(os.listdir(labeled_reports), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        if filename in check_files:
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
                    if "SENTENCE LABEL" == line.rstrip('\n'):
                        label_findingIdx = i

                    if "ANNOTATION WITH SENTENCE LABEL" in line:
                        end_of_label_findingIdx = i
            
                    if "ANNOTATION WITH SENTENCE WITH LABELS" in line:
                        annotationIdx = i
    
                if label_findingIdx != 0 and end_of_label_findingIdx != 0:
                    check_sentences_and_annotations(searchlines[annotationIdx+1:], 
                                                                searchlines[label_findingIdx+1:end_of_label_findingIdx-1],
                                                                filename)
               
if __name__ == "__main__":
    extract_sentence_and_annotation(TRAIN, CHECK_FILES)