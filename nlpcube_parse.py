from pathlib import Path
from cube.api import Cube
import razdel

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / 'to_parse'
OUTPUT_DIR = BASE_DIR / 'parsing_results' / 'nlpcube'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_FILENAMES = [
    'ru_gsd-ud-test-to-parse.txt',
    'ru_poetry-ud-test-to-parse.txt',
    'ru_syntagrus-ud-test-to-parse.txt',
    'ru_taiga-ud-test-to-parse.txt'
]

cube = Cube()
cube.load("ru")

for filename in INPUT_FILENAMES:
    print(f"Обрабатываю файл: {filename}")

    input_file = INPUT_DIR / filename
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    sentences = [s.text for s in razdel.sentenize(raw_text)]

    output_filename = filename.replace('-to-parse.txt', '-parsed-by-nlpcube.conllu')
    output_file = OUTPUT_DIR / output_filename

    error_count = 0

    with open(output_file, 'w', encoding='utf-8') as out:
        for i, sent_text in enumerate(sentences, 1):
            if not sent_text.strip():
                continue

            try:
                doc = cube(sent_text)

                for sentence in doc.sentences:
                    for word in sentence.words:
                        conllu_line = '\t'.join([
                            str(word.index),
                            word.word,
                            word.lemma,
                            word.upos,
                            word.xpos if word.xpos else '_',
                            word.attrs if word.attrs else '_',
                            str(word.head),
                            word.label if word.label else '_',
                            word.deps if word.deps else '_',
                            '_'
                        ])
                        out.write(conllu_line + '\n')
                    out.write('\n')

            except Exception as e:
                error_count += 1
                if error_count <= 5:
                    print(f"  Ошибка в предложении {i}: {sent_text[:100]}...")
                    print(f"    {type(e).__name__}: {e}")
                continue

            if i % 50 == 0:
                print(f"  Обработано {i}/{len(sentences)} предложений")

    print(f"  Сохранён: {output_file}")
    if error_count > 0:
        print(f"  Пропущено предложений из-за ошибок: {error_count}")

print("Готово!")
