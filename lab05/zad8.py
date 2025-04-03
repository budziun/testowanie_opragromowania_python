from unittest.mock import Mock

mock = Mock()
mock.method1(1)
mock.method2('tekst')
mock.nested.method(3)

print("Przed resetem:")
print("metoda1 ilosc call:", mock.method1.call_count)
print("mock_calls:", mock.mock_calls)

mock.reset_mock()
print("\nPo resecie:")
print("metoda1 ilosc call:", mock.method1.call_count)
print("mock_calls:", mock.mock_calls)

mock.method1.return_value = 42
mock.reset_mock(return_value=False)
print("\nPo resecie z return_value=False:")
print("method1 return_value:", mock.method1.return_value)