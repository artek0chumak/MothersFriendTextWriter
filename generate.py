# -*- coding: utf-8 -*-
"""
Генератор текста из модели, полученной обучением с помощью train.py.
Используйте -h для вызова справки.
"""
import argparse
import random
import pickle


def load_model(dest_model):
    """
    Загрузка модели из файла
    :param dest_model: Расположение файла модели
    :type dest_model: str
    :return: Словарь кортежа слов в частоты
    :rtype: dict
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
    :type model: dict
    :type length: int
    :type seed: str
    :return: Генератор слов
    :rtype: generator
    """
    n = len(next(iter(model)))
    pnt = 0

    if seed is None:
        seed = random.choice(tuple(i[0] for i in model))
        if seed in ',.!?;:-':
            pnt += 1
    if seed not in tuple(i[0] for i in model):
        raise ValueError('Данного слова нет в модели')
    yield seed

    t = [seed] + list(random.choice(tuple(i[1:n-1] for i in model
                                          if i[0] == seed)))
    if len(t) == 1:
        t += random.choice(tuple(i[1:n-1] for i in model))

    while length + pnt - 1 > 0:
        # Выбор нужного слова на основе n-1 предыдущих
        temp = weighted_choices(tuple((i[-1], model[i])
                                      for i in model if list(i[:-1]) == t))
        if temp is None:
            # Выбор нового слова, если не удалось найти подходящий по последним
            temp = random.choice(tuple(i[0] for i in model))
        if temp in ',.!?;:-':
            pnt += 1

        # Удаляем первое слово, так как оно больше нам не нужно
        t = t[1:] + [temp]
        length -= 1
        yield temp


def create_text(t):
    """
    Создает текст из списка слов
    :param t: Генератор слов
    :type t: generator
    :return: Сгенерированный текст
    :rtype: str
    """

    res = ''
    for i in t:
        if i in ',.!?;:':
            res += i
        else:
            res += ' ' + i

    return res


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
    parser = argparse.ArgumentParser(description='Generate text using model.',
                                     prog='generate.py')
    parser.add_argument('--model', action='store',
                        help='destination to model file')
    parser.add_argument('--seed', action='store', help='set starting word')
    parser.add_argument('--length', action='store', type=int,
                        help='length of generated text')
    parser.add_argument('--output', action='store',
                        help='destination to output file.'
                             ' If it isn\'t set, uses stdout')
    args = vars(parser.parse_args())
    main(args)
