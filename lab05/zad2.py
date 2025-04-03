from unittest.mock import Mock

#zad2
class SampleClass:
    def method(self, x):
        pass

my_mock = Mock(spec=SampleClass, autospec=True)

my_mock.method.side_effect = [1, 2, 3]
def modify_args(x):
    return x * 2

my_mock.method.side_effect = modify_args

my_mock.method.side_effect = Exception("Test Exception")