import random
import re

TOKENIZE_RE = re.compile(r'(\w+)', re.U)
SEPARATOR = '\n—weird—\n'


def shuffle_string(word: str, middle_letters: list):
    """
    :param word: word to encode
    :param middle_letters: word without first and last letter
    :return: encoded word
    """
    while True:
        random.shuffle(middle_letters)
        shuffled_word = word[0] + "".join(middle_letters) + word[-1]
        if word != shuffled_word:
            return shuffled_word


def unshuffle_string(word: str, original_words: list):
    """
    :param word: encoded or original word with multiple the same letters
    :param original_words: list of original words
    :return: decoded word if word was encoded, otherwise word
    """
    for original_word in original_words:
        if len(word) == len(original_word):
            if word.startswith(original_word[0]) and word.endswith(original_word[-1]):
                if not set(word) - set(original_word):
                    original_words.remove(original_word)
                    return original_word
    return word


def encode(text_to_encode: str):
    """
    :param text_to_encode:
    :return: separator, encoded string, separator, list of original words
    """
    original_words = []
    encoded_text = []
    listed_text = TOKENIZE_RE.split(text_to_encode)
    for word in listed_text:
        if len(word) > 3:
            middle_letters = list(word[1:-1])
            if len(set(middle_letters)) > 1:
                original_words.append(word)
                word = shuffle_string(word, middle_letters)
        encoded_text.append(word)
    original_words = sorted(original_words, key=lambda s: s.lower())
    original_words = " ".join(original_words)
    encoded_text = "".join(encoded_text)
    result = "".join([SEPARATOR, encoded_text, SEPARATOR, original_words])
    return result


def decode(text_to_decode: str):
    """
    :param text_to_decode: encoded text
    :return: decoded string
    """
    if not text_to_decode.startswith(SEPARATOR):
        raise ValueError("Could not decode. Given text is not a result of an encoder. Please enter valid text to decode and try again.")
    decoded_text = []
    encoded = [x for x in text_to_decode.split(sep=SEPARATOR) if x]
    if len(encoded) < 2:
        return encoded[0]
    encoded_text = re.findall(r"[\w']+|[.,!?;()]", encoded[0])
    original_words = re.findall(r"[\w']+|[.,!?;()]", encoded[1])
    for word in encoded_text:
        if len(word) > 3:
            word = unshuffle_string(word, original_words)
        decoded_text.append(word)
    decoded_text = " ".join(decoded_text)
    result = re.sub(r'\s+([?.!,)])', r'\1', decoded_text)
    result = re.sub(r'([(])\s+', r'\1', result)
    return result


if __name__ == '__main__':
    text = '''This is a long looong test sentence, with some big (biiiiig) words!'''
    print("Encoder result:")
    print(encode(text))
    print("\nDecoder result:\n")
    print(decode(encode(text)))
