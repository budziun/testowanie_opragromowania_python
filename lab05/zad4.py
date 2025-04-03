from unittest.mock import MagicMock
import contextlib

magic_mock = MagicMock()

magic_mock.__len__.return_value = 10
magic_mock.__add__.return_value = "dodano"
magic_mock.__getitem__.return_value = "przedmiot"

magic_mock.__str__.return_value = "Losowy tekst"

class MockContextManager(contextlib.AbstractContextManager):
    def __enter__(self):
        return magic_mock

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

# Demonstration
with MockContextManager() as cm:
    print(len(cm))
    print(str(cm))