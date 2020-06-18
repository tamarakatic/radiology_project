import os
import re
import nltk
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from sklearn.metrics import precision_score, recall_score
from sklearn.metrics import confusion_matrix


def find_annotations(openI_files, annotation):

    labels = []
    for filename in sorted(os.listdir(openI_files), key=lambda x: int(os.path.splitext(x)[0])): # sort files in folder
        with open(openI_files+filename, 'r') as fp:
                searchlines = fp.readlines()
  
                for i, line in enumerate(searchlines):
                    if annotation in line:
                        for nextLine in searchlines[i+1:]:
                            try:
                                sentence = nextLine.rstrip('\n')
                                key = sentence.split(': ')[1]
                                # value = sentence.split(': ')[0]
                                labels.append(key)
                            except IndexError:
                                import pdb; pdb.set_trace()

    return labels


def print_results(human_labels, machine_labels):
    acc = accuracy_score(human_labels, machine_labels)
    f1 = f1_score(human_labels, machine_labels, average='macro', labels=np.unique(machine_labels))
    precision = precision_score(human_labels, machine_labels, average='macro', labels=np.unique(machine_labels))
    recall = recall_score(human_labels, machine_labels, average='macro', labels=np.unique(machine_labels))

    print(f"\tAccuracy: {acc:.4f}")
    print(f"\tF1 score: {f1:.4f}")

    print(f"\tPrecision: {precision:.4f}")
    print(f"\tRecall: {recall:.4f}")


if __name__ == '__main__':
    current_filepath = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(current_filepath, os.pardir))

    text_openi_file_v1 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_v1/") 
    machine_lab_v1 = find_annotations(text_openi_file_v1, "ANNOTATION WITH SENTENCE WITH LABELS")

    text_openi_file_v2 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_v2/") 
    machine_lab_v2 = find_annotations(text_openi_file_v2, "ANNOTATION WITH SENTENCE WITH LABELS")

    human_labeled_file = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/label_100_reports/")
    human_lab = find_annotations(human_labeled_file, "ANNOTATION WITH SENTENCE LABEL")

    print("\n ----------- PURE MATCHING ----------- ")  
    print("\n Version 1 (Heading): ")
    print_results(human_lab, machine_lab_v1)

    print("\n Version 2 (Heading + Subheadings): ")
    print_results(human_lab, machine_lab_v2)

    fastText_v1 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_fastText_v1/") 
    machine_lab_fastText_v1 = find_annotations(fastText_v1, "ANNOTATION WITH SENTENCE WITH LABELS")

    print("\n ----------- FAST TEXT ----------- ") 
    print("\n Version 1 (Heading): ")
    print_results(human_lab, machine_lab_fastText_v1)

    fastText_v2 = os.path.join(root_path, "/home/martin/Documents/radiology_project/radiology_project/data/openITest_Train/test_fastText_v2/") 
    machine_lab_fastText_v2 = find_annotations(fastText_v2, "ANNOTATION WITH SENTENCE WITH LABELS")
   
    print("\n Version 2 (Heading + Subheadings): ")
    print_results(human_lab, machine_lab_fastText_v2)