from math import floor
import random
import json

from data.definition import SIAMESE_SEQ_FILLTERED_LABELED_REPORTS_JSON
from data.definition import TRAIN_UPDATED_SUMMARIZATION
from data.definition import DEV_UPDATED_SUMMARIZATION

def randomize_files(file_list):
    random.Random(1000).shuffle(file_list)


def get_train_dev_test_sets(file_list):
    split = 0.89
    split_index = floor(len(file_list) * split)
    train = file_list[:split_index]

    dev = file_list[split_index:]

    return train, dev


if __name__ == '__main__':
    jsonFile = []
    for line in open(SIAMESE_SEQ_FILLTERED_LABELED_REPORTS_JSON, "r"):
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