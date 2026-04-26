# Удаляю аннотации из файлов:
# gold_standsrd_annotated_texts/ru_gsd-ud-test.conllu
# gold_standard_annotated_texts/ru-poetry-ud-test.conllu
# gold_standard_annotated_texts/ru_syntagrus-ud-test.conllu
# gold_standard_annotated_texts/ru_taiga-ud-test.conllu
# И сохраняю очищенные от разметки данные в соответственно:
# to_parse/ru_gsd-ud-test-to-parse.conllu
# to_parse/ru_poetry-ud-test-to-parse.conllu
# to_parse/ru_syntagrus-ud-test-to-parse.conllu
# to_parse/ru_taiga-ud-test-to-parse.conllu

import conllu
from pathlib import Path
from read_and_write_decorator import read_and_write


BASE_DIR = Path(__file__).resolve().parent
ANNOTATED_TEXTS_DIR = BASE_DIR / 'gold_standard_annotated_texts'
TO_PARSE_DIR = BASE_DIR / 'to_parse'
INPUT_FILENAMES = [
    'ru_gsd-ud-test.conllu', 'ru_poetry-ud-test.conllu',
    'ru_syntagrus-ud-test.conllu', 'ru_taiga-ud-test.conllu'
    ]
OUTPUT_FILENAMES = [filename.replace('.conllu', '-to-parse.txt') for filename in INPUT_FILENAMES]


@read_and_write
def delete_annotations(read_data):
    data = conllu.parse(read_data)
    return data


delete_annotations(ANNOTATED_TEXTS_DIR, INPUT_FILENAMES, TO_PARSE_DIR, OUTPUT_FILENAMES)
