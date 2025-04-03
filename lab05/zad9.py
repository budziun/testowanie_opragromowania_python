from unittest.mock import Mock, call

mock = Mock()
mock.method(1, 2)
mock.method(x=3, y=4)
mock.method('pos', named=5)

c1 = call(1, 2)
c2 = call(x=3, y=4)

print("Matching first call:", c1 in mock.method.call_args_list)
print("Matching second call:", c2 in mock.method.call_args_list)

expected_calls = [
    call(1, 2),
    call(x=3, y=4),
    call('pos', named=5)
]

print("\nCall list matches:", mock.method.call_args_list == expected_calls)

print("\nCall object details:")
last_call = mock.method.call_args
print("Positional args:", last_call.args)
print("Keyword args:", last_call.kwargs)

print("\nCall object demonstration:")
sample_call = call(1, 2, x=3)
print("Call args:", sample_call.args)
print("Call kwargs:", sample_call.kwargs)