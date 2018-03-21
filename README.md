# MOTHER's FRIEND TEXT WRITER

Генератор текстов, обучающийся на основе других текстов. Модель обучения - n-граммы слов. В качестве слов принимаются и знаки препинания.

## Getting Started.

### Prerequisites

Проект написан на python3.6, используются только стандартные библиотеки (pickle, random, argparse, collections). Для установки python перейдите по ссылке: [https://www.python.org](https://www.python.org/).

### Training
Для запуска обучения модели используется файл train.py
    python3 train.py --lc --input-dir DIRECTORY --model MODEL --ngrams N
1. lc - флаг перевода слов в прописной формат.
2. DIRECTORY - папка с текстами на обучение в кодировке UTF-8 и в формате txt(*.txt). Если не указан, то используется текст с клавиатуры.
3. MODEL - путь к файлу модели, которую надо обучить. Если не указан, создается новая модель.
4. N - количество слов в n-грамме. Если не указан, то используется N=2.

### Generating
Для создания текстов на основе уже обученной модели используется файл generate.py
    python3 generate.py MODEL --seed SEED LENGTH --output OUTPUT
1. MODEL - путь к файлу модели.
2. SEED - первое слово в генерируемом тексте.
3. LENGTH - длина текста в словах(знаки пунктуации не считаются).
4. OUTPUT - файл, куда записывается текст.

## Example
    python generate.py Маяковский.model 40  стучат в бюро аркосовы, со сметаной, с дону!  башня- хотите?  поезд темный и душный, и ты преуспеешь на жизненной сцене- начальство заметит тебя и оценит.  аж на тракторах- пахали!  зажать!  беги на вой!  1915 вам.
Ссылка на модель в [Google Drive](https://drive.google.com/open?id=1LvjaDZKfT0W_qx-qgVYTCTcCBZj73rSu)
(Использованы тексты В.В. Маяковского, Ф.М. Достоевского, Стивена Кинга).
## Authors

**Артем Чумаченко **- _Разработка_

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details