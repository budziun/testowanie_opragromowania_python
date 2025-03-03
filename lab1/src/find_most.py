from collections import Counter
def find_most_frequent_word(text: str) -> str:
    words = text.lower().split()
    if not words:
        return ""
    words_count = Counter(words)
    return max(words_count, key=words_count.get)
