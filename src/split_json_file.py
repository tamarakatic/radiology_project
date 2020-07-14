from math import floor
from random import shuffle
import json

from data.definition import NEW_UPDATED_LABELED_REPORTS_JSON
from data.definition import TRAIN_UPDATED_SUMMARIZATION
from data.definition import TEST_UPDATED_SUMMARIZATION 
from data.definition import DEV_UPDATED_SUMMARIZATION

def randomize_files(file_list):
    shuffle(file_list)


def get_train_dev_test_sets(file_list):
    split = 0.85
    split_index = floor(len(file_list) * split)
    train = file_list[:split_index]

    # dev_split = 0.1

    # split_dev_index = floor(len(file_list) * dev_split) + split_index

    dev = file_list[split_index:]
    # test = file_list[split_dev_index:]

    return train, dev


if __name__ == '__main__':
    jsonFile = []
    for line in open(NEW_UPDATED_LABELED_REPORTS_JSON, "r"):
        jsonFile.append(json.loads(line))

    print(len(jsonFile))
    randomize_files(jsonFile)

    train, dev = get_train_dev_test_sets(jsonFile)

    with open(TRAIN_UPDATED_SUMMARIZATION, "w", encoding='utf-8') as trainJF:
        for tr in train:
            json.dump(tr, trainJF)
            trainJF.write('\n')

    with open(DEV_UPDATED_SUMMARIZATION, "w", encoding='utf-8') as devJF:
        for d in dev:
            json.dump(d, devJF)
            devJF.write('\n')

    # with open(TEST_UPDATED_SUMMARIZATION, "w", encoding='utf-8') as testJF:
    #     for te in test:
    #         json.dump(te, testJF)
    #         testJF.write('\n')
