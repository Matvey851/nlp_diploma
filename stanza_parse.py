import stanza
from pathlib import Path
from read_and_write_decorator import read_and_write

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / 'to_parse'
OUTPUT_DIR = BASE_DIR / 'parsing_results' / 'stanza'

INPUT_FILENAMES = [
    'ru_gsd-ud-test-to-parse.txt', 'ru_poetry-ud-test-to-parse.txt',
    'ru_syntagrus-ud-test-to-parse.txt', 'ru_taiga-ud-test-to-parse.txt'
]

OUTPUT_FILENAMES = [
    'ru_gsd-ud-test-parsed-by-stanza.conllu', 'ru_poetry-ud-test-parsed-by-stanza.conllu',
    'ru_syntagrus-ud-test-parsed-by-stanza.conllu', 'ru_taiga-ud-test-parsed-by-stanza.conllu'
]

# Предполагалось создание декоратора для уменьшения количества повторябщегося в проекте кода,
# но в итоге он был применен только к скрипту для stanza для удобства редактирвания остальных скриптов,
# оказавшихся более сложными
def read_and_write(func):
    def wrapper(read_dir, read_filenames, output_dir, output_filenames, parser=None):
        for read_filename, output_filename in zip(read_filenames, output_filenames):
            with open(read_dir / read_filename, 'r', encoding='utf-8') as file:
                read_data = file.read()
            result = func(read_data)
            with open(output_dir / output_filename, 'w', encoding='utf-8') as file:
                if parser == 'stanza':
                    file.write((result))
                    file.write('\n\n')
                    continue
                for sentence in result:
                    file.write((sentence.metadata['text'] + ' '))
    return wrapper


@read_and_write
def stanza_parse(read_data):
    nlp = stanza.Pipeline(lang='ru',
                          processors='tokenize,pos,lemma,depparse')
    parsed_data = nlp(read_data)
    conllu = "{:C}".format(parsed_data)
    return conllu


stanza_parse(INPUT_DIR, INPUT_FILENAMES, OUTPUT_DIR, OUTPUT_FILENAMES, parser='stanza')
