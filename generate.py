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
    :return: Словарь кортежа слов в частыт
    :rtype: dict
    """
    with open(dest_model, 'rb') as f:
        return pickle.load(f)


def weighted_choices(choices):
    """
    Куммулятивное распределение
    :param choices: Список слов и их частоты
    :type choices: list
    :return: Выбранное слово
    :rtype: str
    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w


def generate_text(model, length, seed):
    """
    Генерация текста
    :param model: Модель текстов
    :param length: Длина текста в словах(знаки пунктуации считаются за слова)
    :param seed: Начальное слово
    :type model: dict
    :type length: int
    :type seed: str
    :return: Список слов
    :rtype: list
    """
    l_ngrams = len(next(iter(model)))
    t = ['$' for _ in range(l_ngrams - 1)]
    if seed is None:
        seed = random.choice([i[-1] for i in model if list(i[:-1]) == t])
    t.append(seed)
    while len(t) < length + l_ngrams:
        t.append(weighted_choices([(i[-1], model[i]) for i in model if list(i[:-1]) == t[-l_ngrams + 1:]]))
        if t[-1] is None:
            t[-1] = random.choice([i[-1] for i in model if list(i[:-1]) == ['$' for _ in range(l_ngrams - 1)]])

    return t[l_ngrams - 1:]


def create_text(t):
    """
    Создает текст из списка слов
    :param t: Список слов
    :type t: list
    :return: Сгенерированный текст
    :rtype: str
    """
    text = ''
    for i in t:
        if i in (',', '.', '!', '?', ';', ':'):
            text += i
        elif i == '$':
            text += '\n'
        else:
            text += ' ' + i

    if t[-1] not in ('.', '!', '?'):
        text += '.'

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
