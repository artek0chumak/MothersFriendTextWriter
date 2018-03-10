import argparse
import os
import re
#import pymorphy2


r_alphabet = re.compile('[а-яА-Я0-9-]+|[.,:;!?]+')


def gen_token(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def gen_lines(file, lc):
    with open(file, 'r') as f:
        for line in f:
            if lc:
                yield line.lower()
            else:
                yield line


def gen_bigrams(token):
    t0 = '$'
    for t1 in token:
        yield t0, t1
        if t1 in '.!?':
            yield t1, '$'
            t0 = '$'
        else:
            t0 = t1


def first_step(args):
    lines = []
    if args.get('input_dir') is None:
        lines = input().split()
    else:
        for file in os.listdir(args['input_dir']):
            if file[-4:] == '.txt':
                lines = gen_lines(os.path.join(args['input_dir'], file), args.get('LC'))

    token = gen_token(lines)
    bigrams = gen_bigrams(token)
    print('\n'.join(['{0} {1}'.format(i[0], i[1]) for i in bigrams]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train model to generate texts.', prog='train.py')
    parser.add_argument('--lc', action='store_true', help='apply lower_case() to texts')
    parser.add_argument('--input-dir', action='store',
                        help='destination to texts. If it isn\'t set, uses texts from stdin')
    parser.add_argument('model', action='store', help='destination to model file')
    args = vars(parser.parse_args())
    first_step(args)
