import os
import numpy as np
import pandas as pd
from collections import defaultdict

from sklearn.metrics import accuracy_score

from data.definition import WEIGHTS_V1, WEIGHTS_V2
from data.definition import TEST_V1, TEST_V2
from data.definition import BASELINE, HUMAN_LABELS
from data.definition import TEST_V1_PATTERN_MATCHING, TEST_V2_PATTERN_MATCHING
from data.definition import FASTTEXT_V1, FASTTEXT_V2
from data.definition import FASTTEXT_V1_PATTERN_MATCHING, FASTTEXT_V2_PATTERN_MATCHING
from data.definition import RESULTS, TEST

import warnings
warnings.filterwarnings('ignore')

with open(WEIGHTS_V1) as fsw1:
    lines_v1 = fsw1.read().splitlines()

numbers_v1 =[float(e.strip()) for e in lines_v1]

with open(WEIGHTS_V2) as fsw2:
    lines_v2 = fsw2.read().splitlines()

numbers_v2 =[int(e.strip()) for e in lines_v2]

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
    # df = pd.DataFrame(results)
    # df.to_csv(RESULTS+"labeled/{}.csv".format(file_name), index=False)
    return labels


def print_results(human_labels, machine_labels, numbers):
    acc = accuracy_score(human_labels, machine_labels, sample_weight=numbers)
    print(f"\tAccuracy: {acc:.4f}")


if __name__ == '__main__':
    human_lab = find_annotations(HUMAN_LABELS, "ANNOTATION WITH SENTENCE LABEL", "human_labels")
    machine_lab_baseline = find_annotations(BASELINE, "ANNOTATION WITH SENTENCE WITH LABELS", "baseline")

    machine_lab_v1 = find_annotations(TEST_V1, "ANNOTATION WITH SENTENCE WITH LABELS", "pure_matching_v1")
    machine_lab_v2 = find_annotations(TEST_V2, "ANNOTATION WITH SENTENCE WITH LABELS", "pure_matching_v2")

    machine_lab_rule_based_v1 = find_annotations(TEST_V1_PATTERN_MATCHING, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_pure_matching_v1")
    machine_lab_rule_based_v2 = find_annotations(TEST_V2_PATTERN_MATCHING, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_pure_matching_v2")

    machine_lab_fastText_v1 = find_annotations(FASTTEXT_V1, "ANNOTATION WITH SENTENCE WITH LABELS", "fastText_v1")
    machine_lab_fastText_v2 = find_annotations(FASTTEXT_V2, "ANNOTATION WITH SENTENCE WITH LABELS", "fastText_v2")

    machine_lab_rule_based_fastText_v1 = find_annotations(FASTTEXT_V1_PATTERN_MATCHING, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_fastText_v1")
    machine_lab_rule_based_fastText_v2 = find_annotations(FASTTEXT_V2_PATTERN_MATCHING, "ANNOTATION WITH SENTENCE WITH LABELS", "rule_based_fastText_v2")

    print("\n ----------- BASELINE ----------- ")
    print_results(human_lab, machine_lab_baseline, numbers_v1) 

    print("\n ----------- PURE MATCHING ----------- ")  
    print("\n Version 1 (Heading): ")
    print_results(human_lab, machine_lab_v1, numbers_v1)

    print("\n Version 2 (Heading + Subheadings based on Impact factor): ")
    print_results(human_lab, machine_lab_v2, numbers_v2)

    print("\n ----------- PURE MATCHING WITH RULES ----------- ")
    print("\n Version 1 (Heading): ")
    print_results(human_lab, machine_lab_rule_based_v1, numbers_v1)

    print("\n Version 2 (Heading + Subheadings based on Impact factor): ") 
    print_results(human_lab, machine_lab_rule_based_v2, numbers_v2)

    print("\n ----------- FAST TEXT ----------- ") 
    print("\n Version 1 (Heading): ")
    print_results(human_lab, machine_lab_fastText_v1, numbers_v1)

    print("\n Version 2 (Heading + Subheadings based on Impact factor): ")
    print_results(human_lab, machine_lab_fastText_v2, numbers_v2)

    print("\n ----------- FAST TEXT WITH RULES ----------- ")
    print("\n Version 1 (Heading): ") 
    print_results(human_lab, machine_lab_rule_based_fastText_v1, numbers_v1)

    print("\n Version 2 (Heading + Subheadings based on Impact factor): ")
    print_results(human_lab, machine_lab_rule_based_fastText_v2, numbers_v2)
    print()