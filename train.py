"""Программа для обучения модели программы генерации текстов. Реализация модели - через биграммы, ввод данных - через
терминал(stdin) или через документы в папке. Модель сохраняется через модуль Pickle."""

import argparse
import os
import re
import pickle
from collections import Counter


r_alphabet = re.compile('[а-яА-Я0-9]+|[-.,:;!?]+')


def gen_token(files):
    """Generator to find all words in texts"""
    for file in files:
        for line in file:
            for token in r_alphabet.findall(line):
                yield token


def gen_lines(file, lc):
    """Generator to find all lines in the texts"""
    with open(file, 'r') as f:
        for line in f:
            if lc:
                yield line.lower()
            else:
                yield line


def gen_files(input_dir, lc):
    """Generator to find files in a folder"""
    if input_dir is None:
        return [[input()]]
    else:
        return [gen_lines(os.path.join(input_dir, file), lc) for file in os.listdir(input_dir) if file[-4:] == '.txt']


def gen_bigrams(token):
    """Generator to create bigrams from words"""
    t0 = '$'
    for t1 in token:
        yield t0, t1
        if t1 in '.!?':
            yield t1, '$'
            t0 = '$'
        else:
            t0 = t1


def gen_model(bigrams):
    """Count words to create bigrams model"""
    p_model = Counter(i for i in bigrams)
    # Return dict from word to words(i[1]) with their frequences in texts(p_model)
    return {(i[0], i[1]): p_model[(i[0], i[1])] for i in p_model}


def update_model(model, bigrams):
    """Update model, if it exists"""
    u_model = Counter(i for i in bigrams)
    for i in u_model:
        if i in model:
            model[(i[0], i[1])] += u_model[i]
        else:
            model[(i[0], i[1])] = u_model[i]

    return model


def load_model(model_dest):
    """Load model from file"""
    with open(model_dest, 'rb') as f:
        return pickle.load(f)


def save_model(model, model_dest):
    """Save model to file"""
    with open(model_dest + '.model', 'wb') as f:
        pickle.dump(model, f)


def train_model(bigrams, model_dest):
    """Main function for model"""
    if model_dest is None:
        # create model, if it doesn't exist
        model = gen_model(bigrams)
        model_dest = input("Write destination for model file:\n")
        save_model(model, model_dest)
    else:
        # train model, if it exists
        model = load_model(model_dest)
        model = update_model(model, bigrams)
        save_model(model, model_dest)


def main(args):
    """Main function to train model"""
    # find files
    files = gen_files(args['input_dir'], args['lc'])
    # find words in files
    token = gen_token(files)
    # create bigrams
    bigrams = gen_bigrams(token)
    # train or create model using bigrams
    train_model(bigrams, args['model'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train model to generate texts.', prog='train.py')
    parser.add_argument('--lc', action='store_true', help='apply lower_case() to texts')
    parser.add_argument('--input-dir', action='store',
                        help='destination to texts. If it isn\'t set, uses texts from stdin')
    parser.add_argument('--model', action='store', help='destination to model file')
    args = vars(parser.parse_args())
    main(args)
