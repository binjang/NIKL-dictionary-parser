# NIKL-dictionary-parser
Unofficial parser for [NIKL Dictionary](https://krdict.korean.go.kr/kor/mainAction).
As of January 2024, the dictionary contains 53,172 entries, 11 json files in total.

국립국어원의 "한국어기초사전"을 csv 파일로 파싱하는 라이브러리입니다. 최신 버전의 사전 파일들은 위 링크의 "사전 전체 내려받기" 버튼을 통해 다운받을 수 있습니다.
2024년 1월 버전을 기준으로 53,172개의 항목, 11개 json 파일로 구성되어 있습니다.

## Installation
```shell
pip3 install -r requirements.txt  # installs dependencies
```

## Usage
Edit configurations on `main.sh`
```shell
bash main.sh  # runs main.py in default configurations
```

## Data Description
| Column Name        | Type                  | Description                          | 설명                         |
|--------------------|-----------------------|--------------------------------------|----------------------------|
| Form               | `str`                 | Registered word entry                | 단어                         |
| Part of Speech     | `str` or `None`       | Part of speech of the word in Korean | 품사                         |
| Korean Definition  | `str`                 | Definition of the word in Korean     | 해당 단어의 한글 정의               |
| English Definition | `List[str]` or `None` | Definition of the word in English    | 한글 정의의 영문 번역본              |
| Usages             | `List[str]` or `None` | Sample sentence or dialogue          | 해당 단어의 예문 (문장 또는 대화 형식)    |
| Vocabulary Level   | `str` or `None`       | Difficulty of the word (3 levels)    | 단어의 난이도 ('초급', '중금', '고급') |
| Semantic Category  | `str` or `None`       | Semantic category of the word        | 단어 분류 (ex. '자연 > 기상 및 기후') |

## Future Updates
- Support more arguments