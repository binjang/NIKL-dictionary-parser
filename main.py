import pandas as pd
import json
from tqdm import tqdm
import argparse
from pathlib import Path

from helpers import parse_feature, parse_equivalents, parse_examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', '-i', type=str, help='Input file directory', default='2024_01')
    parser.add_argument('--output_filename', '-o', type=str, help='Output file path', default='results.csv')
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_filename = args.output_filename

    json_files = list(input_dir.glob('*.json'))
    results = pd.DataFrame(columns=['Form', 'Part of Speech', 'Korean Definition', 'English Definition', 'Usages', 'Vocabulary Level', 'Semantic Category'])

    form_col = []
    pos_col = []
    kor_definitions_col = []
    eng_definitions_col = []
    usages_col = []
    vocabulary_level_col = []
    semantic_category_col = []
    for file in tqdm(json_files):
        with open(file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        entries = data['LexicalResource']['Lexicon']['LexicalEntry']

        for i, entry in enumerate(entries):
            if type(entry['Lemma']) is list:
                form = parse_feature(entry['Lemma'][0], 'writtenForm')
            else:
                form = parse_feature(entry['Lemma'], 'writtenForm')

            pos = parse_feature(entry, 'partOfSpeech')
            pos = (pos if pos != "품사 없음" else None)
            vocabulary_level = parse_feature(entry, 'vocabularyLevel')
            vocabulary_level = (vocabulary_level if vocabulary_level != "없음" else None)
            semantic_category = parse_feature(entry, 'semanticCategory')

            kor_definitions = []
            eng_definitions = []
            usage_lists = []
            if type(entry['Sense']) is list:
                for meaning in entry['Sense']:
                    kor_definition = parse_feature(meaning, 'definition')
                    try:
                        eng_definition = parse_equivalents(meaning, "영어", 'definition')
                    except Exception as e:
                        print(i)
                        print(f"{eng_definition = }")
                        raise e

                    usage_list = parse_examples(meaning, ['문장', '대화'])

                    kor_definitions.append(kor_definition)
                    eng_definitions.append(eng_definition)
                    usage_lists.extend(usage_list)

            elif type(entry['Sense']) is dict:
                if entry['Sense'].get('Equivalent', None) is None:
                    continue

                kor_definition = parse_feature(entry['Sense'], 'definition')
                eng_definition = parse_equivalents(entry['Sense'], "영어", 'definition')
                usage_list = parse_examples(entry['Sense'], ['문장', '대화'])

                kor_definitions.append(kor_definition)
                eng_definitions.append(eng_definition)
                usage_lists.extend(usage_list)

            else:
                print(f"Unexpected type: {type(entry['Sense']) = }")
                break

            form_col.append(form)
            pos_col.append(pos)
            kor_definitions_col.append(kor_definitions)
            eng_definitions_col.append(eng_definitions)
            usages_col.append(usage_lists)
            vocabulary_level_col.append(vocabulary_level)
            semantic_category_col.append(semantic_category)

    results['Form'] = form_col
    results['Part of Speech'] = pos_col
    results['Korean Definition'] = kor_definitions_col
    results['English Definition'] = eng_definitions_col
    results['Usages'] = usages_col
    results['Vocabulary Level'] = vocabulary_level_col
    results['Semantic Category'] = semantic_category_col

    print(f"Saving results to {output_filename} ...")
    results.to_csv(output_filename, index=False)


if __name__ == "__main__":
    main()
