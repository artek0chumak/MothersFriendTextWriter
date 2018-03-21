# -*- coding: utf-8 -*-
"""
Генератор текста из модели, полученной обучением с помощью train.py.
Используйте -h для вызова справки.
"""
import argparse
import random
import pickle
from collections import Counter


def load_model(dest_model):
    """
    Загрузка модели из файла
    :param dest_model: Расположение файла модели
    :type dest_model: str
    :return: Словарь кортежа слов в частоты
    :rtype: Counter
    """
    with open(dest_model, 'rb') as f:
        return pickle.load(f)


def weighted_choices(choices):
    """
    Куммулятивное распределение
    :param choices: Последовательность слов и их частоты
    :type choices: list or tuple
    :return: Выбранное слово
    :rtype: str or None
    """
    # c - слово, w - вес
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

    return None


def generate_text(model, length, seed):
    """
    Генерация текста
    :param model: Модель текстов
    :param length: Длина текста в словах(знаки пунктуации считаются за слова)
    :param seed: Начальное слово
    :type model: Counter
    :type length: int
    :type seed: str
    :return: Генератор слов
    :rtype: generator
    """
    # Нахождение числа слов в n-грамме
    l_ngrams = len(next(iter(model)))
    # Список без слов
    e_list = ['$' for _ in range(l_ngrams - 1)]

    if (seed not in set(i[0] for i in model)) and (seed is not None):
        seed = None
    if seed is None:
        seed = random.choice(tuple(i[-1] for i in model if list(i[:-1]) == e_list))
    t = e_list[1:] + [seed]

    # Первое слово
    yield seed

    while length > 0:
        # Выбор нужного слова на основе n-1 предыдущих
        temp = weighted_choices(tuple((i[-1], model[i]) for i in model if list(i[:-1]) == t))
        if temp is None:
            # Выбор нового слова, если не удалось найти подходящий по последним
            temp = random.choice(tuple(i[-1] for i in model if list(i[:-1]) == e_list))
        # Проверка на знак пунктуации, так как length - количество слов
        if temp not in '-.,!?;':
            length -= 1

        # Удаляем первое слово, так как оно больше нам не нужно
        t = t[1:] + [temp]
        yield temp


def create_text(t):
    """
    Создает текст из списка слов
    :param t: Генератор слов
    :type t: generator
    :return: Сгенерированный текст
    :rtype: str
    """
    text = ''
    for i in t:
        if i in '-.,!?;':
            text += i
        elif i == '$':
            text += '\n'
        else:
            text += ' ' + i

    # Добавление точки в конце
    if (text[-1] != '.') and (text[-1] not in '-,!?;'):
        text += '.'
    elif text[-1] in '-,!?;':
        text[-1] = '.'

    return text


def save_text(text, text_dest):
    """
    Сохраняет текст в файл
    :param text: Текст
    :param text_dest: Располжение файла текста
    :type text: str
    :type text_dest: str
    :return: None
    """
    with open(text_dest, 'w') as f:
        f.write(text)


def main(args):
    """
    Главная функция
    :param args: Аргументы запуска генератора
    :type args: dict
    :return: None
    """
    model = load_model(args['model'])
    t = generate_text(model, args['length'], args['seed'])
    text = create_text(t)
    if args['output'] is None:
        print(text)
    else:
        save_text(text, args['output'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate text using model.', prog='generate.py')
    parser.add_argument('model', action='store', help='destination to model file')
    parser.add_argument('--seed', action='store', help='set starting word')
    parser.add_argument('length', action='store', type=int, help='length of generated text')
    parser.add_argument('--output', action='store',
                        help='destination to output file. If it isn\'t set, uses stdout')
    args = vars(parser.parse_args())
    main(args)
