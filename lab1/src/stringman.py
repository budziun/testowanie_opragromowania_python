class StringManipulator:
    @staticmethod
    def reverse_string(text: str) -> str:
        return text[::-1]
    @staticmethod
    def count_words(text: str) -> int:
        return len(text.split()) if text else 0
    @staticmethod
    def capitalize_words(text: str) -> str:
        return " ".join(word.capitalize() for word in text.split())
