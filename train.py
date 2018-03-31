# -*- coding: utf-8 -*-
"""
Обучение модели для генерации текста на основоне других текстов.
Используйте -h для вызова справки.
"""
import argparse
import os
import re
from collections import Counter
import pickle

r_alphabet = re.compile('[а-яА-Я]+|[a-zA-Z]+')


def gen_token(files):
    """
    Генератор слов из файлов текстов
    :param files: Список путей к файлам
    :type files: generator
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
        # Один input - одна строка в одном файле
        if lc:
            yield [input().lower()]
        else:
            yield [input()]
    else:
        for root, dirs, files in os.walk(dest_file):
            for file in files:
                if file.endswith('.txt'):
                    yield gen_lines(os.path.join(root, file), lc)


def gen_ngramms(token, n):
    """
    Генерация n-грамм
    :param token: Генератор токена
    :param n: Количество слов в n-грамме
    :type token: generator
    :type n: int
    :return: Список из слов
    :rtype: list
    """
    it_token = iter(token)
    t = [next(it_token) for _ in range(n - 1)]
    for ti in token:
        yield t + [ti]
        t = t[1:] + [ti]


def load_model(model_dest):
    """
    Загрузка модели из файла
    :param model_dest: Расположение файла
    :type: str
    :return: Модель
    :rtype: Counter
    """
    with open(model_dest, 'rb') as f:
        return pickle.load(f)


def save_model(model, model_dest):
    """
    Сохранение модели в файл
    :param model: Модель
    :param model_dest: Расположение файла
    :type model: Counter
    :type model_dest: str
    :return: None
    """
    with open(model_dest, 'wb') as f:
        pickle.dump(model, f)


def train_model(ngramms, model_dest):
    """
    Главная функция обучения модели
    :param ngramms: Генератор n-грамм
    :param model_dest: Расположение файла модели
    :type ngramms: generator
    :type model_dest: str
    :return: None
    """
    if os.path.isfile(model_dest):
        # Обновление модели
        model = Counter(load_model(model_dest))
        model.update([tuple(i) for i in ngramms])
        save_model(model, model_dest)
    else:
        # Создание модели
        model = Counter([tuple(i) for i in ngramms])
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
    ngramms = gen_ngramms(token, args['ngramms'])
    train_model(ngramms, args['model'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Train model to generate texts.', prog='train.py')
    parser.add_argument('--lc', action='store_true',
                        help='apply lower_case() to texts')
    parser.add_argument('--input-dir', action='store',
                        help='destination to texts. If it isn'
                             '\'t set, uses texts from stdin')
    parser.add_argument('--model', action='store',
                        help='destination to model file')
    parser.add_argument('--ngramms', action='store', default=2, type=int,
                        help='number of using words in one token')
    args = vars(parser.parse_args())
    main(args)
