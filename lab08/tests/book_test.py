import pytest
from src.book import Book, LibraryManager

# --- Fixtures ---
@pytest.fixture
def library():
    return LibraryManager()

@pytest.fixture
def sample_books():
    return [
        Book(1, "The Hobbit", "J.R.R. Tolkien", 1937, "Fantasy"),
        Book(2, "1984", "George Orwell", 1949, "Dystopia"),
        Book(3, "Python Programming", "John Smith", 2020, "Education"),
        Book(4, "The Fellowship of the Ring", "J.R.R. Tolkien", 1954, "Fantasy"),
        Book(5, "Brave New World", "Aldous Huxley", 1932, "Dystopia")
    ]

@pytest.fixture
def populated_library(library, sample_books):
    for book in sample_books:
        library.add_book(book)
    return library


def test_add_and_get_book(library):
    book = Book(10, "Test Book", "Author", 2000, "Test")
    assert library.add_book(book)
    assert library.get_book(10) == book


def test_add_existing_book(populated_library, sample_books):
    assert not populated_library.add_book(sample_books[0])

def test_remove_book(populated_library):
    assert populated_library.remove_book(1)
    assert populated_library.get_book(1) is None


def test_remove_nonexistent_book(populated_library):
    assert not populated_library.remove_book(999)


def test_remove_borrowed_book_raises(populated_library):
    populated_library.borrow_book(2, "user1")
    with pytest.raises(ValueError):
        populated_library.remove_book(2)


def test_borrow_and_return_book(populated_library):
    assert populated_library.borrow_book(3, "user2")
    assert populated_library.return_book(3, "user2")


def test_borrow_already_borrowed_book(populated_library):
    populated_library.borrow_book(3, "user2")
    assert not populated_library.borrow_book(3, "user3")


def test_return_book_not_borrowed(populated_library):
    with pytest.raises(ValueError):
        populated_library.return_book(3, "user1")


def test_search_books_by_author(populated_library):
    results = populated_library.search_books({"author": "Tolkien"})
    assert all("Tolkien" in book.author for book in results)


def test_search_books_by_genre_and_year(populated_library):
    results = populated_library.search_books({"genre": "Dystopia", "year_from": 1930, "year_to": 1950})
    assert all(book.genre == "Dystopia" and 1930 <= book.publication_year <= 1950 for book in results)


def test_search_books_available_only(populated_library):
    populated_library.borrow_book(2, "user1")
    results = populated_library.search_books({"available_only": True})
    assert all(not book.is_borrowed for book in results)


def test_library_statistics(populated_library):
    populated_library.borrow_book(1, "user1")
    populated_library.borrow_book(2, "user2")
    stats = populated_library.get_statistics()
    assert stats["total_books"] == 5
    assert stats["borrowed_books"] == 2
    assert stats["available_books"] == 3
    assert stats["borrowers_count"] == 2
    assert "Fantasy" in stats["genres"]
    assert len(stats["popular_books"]) <= 5

@pytest.mark.parametrize("book_id,expected", [(1, True), (999, False)])
def test_get_book_by_id(populated_library, book_id, expected):
    assert (populated_library.get_book(book_id) is not None) == expected

@pytest.mark.parametrize("book,should_raise", [("not_a_book", True), (Book(99, "Valid", "Author", 2020, "Genre"), False)])
def test_add_book_type_check(library, book, should_raise):
    if should_raise:
        with pytest.raises(TypeError):
            library.add_book(book)
    else:
        assert library.add_book(book)
