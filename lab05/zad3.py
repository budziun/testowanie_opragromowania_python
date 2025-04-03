from unittest.mock import Mock
#zad3

my_mock = Mock()
my_mock.method(1, 2)
my_mock.method(3, 4)
my_mock.method(x=5, y=6)

print("Call count:", my_mock.method.call_count)

print("Call args list:", my_mock.method.call_args_list)

print("Last call args:", my_mock.method.call_args)