import os
import re
import nltk
import numpy as np
import pandas as pd
from collections import defaultdict
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import confusion_matrix

import warnings
warnings.filterwarnings('ignore')

with open('/home/martin/Documents/radiology_project/radiology_project/src/sample_weights_v2.txt') as fsw2:
    lines_v2 = fsw2.read().splitlines()

numbers_v2 =[int(e.strip()) for e in lines_v2]

with open('/home/martin/Documents/radiology_project/radiology_project/src/sample_weights_v1.txt') as fsw1:
    lines_v1 = fsw1.read().splitlines()

numbers_v1 =[float(e.strip()) for e in lines_v1]

def find_annotations(openI_files, annotation, file_name):
    results = defaultdict(list)
    labels = []
    for filename in sorted(os.listdir(openI_files), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        with open(openI_files+filename, 'r') as fp:
                searchlines = fp.readlines()
  
                for i, line in enumerate(searchlines):
                    if annotation in line:
                        for nextLine in searchlines[i+1:]:
                            try:
                                sentence = nextLine.rstrip('\n').rstrip()
                                key = sentence.split(': ')[1]
                                value = sentence.split(': ')[0]

                                results["filename"].append(filename)
                                results["annotation"].append(value)
                                results["label"].append(key)

                                labels.append(key)
                            except IndexError:
                                import pdb; pdb.set_trace()
    df = pd.DataFrame(results)
    df.to_csv('/home/martin/Documents/radiology_project/radiology_project/results/labeled/{}.csv'.format(file_name), index=False)

    return labels
# from sklearn.utils.class_weight import compute_sample_weight
# sample_weight=compute_sample_weight(y=machine_labels)

def print_results(human_labels, machine_labels, numbers):
    acc = accuracy_score(human_labels, machine_labels, sample_weight=numbers)
    balanced_acc = balanced_accuracy_score(human_labels, machine_labels, sample_weight=numbers)
    f1 = f1_score(human_labels, machine_labels, average='weighted', labels=np.unique(machine_labels), sample_weight=numbers)
    precision = precision_score(human_labels, machine_labels, average='weighted', labels=np.unique(machine_labels), sample_weight=numbers)
    recall = recall_score(human_labels, machine_labels, average='weighted', labels=np.unique(machine_labels), sample_weight=numbers)

    print(f"\tAccuracy: {acc:.4f}")
    # print(f"\tBalanced Accuracy: {balanced_acc:.4f}")
    # print(f"\tF1 score: {f1:.4f}")

    # print(f"\tPrecision: {precision:.4f}")
    # print(f"\tRecall: {recall:.4f}")


if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))

    text_openi_file_v1 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_v1/") 
    machine_lab_v1 = find_annotations(text_openi_file_v1, "ANNOTATION WITH SENTENCE WITH LABELS", "pure_matching_v1")

    baseline_file = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_baseline/") 
    machine_lab_baseline = find_annotations(baseline_file, "ANNOTATION WITH SENTENCE WITH LABELS", "baseline")

    text_openi_file_v2 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_v2/") 
    machine_lab_v2 = find_annotations(text_openi_file_v2, "ANNOTATION WITH SENTENCE WITH LABELS", "pure_matching_v2")

    human_labeled_file = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/label_132_reports/")
    human_lab = find_annotations(human_labeled_file, "ANNOTATION WITH SENTENCE LABEL", "human_labels")

    print("\n ----------- BASELINE ----------- ")
    print_results(human_lab, machine_lab_baseline, numbers_v1) 

    print("\n ----------- PURE MATCHING ----------- ")  
    print("\n Version 1 (Heading): ")
    print_results(human_lab, machine_lab_v1, numbers_v1)

    print("\n Version 2 (Heading + Subheadings based on Impact factor): ")
    print_results(human_lab, machine_lab_v2, numbers_v2)

    print("\n ----------- PURE MATCHING WITH RULES ----------- ")
    print("\n Version 1 (Heading): ")
    rule_based_v1 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_pattern_matching_v1/") 
    machine_lab_rule_based_v1 = find_annotations(rule_based_v1, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_v1")
    print_results(human_lab, machine_lab_rule_based_v1, numbers_v1)

    print("\n Version 2 (Heading + Subheadings based on Impact factor): ")
    rule_based_v2 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_pattern_matching_v2/") 
    machine_lab_rule_based_v2 = find_annotations(rule_based_v2, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_v2")
    print_results(human_lab, machine_lab_rule_based_v2, numbers_v2)

    fastText_v1 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_fastText_v1/") 
    machine_lab_fastText_v1 = find_annotations(fastText_v1, "ANNOTATION WITH SENTENCE WITH LABELS", "fastText_v1")

    print("\n ----------- FAST TEXT ----------- ") 
    print("\n Version 1 (Heading): ")
    print_results(human_lab, machine_lab_fastText_v1, numbers_v1)

    fastText_v2 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_fastText_v2/") 
    machine_lab_fastText_v2 = find_annotations(fastText_v2, "ANNOTATION WITH SENTENCE WITH LABELS", "fastText_v2")
   
    print("\n Version 2 (Heading + Subheadings based on Impact factor): ")
    print_results(human_lab, machine_lab_fastText_v2, numbers_v2)

    print("\n ----------- FAST TEXT WITH RULES ----------- ")
    print("\n Version 1 (Heading): ")
    rule_based_fastText_v1 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_fastText_matching_v1/") 
    machine_lab_rule_based_fastText_v1 = find_annotations(rule_based_fastText_v1, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_fastText_v1")
    print_results(human_lab, machine_lab_rule_based_fastText_v1, numbers_v1)

    print("\n Version 2 (Heading + Subheadings based on Impact factor): ")
    rule_based_fastText_v2 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_fastText_matching_v2/") 
    machine_lab_rule_based_fastText_v2 = find_annotations(rule_based_fastText_v2, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_fastText_v2")
    print_results(human_lab, machine_lab_rule_based_fastText_v2, numbers_v2)
    print()