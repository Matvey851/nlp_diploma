#!/usr/bin/env python3
from pathlib import Path

PARSED_DIR = Path('parsing_results/deeppavlov')

FILES = [
    'ru_syntagrus-ud-test-parsed-by-deeppavlov.conllu',
    'ru_taiga-ud-test-parsed-by-deeppavlov.conllu',
]

REPLACEMENTS = {
    '"': '\u00ab',
    '"': '\u00bb',
    '\'': '\u00ab',
    '\'': '\u00bb',
}

for filename in FILES:
    file_path = PARSED_DIR / filename

    if not file_path.exists():
        print(f"Файл не найден: {file_path}")
        continue

    print(f"Обработка: {filename}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('``	`', '"	"')
    content = content.replace("''	''", "\"	\"")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  Сохранён: {file_path}")

print("Готово!")
