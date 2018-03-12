"""Генератор текста на основе биграмм. Для генерации текста надо использовать уже обученную модель(обучение идет из
предлагаемых пользователем текстов). Для генерации текста можно указать параметры - начальное слово, длину. Вывод может
происходить как и в stdout, так и в файл."""
import argparse
import random
import pickle


def load_model(dist_model):
    """Load model from file"""
    with open(dist_model, 'rb') as f:
        return pickle.load(f)


def weighted_choices(choices):
    """Choise by weight"""
    total = sum(w for c, w in choices)
    # Choise float from 0 to total
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w


def generate_text(model, length, seed):
    """Main function to generate text"""
    t = []
    if seed is None:
        seed = random.choice(list(i[0] for i in model.keys()))
    t.append(seed)
    # Number of punctuation symbols
    pnc = 0
    while len(t) - pnc < length:
        t.append(weighted_choices([(i[1], model[i]) for i in model if i[0] == t[-1]]))
        if t[-1] in (',', '.', '!', '?', ';', ':'):
            pnc += 1
    return t


def create_text(t):
    """Create text from list of tokens"""
    text = ''
    for i in t:
        if i in (',', '.', '!', '?', ';', ':'):
            text += i
        elif i == '$':
            text += '\n'
        else:
            text += ' ' + i

    # Adding last dot
    if t[-1] not in ('.', '!', '?'):
        text += '.'

    return text


def save_text(text, text_dest):
    """Save text to file"""
    with open(text_dest, 'w') as f:
        f.write(text)


def main(args):
    """Main function"""
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
