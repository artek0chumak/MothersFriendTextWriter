"""
Библиотека для работы с моделью текста.
"""

from collections import Counter
import pickle


def load_model(model_dest):
    """
    Загрузка модели из файла
    :param model_dest: Расположение файла
    :type: str
    :return: Модель
    :rtype: Counter
    """
    with open(model_dest, 'rb') as f:
        model = pickle.load(f)
        if type(model) is dict:
            return Counter(model)
        elif type(model) is Counter:
            return model
        else:
            raise TypeError('Не правильный тип модели! Он должен быть '
                            'словарем или Counter!')


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


def train_model(ngramms, model_dest, upd_it):
    """
    Главная функция обучения модели
    :param ngramms: Генератор n-грамм
    :param model_dest: Расположение файла модели
    :param upd_it: Флаг обновления модели
    :type ngramms: generator
    :type model_dest: str
    :type upd_it: bool
    :return: None
    """
    try:
        m = load_model(model_dest)
    except FileNotFoundError:
        m = None

    if upd_it:
        # Если пытаемся обновить несуществующую модель, вызываем исключение
        if m is None:
            raise FileNotFoundError('Нет модели для обновления')

        m.update([tuple(i) for i in ngramms])
    else:
        m = Counter([tuple(i) for i in ngramms])

    save_model(m, model_dest)
