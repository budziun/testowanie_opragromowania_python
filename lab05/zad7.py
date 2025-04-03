from unittest.mock import Mock, ANY

mock = Mock()
mock.complex_method(1, 'text', [1, 2, 3])
mock.complex_method(2, 'another', {'key': 'value'})
mock.complex_method(3, 'third', [4, 5, 6])

mock.complex_method.assert_any_call(1, ANY, [1, 2, 3])
mock.complex_method.assert_any_call(ANY, 'another', ANY)
def is_list(arg):
    return isinstance(arg, list)

mock.complex_method.assert_any_call(ANY, ANY, [1, 2, 3])
mock.complex_method.assert_any_call(ANY, ANY, [4, 5, 6])

calls_with_lists = [
    call for call in mock.complex_method.call_args_list
    if is_list(call[0][2])
]
assert len(calls_with_lists) > 0, "Blad"

print("Sukces")