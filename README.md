# Структура проекта
Директории проекта
- папка gold_standart_annotated_text содержит скачанные файлы соответствующих корупсов
> [ссылка на скачивание ru_gsd-ud-test.conllu](https://github.com/UniversalDependencies/UD_Russian-GSD/blob/master/ru_gsd-ud-test.conllu)
> [ссылка на скачивание ru_poetry-ud-test.conllu](https://github.com/UniversalDependencies/UD_Russian-Poetry/blob/master/ru_poetry-ud-test.conllu)
> [ссылка на скачивание ru_syntagrus-ud-test.conllu](https://github.com/UniversalDependencies/UD_Russian-SynTagRus/blob/master/ru_syntagrus-ud-test.conllu)
> [ссылка на скачивание ru_taiga-ud-test.conllu](https://github.com/UniversalDependencies/UD_Russian-Taiga/blob/master/ru_taiga-ud-test.conllu)
- папка to_parse содержит файлы соответствующих корпусов, отчищенные от аннотаций
- папка parsing_results содержит результаты парсинга
- папка eval_results содержит результаты оценивания работы парсера скриптом conll18_ud_eval.py

Файлы проекта
- README.md - справочная информация об эксперименте
- requirements_<название_парсера> - список зависимостей, которые необходимо установить перед запуском определенного парсера
- delete_annotations.py - скрипт для получения сырого текста из файлов корпусов
- conll18_ud_eval.py - скрипт для оценки результатов парсинга
> скачан [с этой страницы](https://universaldependencies.org/conll18/evaluation.html)
- <название_парсера>_parse - скрипты для запуска парсеров, запускаемых ручным скриптом
- evaluate.sh - скрипт для запуска conll18_ud_eval для всех парсеров и всех корпусов
- download_nltk файл для загрузки модуля, необходимого для работы парсера deeppavlov
- deeppavlov_quotes - файл для замены кавычек нестандартного (относительно корпусов gold_standard_annotated_text) формата на стандартные в результате работы deeppavlov


# Повторение эксперимента
Все команды следует выполнять из корневой (верхней) папки проекта

## 1. Создание начальных данных
Для поторения эксперимента нужно следать следующие шаги.
1. Загрузить репозиторий на свой ПК. 

2. Удалить данные полученные в ходе эксперимента:
    - все файлы в папке to_parse
    - все файлы в подпапках директории parsing_results
    - все файлы в подпапках директории eval_results
**Важно! Сами директории и поддиректории не удалять, иначе некоторые скрипты не будут работать!**

3. Очистить скачанные данные, загруженные в папку gold_standard_annotated_texts. 
Для этого нужно запустить скрипт delete_annotations.py:
```bash
python delete_annotations.py
```
Очищенные от аннотаций тексты корпусов будут сохранены в папку to_parse

## 2. Парсинг

### UDPipe 2
1. Очищенные файлы из папки to_parse поочередно загрузить в парсер через [предоставленный разработчиками веб-интерфес](https://lindat.mff.cuni.cz/services/udpipe/)
> Доступ по ссылке может быть ограничен для ряда стран владельцами сервера
2. Нажать Process input
3. Полученные на выходе файлы сохранить в директорию parsing_results/UDPipe2 с нужными названиями

### Stanza
1. (Опционально) Создать и активировать виртуальное окружение
```bash
python -m venv venv_stanza
source venv_stanza/Scripts/activate # Windows
source venv_stanza/bin/activate # Linux
```
2. Установить зависимости, необходимые для работы парсера
```bash
pip install -r requirements_stanza.txt
```
3. Запустить скрипт stanza_parse.py
```bash
python stanza_parse.py
```
Результаты парсинга будут сохранены в папке parsing_results/stanza

### deeppavlov
Для работы парсеру deeppavlov необходима библиотека fasttext, которая может быть запущена только на Linux или MacOS.
С учетом давнего последнего обновления проекта и специфического списка зависимостей, я пользовался интерпетатором python 3.9 (при работе со stanza пользовался 3.12).
Также вероятно, что доступность некоторых моделей, которые парсер устанавливает при развертывании, имеет ограничения, связанные с местоположением устройства, на котором запущен парсер.

1. (Опционально) Создать и активировать виртуальное окружение
```bash
python -m venv venv_deeppavlov
source venv_deeppavlov/Scripts/activate # Windows
source venv_deeppavlov/bin/activate # Linux
```
2. Установить зависимости проекта
```bash
pip install -r requirements_deeppavlov.txt
```
3. Установаить зависимости модели (именно этих версий) 
```bash
python -m deeppavlov install ru_syntagrus_joint_parsing
```
4. Установить необходимые модули nltk с помощью файла download_nltk.py
```bash
python download_nltk.py
```
4. Запустить скрипт deeppavlov_parse.py
```bash
python deeppavlov_parse.py
```
Результаты парсинга будут сохранены в parsing_results/deeppavlov

### nlpcube
Для работы парсеру nlpcube требуется графический процессор с поддержкой технологии CUDA. В моем случае мне пришлось арендовать сервер с NVIDIA Tesla T4 и запускать парсер на нем.
Также nlpcube как и deeppavlov использует fasttext, а значит, вероятно, он может быть запущен только на Linux или MacOS.
Как и с deeppavlov в виду давнего последнего обновления проекта и специфического списка зависимостей я использовал интерпретатор python 3.9.

1. (Опционально) Создать и активировать виртуальное окружение
```bash
python -m venv venv_nlpcube
source venv_nlpcube/Scripts/activate # Windows
source venv_nlpcube/bin/activate # Linux
```
2. Установить fasttext-wheel
```bash
pip install fasttext-wheel pybind11 setuptools wheel
```
3. Устанока и починка fasttext 0.9.2
Парсер требует fasttext==0.9.2, однако при компиляции этого модуля я столкнулся с ошибкой `error: 'uint64_t' was not declared in this scope`. Решить ее мне помог [ответ в обсуждении](https://github.com/facebookresearch/fastText/issues/1281#issuecomment-1540738521).
В соответствии с рекомендацией нужно выполнить следующие инструкции 
```bash
sudo apt-get update
sudo apt-get install build-essential python3-dev

# 3. Скачайте исходный код fasttext и перейдите в нужную версию
git clone https://github.com/facebookresearch/fastText.git
cd fastText
git checkout v0.9.2

# 4. Внесите поправку: откройте файл src/args.cc в любом редакторе (nano, vim)
nano src/args.cc

# Найдите в самом верху файла блок #include ... и добавьте строку:
# #include <cstdint>
# Например, после строки #include <unordered_map>.

# Сохраните файл и закройте редактор.

# 5. Установите исправленный fasttext
pip install .
cd ..
```
4. Установить остальные зависимости парсера (именно этих версий)
```bash
pip install -r requirements_nlpcube.txt
```
5. Запустить парсер
```bash
python nlpcube_parse.py
```

## 3. Обработка полученных данных перед оценкой
Чтобы скрипт conll18_ud_eval.py отработал успешно, данные полученные от парсеров deeppavlov и nlpcube нужно немного обработать.

### Данные от deeppavlov 
При обработке текстов корпусов syntagrus и taiga, deeppavlov заменил формат кавычек, что в дальнейшем может привести к проблемам в работе скрипта conll18_ud_eval.py, когда тот будет сравнивать полученные данные с эталонными. 
Для того чтобы вернуть тот формат кавычек, которые применяются в эталонных корпусах, нужно запустить файл deeppavlov_quotes.py
```bash
python deeppavlov_quotes.py
```
Файлы, в которых не были изменены кавычки, находятся в parsing_results/deeppavlov/before_quotes_replacement.

### Данные от nlpcube
В полученных от nlpcube данных обработки корпусов syntagrus и taiga в нескольких фрагментах пропущены точки в конце предложения. Таких место около 5 в syntagrus и около 2 в taiga. При запуске evaluation.sh они будут выводиться в файлы eval_results/nlpcube/nlpcube-ru_syntagrus-ud-test-eval-results.txt и eval_results/nlpcube/nlpcube-ru_taiga-ud-test-eval-results.txt соответственно. Я исправлял это вручную, ориентируясь на информацию выводимую в файл оценки и проводя поиск этих слов в файле, полученном после парсинга. Находя предложение, разбор которого не заканчивался точкой, я добавлял строку с точкой из эталонного корпуса, а также соответствующий ей индекс. Например, `15	.	.	PUNCT	_	_	11	punct	11:punct	_`. Неизмененные файлы, полученные после обработки корпуса syntagrus, находятся в parsing_results/nlpcube/before_dots_fix.

## 4. Оценка результатов работы парсеров с помощью файла conll18_ud_eval.py

Для оценивания всех файлов, полученных в результате работы парсеров, достаточно выполнить файл evaluate.sh, перед этим дав ему разрешение на выполнение
```bash
chmod +x evaluate.sh
bash evaluate.sh
```
Файлы с оценками (в подпапках, соответствующих парсеру и с названиями, соответствующими парсеру и разобранному корпусу) будут в eval_results


## Важная информация об обработке парсером nlpcube корпусов gsd, syntagrus и taiga

**В соответствии со скриптом nlpcube_parse.py разбор предложений, вызвавших ошибку у парсера, не был выполнен. В файле, полученном от парсера, вместо разобранного предложения стоит заглушка.**

Заглушка представляет собой предложение с аннотациями, значения которых созданы искуственно. Их значения
1. ID — порядковый номер слова в предложении, совпадает с оригиналом (1, 2, 3, 4, 5...)
2. FORM — оригинальная словоформа из исходного текста (сохраняется для совпадения с эталоном)
3. LEMMA — `_`
4. UPOS — `_`
5. XPOS — `_`
6. FEATS — `_`
7. HEAD — `0` для первого слова (корень), `1` для всех остальных (зависят от первого слова)
8. DEPREL — `root` для первого слова (связь "корень"), `dep` для всех остальных (связь "зависимость" по умолчанию)
9. DEPS — `_`
10. MISC — `_`

Информация о таких предложениях, а также об ошибках, с которыми столкнулся парсер при их разборе, приведена в файлах находящихся в parsing_results/nlpcube/error_logs.

Для gsd таких предложений 2 из 610, для syntagrus 31 из 8740, для taiga 3 из 963 предложений.
