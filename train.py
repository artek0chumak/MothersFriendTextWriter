"""
Обучение модели для генерации текста на основоне других текстов.
Используйте -h для вызова справки.
"""
import argparse
import os
import re
from collections import Counter
import pickle

r_alphabet = re.compile('[а-яА-Я0-9]+|[-.,:;!?]+')


def gen_token(files):
    """
    Генератор слов из файлов текстов
    :param files: Список путей к файлам
    :type files: list
    :return: Слово из файла
    :rtype: str
    """
    for file in files:
        for line in file:
            for token in r_alphabet.findall(line):
                yield token


def gen_lines(file, lc):
    """
    Генератор строк из файла
    :param file: Путь к файлу
    :param lc: Флаг на использование lower
    :type file: str
    :type lc: bool
    :return: Строку из файла
    :rtype: str
    """
    with open(file, 'r') as f:
        for line in f:
            if lc:
                yield line.lower()
            else:
                yield line


def open_files(dest_file, lc):
    """
    Созданиие списка строк
    :param dest_file: Путь к файлу
    :param lc: Флаг на использование lower
    :type dest_file: str
    :type lc: bool
    :return: Список файлов, т.е. список строк
    :rtype: list
    """
    if dest_file is None:
        #Один input - одна строка в файле
        return [[input()]]
    else:
        return [gen_lines(os.path.join(dest_file, file), lc) for file in os.listdir(dest_file) if file[-4:] == '.txt']


def gen_ngrams(token, n):
    """
    Генерация n-грамм
    :param token: Генератор токена
    :param n: Количество слов в n-грамме
    :type token: generator
    :type n: int
    :return: Список из слов
    :rtype: list
    """
    t = ['$' for _ in range(n - 1)]
    for ti in token:
        yield t + [ti]
        if ti in '.!?':
            for i in range(1, n - 1):
                yield t[i:] + [ti] + ['$'] * i

            t = ['$' for _ in range(n - 1)]
        else:
            t = t[1:] + [ti]


def gen_model(ngrams):
    """
    Генерация модели
    :param ngrams: Генератор n-грамм
    :type ngrams: generator
    :return: Словарь из n-граммы в частоту распределения
    """
    p_model = Counter([tuple(i) for i in ngrams])
    return {i: p_model[i] for i in p_model}


def update_model(model, ngrams):
    """
    Обновление модели
    :param model: Модель
    :param ngrams: Генератор n-грамм
    :type model: dict
    :type ngrams: generator
    :return: Обновленная модель
    :rtype: dict
    """
    u_model = Counter(tuple(ngrams))
    for i in u_model:
        if i in model:
            model[i] += u_model[i]
        else:
            model[i] = u_model[i]

    return model


def load_model(model_dest):
    """
    Загрузка модели из файла
    :param model_dest: Расположение файла
    :type: str
    :return: Модель
    :rtype: dict
    """
    with open(model_dest, 'rb') as f:
        return pickle.load(f)


def save_model(model, model_dest):
    """
    Сохранение модели в файл
    :param model: Модель
    :param model_dest: Расположение файла
    :type model: dict
    :type model_dest: str
    :return: None
    """
    with open(model_dest, 'wb') as f:
        pickle.dump(model, f)


def train_model(ngrams, model_dest):
    """
    Главная функция обучения модели
    :param ngrams: Генератор n-грамм
    :param model_dest: Расположение файла модели
    :type ngrams: generator
    :type model_dest: str
    :return: None
    """
    if model_dest is None:
        model = gen_model(ngrams)
        model_dest = input("Write destination for model file:\n")
        save_model(model, model_dest)
    else:
        model = load_model(model_dest)
        model = update_model(model, ngrams)
        save_model(model, model_dest)


def main(args):
    """
    Главная функция
    :param args: Аргументы запуска обучения
    :type args: dict
    :return: None
    """
    files = open_files(args['input_dir'], args['lc'])
    token = gen_token(files)
    ngrams = gen_ngrams(token, args['ngrams'])
    train_model(ngrams, args['model'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train model to generate texts.', prog='train.py')
    parser.add_argument('--lc', action='store_true', help='apply lower_case() to texts')
    parser.add_argument('--input-dir', action='store',
                        help='destination to texts. If it isn\'t set, uses texts from stdin')
    parser.add_argument('--model', action='store', help='destination to model file')
    parser.add_argument('--ngrams', action='store', default=2, type=int, help='number of using words in one token')
    args = vars(parser.parse_args())
    main(args)
