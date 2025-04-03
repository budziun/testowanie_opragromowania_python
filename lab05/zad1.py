from unittest.mock import Mock

#zad1

my_mock = Mock(name='TEST Jakub Budzich')

my_mock.get_data.return_value = 'test_test'

result = my_mock.get_data('user')

my_mock.get_data.assert_called_with('user')

print(my_mock.get_data.call_args)