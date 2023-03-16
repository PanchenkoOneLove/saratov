"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting from largest amount of unique symbols
    2) Find rarest symbol for document
    3) Count every punctuation char
    4) Count every non ascii char
    5) Find most common non ascii char for document
"""
from typing import List
import re
import collections


def get_longest_diverse_words(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        long_words = {'a': 1}  # {'word': *amount of unique sym* }

        for line in file:
            line = line.encode('utf-8').decode('unicode-escape')  # Representation of the Unicode literals
            words = re.findall(r'\b[A-Za-zäöüÄÖÜß]+\b', line)  # Template for finding Germanic words

            for word in words:
                uniq_amount = len(set(word))  # the length of unique characters in the word
                min_uniq_dict = min(long_words.values())  # minimum number of unique characters
                if len(long_words) <= 10:
                    long_words[word] = uniq_amount
                elif uniq_amount > min_uniq_dict:
                    long_words = {key: val for key, val in long_words.items() if val != min_uniq_dict}
                    long_words[word] = uniq_amount  # dictionary overwrite

    return long_words.keys()  # Converting dictionary to a list of keywords


def get_rarest_char(file_path: str) -> str:
    with open(file_path, "r") as file:
        text = file.read().encode('utf-8').decode('unicode-escape')
        counter_dict = collections.Counter(text)  # Counting every character in the text
        rarest_char = min(counter_dict, key=counter_dict.get)  # Finding the rarest symbol
        return rarest_char

def count_punctuation_chars(file_path: str) -> int:
    with open(file_path, "r") as file:
        text = file.read().encode('utf-8').decode('unicode-escape')
        punctuation_chars = re.findall(r'[^\w\s]', text)
        punctuation_chars_dict = collections.Counter(punctuation_chars)
        return sum(punctuation_chars_dict.values())  # The sum of all characters in the symbol dictionary


def count_non_ascii_chars(file_path: str) -> int:
    with open(file_path, "r") as file:
        text = file.read().encode('utf-8').decode('unicode-escape')
        non_ascii = re.findall(r'[^\x00-\x7F]', text)
        non_ascii_dict = collections.Counter(non_ascii)
        return sum(non_ascii_dict.values())  # the sum of all non_ascii symbol


def get_most_common_non_ascii_char(file_path: str) -> str:
    with open(file_path, "r") as file:
        text = file.read().encode('utf-8').decode('unicode-escape')
        non_ascii = re.findall(r'[^\x00-\x7F]', text)
        non_ascii_dict = collections.Counter(non_ascii)
        common = max(non_ascii_dict.values())
        return list(non_ascii_dict.keys())[list(non_ascii_dict.values()).index(common)]  # A common non-ascii symbol
