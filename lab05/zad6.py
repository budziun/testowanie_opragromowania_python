from unittest.mock import Mock, call

mock = Mock()
mock.method1('test1')
mock.method1('test2')
mock.method2()


mock.method1.assert_called()
mock.method2.assert_called_once()
mock.method_not_called = Mock()
mock.method_not_called.assert_not_called()


mock.method1.assert_called_with('test2')
mock.method1.assert_any_call('test1')

# Check call order
expected_calls = [
    call('test1'),
    call('test2')
]
mock.method1.assert_has_calls(expected_calls)
mock.method1.assert_has_calls(expected_calls, any_order=True)

# Examine mock_calls and method_calls
print("mock_calls:", mock.mock_calls)
print("method_calls:", mock.method1.mock_calls)