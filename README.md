# MOTHER's FRIEND TEXT WRITER

Генератор текстов, обучающийся на основе других текстов. Модель обучения - n-граммы слов.

## Getting Started.

### Prerequisites

Проект написан на python 3.6, используются только стандартные библиотеки (pickle, random, argparse, collections). Для установки python перейдите по ссылке: [https://www.python.org](https://www.python.org/).

### Training
Для запуска обучения модели используется файл train.py
```
    python3 train.py --lc --input-dir DIRECTORY --model MODEL --ngramms N --punc
```
1. lc - флаг перевода слов в прописной формат.
2. DIRECTORY - папка с текстами на обучение в кодировке UTF-8 и в формате txt(*.txt). Если не указан, то используется текст с клавиатуры.
3. MODEL - путь к файлу модели, которую надо обучить.
4. N - количество слов в n-грамме. Если не указан, то используется N=2.
5. punc - флаг добавления знаков пунктуации в модель

### Generating
Для создания текстов на основе уже обученной модели используется файл generate.py
```
    python3 generate.py --model MODEL --seed SEED --length LENGTH --output OUTPUT
```
1. MODEL - путь к файлу модели.
2. SEED - первое слово в генерируемом тексте.
3. LENGTH - длина текста в словах.
4. OUTPUT - файл, куда записывается текст. Если не указан, то текст выводится на экран.

## Example
```    
python3 generate.py --model Маяк --length 10
бесплатно стол и квартира как врезать ей в радиоухо шепчу
```

Ссылка на модель в [Google Drive](https://drive.google.com/drive/folders/1LvjaDZKfT0W_qx-qgVYTCTcCBZj73rSu?usp=sharing)
(Использованы тексты В.В. Маяковского).
## Authors

Артем Чумаченко - _Разработка_

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details