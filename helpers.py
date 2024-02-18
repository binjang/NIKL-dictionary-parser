def parse_feature(features_data, target_feature, return_all=False):
    """Helper function for parsing "feat" format data

    Args:
        features_data: json data of feat-val format
        target_feature: feature to parse
        return_all: whether to return all features

    Returns:
        Corresponding feature value

    Examples:
        features_data = {
            'feat': [
                {'att': 'homonym_number', 'val': '2'},
                {'att': 'lexicalUnit', 'val': '단어'},
                {'att': 'partOfSpeech', 'val': '명사'},
                {'att': 'origin', 'val': '說'},
                {'att': 'vocabularyLevel', 'val': '고급'},
                {'att': 'semanticCategory', 'val': '사회 생활 > 언어 행위'}
            ],
            'val': '63211'
        }

        parse_feature(features_data, 'partOfSpeech')  # returns '명사'


    """
    features = features_data['feat']

    if type(features) is list:
        if return_all:
            outputs = []
            for feature in features:
                if feature['att'] == target_feature:
                    outputs.append(feature['val'])
            return outputs

        else:
            for feature in features:
                if feature['att'] == target_feature:
                    return feature['val']

    elif type(features) is dict:
        feature = features
        if feature['att'] == target_feature:
            return feature['val']

    else:
        print(f"{type(features_data) = }")


def parse_equivalents(equivalents_data, language, target_feature):
    """Helper function for parsing "Equivalent" format data

    Args:
        equivalents_data: data of "equivalents" format, containing equivalent definitions and synonyms in different languages
        language: langguage to parse
        feature: feature to parse

    Returns:

    Examples:

        equivalents_data = {
            'Equivalent': [
                {'feat': [
                    {'att': 'language', 'val': '몽골어'},
                    {'att': 'lemma', 'val': 'дуулиан, цуу яриа'},
                    {'att': 'definition', 'val': 'хүмүүсийн дунд тархсан яриа.'}
                ]},
                {'feat': [
                    {'att': 'language', 'val': '아랍어'},
                    {'att': 'lemma', 'val': 'شائعة'},
                    {'att': 'definition', 'val': 'خبر ينتشر بين الناس'}
                ]},
                {'feat': [
                    {'att': 'language', 'val': '중국어'},
                    {'att': 'lemma', 'val': '传言'},
                    {'att': 'definition', 'val': '人们之间传播的故事。'}
                ]}, ...
            ]
        }

        parse_equivalents(equivalents_data, '중국어', 'definition')  # returns '人们之间传播的故事。'

    """
    equivalents = equivalents_data.get("Equivalent", None)
    if type(equivalents) is list:
        for equivalent in equivalents:
            if parse_feature(features_data=equivalent, target_feature='language') == language:
                return parse_feature(features_data=equivalent, target_feature=target_feature)

    elif type(equivalents) is dict:
        if parse_feature(features_data=equivalents, target_feature='language') == language:
            return parse_feature(features_data=equivalent, target_feature=target_feature)

    return None


def parse_examples(examples_data, target_types: list):
    """Helper function for parsing "SenseExample" format data

    Args:
        examples_data:
        target_types:

    Returns:

    Examples:
        examples_data = {
            'SenseExample': [
                {'feat': [
                    {'att': 'type', 'val': '구'},
                    {'att': 'example', 'val': '설이 나돌다.'}
                ]},
                {'feat': [
                    {'att': 'type', 'val': '구'},
                    {'att': 'example', 'val': '설이 난무하다.'}
                ]}, ...
                {'feat': [
                    {'att': 'type', 'val': '문장'},
                    {'att': 'example', 'val': '적자에 대한 책임을 지고 사장이 스스로 물러나리라는 설이 꾸준히 나돌았다.'}
                ]},
                {'feat': [
                    {'att': 'type', 'val': '문장'},
                    {'att': 'example', 'val': '차 의원이 기업으로부터 물질적인 혜택을 받았다는 설이 동료 국회 의원에 의해 제기되었다.'}
                ]},
                {'feat': [
                    {'att': 'type', 'val': '대화'},
                    {'att': 'example', 'val': '선생님, 우리 학교가 곧 다른 곳으로 이전한다는 설이 있다던데, 혹시 들은 적 있으세요?'},
                    {'att': 'example', 'val': '응, 나는 그런 말 들어 본 적이 없는데, 어디서 그런 말을 들었니?'}
                ]}
            ]
        }

        parse_examples(examples_data, target_types=["문장", "대화"])  # ['적자에 대한 ...', ['선생님, ...]]
                                                                    # Returns nested array for dialogues

    """
    examples = examples_data.get('SenseExample', None)
    outputs = []

    if examples is None:
        return outputs

    elif type(examples_data['SenseExample']) is dict:
        feature_type = parse_feature(features_data=examples, target_feature='type')
        if feature_type in target_types:
            return_all = True if feature_type == "대화" else False
            output = parse_feature(features_data=examples, target_feature='example', return_all=return_all)
            outputs.append(output)

        return outputs

    for example in examples:
        feature_type = parse_feature(features_data=example, target_feature='type')
        if feature_type in target_types:
            return_all = True if feature_type == "대화" else False
            output = parse_feature(features_data=example, target_feature='example', return_all=return_all)
            outputs.append(output)

    return outputs
