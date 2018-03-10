import argparse
import pymorphy2


def main(ns):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate text using model.', prog='generate.py')
    parser.add_argument('model', action='store', help='destination to model file')
    parser.add_argument('--seed', action='store', help='set starting word')
    parser.add_argument('length', action='store', help='length of generated text')
    parser.add_argument('--output', action='store',
                        help='destination to output file. If it isn\'t set, uses stdout')
    main(parser.parse_args())
