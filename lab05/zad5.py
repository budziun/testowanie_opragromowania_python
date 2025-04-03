from unittest.mock import Mock, call

mock = Mock()
mock.method.side_effect = lambda x: x * 2 if x < 10 else x + 10
print(mock.method(5))
print(mock.method(15))


mock.method.return_value = 100
mock.method.side_effect = lambda x: x * 2
print(mock.method(5))

# Configuring nested mocks
mock.attribute.method.return_value = 'wynik'
print(mock.attribute.method())

mock.configure_mock(
    attribute1='cos1',
    attribute2__method=lambda: 'metoda test'
)
print(mock.attribute1)
print(mock.attribute2.method())