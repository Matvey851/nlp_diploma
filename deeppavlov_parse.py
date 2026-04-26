from pathlib import Path
from deeppavlov import build_model
from razdel import sentenize


BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / 'to_parse'
OUTPUT_DIR = BASE_DIR / 'parsing_results' / 'deeppavlov'
INPUT_FILENAMES = ['ru_gsd-ud-test-to-parse.txt', 'ru_poetry-ud-test-to-parse.txt',
                  'ru_syntagrus-ud-test-to-parse.txt', 'ru_taiga-ud-test-to-parse.txt']

model = build_model("ru_syntagrus_joint_parsing", download=True, install=True)

for filename in INPUT_FILENAMES:
    input_file = INPUT_DIR / filename
    with open(input_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    sentences = [s.text for s in sentenize(raw_text)]

    output_file = OUTPUT_DIR / (filename.replace('-to-parse.txt', '-parsed-by-deeppavlov.conllu'))
    with open(output_file, 'w', encoding='utf-8') as out:
        for sent in sentences:
            parsed = model([sent])
            for p in parsed:
                if p:
                    out.write(p + '\n\n')
