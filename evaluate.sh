#!/bin/bash

EVAL_SCRIPT="./conll18_ud_eval.py"
GOLD_DIR="./gold_standard_annotated_texts"
PARSED_DIR="./parsing_results"

EVAL_DIR="./eval_results"

DATASETS=(
    "ru_gsd-ud-test"
    "ru_poetry-ud-test"
    "ru_syntagrus-ud-test"
    "ru_taiga-ud-test"
)

ALL_PARSERS=(
    "deeppavlov"
    "nlpcube"
    "stanza"
    "udpipe2"
)


PARSERS=(
    "stanza"
)

for PARSER in "${PARSERS[@]}"; do
    for DATASET in "${DATASETS[@]}"; do
        GOLD_FILE="$GOLD_DIR/${DATASET}.conllu"
        PARSED_FILE="$PARSED_DIR/$PARSER/${DATASET}-parsed-by-${PARSER}.conllu"
        EVAL_FILE="$EVAL_DIR/$PARSER/${PARSER}-${DATASET}-eval-results.txt"
        
        PYTHONIOENCODING=utf-8 py "$EVAL_SCRIPT" --verbose "$GOLD_FILE" "$PARSED_FILE" > "$EVAL_FILE" 2>&1
        
    done
done

echo "Оценка завершена"
