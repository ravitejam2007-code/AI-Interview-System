import re


def is_valid_answer(answer):
    answer = answer.strip()

    if len(answer) < 5:
        return False

    words = answer.split()

    if len(words) < 2:
        return False

    return True


def is_gibberish(text):
    text = text.strip().lower()

    if re.match(r'^[a-z]{5,}$', text) and len(text.split()) == 1:
        return True

    gibberish_patterns = [
        r'^[a-z]{10,}$',
        r'^[a-z]+[0-9]+[a-z]+$',
        r'^(.)\1{4,}$',
        r'^[qwertyuiopasdfghjklzxcvbnm]{6,}$',
    ]

    for pattern in gibberish_patterns:
        if re.match(pattern, text):
            return True

    noise_words = ['asdf', 'qwerty', 'zxcv', 'test', 'testtest', 'aaaa', 'bbbb']
    for word in noise_words:
        if word in text:
            return True

    return False
