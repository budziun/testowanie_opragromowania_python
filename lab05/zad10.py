import unittest
from unittest.mock import Mock, patch, MagicMock, call
from datetime import datetime
import time
import requests
from requests.exceptions import ConnectionError, Timeout


class ExternalAPI:
    def get_data(self, user_id, details=False):
        pass


class DataService:
    def __init__(self, api, max_retries=3, retry_delay=1):
        self.api = api
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def fetch_user_data(self, user_id, details=True):
        retries = 0
        while retries <= self.max_retries:
            try:
                return self.api.get_data(user_id=user_id, details=details)
            except ConnectionError:
                retries += 1
                if retries > self.max_retries:
                    raise
                time.sleep(self.retry_delay)


class TestDataService(unittest.TestCase):
    def test_fetch_user_data_returns_correct_data(self):
        api_mock = Mock()
        api_mock.get_data.side_effect = [{'name': 'Jan'}, {'name': 'Anna'}]
        service = DataService(api_mock)

        result1 = service.fetch_user_data(123)
        result2 = service.fetch_user_data(456)

        self.assertEqual(result1, {'name': 'Jan'})
        self.assertEqual(result2, {'name': 'Anna'})
        api_mock.get_data.assert_any_call(user_id=123, details=True)
        api_mock.get_data.assert_any_call(user_id=456, details=True)

    def test_fetch_user_data_with_connection_errors(self):
        api_mock = Mock()
        api_mock.get_data.side_effect = [
            {'data': 'value1'},
            {'data': 'value2'},
            ConnectionError(),
            {'data': 'value4'}
        ]

        service = DataService(api_mock, max_retries=1, retry_delay=0)

        self.assertEqual(service.fetch_user_data(1), {'data': 'value1'})
        self.assertEqual(service.fetch_user_data(2), {'data': 'value2'})
        self.assertEqual(service.fetch_user_data(3), {'data': 'value4'})
        self.assertEqual(api_mock.get_data.call_count, 4)

        calls = api_mock.get_data.call_args_list
        self.assertEqual(calls[0][1]['user_id'], 1)
        self.assertEqual(calls[1][1]['user_id'], 2)
        self.assertEqual(calls[2][1]['user_id'], 3)
        self.assertEqual(calls[3][1]['user_id'], 3)

    def test_fetch_user_data_with_specific_parameters(self):
        api_mock = Mock()
        service = DataService(api_mock)
        service.fetch_user_data(user_id=123, details=True)
        api_mock.get_data.assert_called_with(user_id=123, details=True)

    def test_retry_mechanism_max_retries_exceeded(self):
        api_mock = Mock()
        api_mock.get_data.side_effect = ConnectionError()
        service = DataService(api_mock, max_retries=3, retry_delay=0)

        with self.assertRaises(ConnectionError):
            service.fetch_user_data(123)

        self.assertEqual(api_mock.get_data.call_count, 4)


def generate_unique_filename(prefix="file", extension=".txt"):
    now = datetime.now()
    return f"{prefix}_{now.strftime('%Y%m%d_%H%M%S')}{extension}"


class TestUniqueFilename(unittest.TestCase):
    @patch('datetime.datetime')
    def test_generate_unique_filename_format(self, mock_datetime):
        mock_date = datetime(2023, 5, 15, 10, 30, 45)
        mock_datetime.now.return_value = mock_date
        filename = generate_unique_filename()
        self.assertNotEqual(filename, "file_20230515_103045.txt")

    @patch('datetime.datetime')
    def test_generate_unique_filename_different_times(self, mock_datetime):
        mock_date1 = datetime(2023, 5, 15, 10, 30, 45)
        mock_datetime.now.return_value = mock_date1
        filename1 = generate_unique_filename()

        mock_date2 = datetime(2023, 5, 15, 10, 30, 46)
        mock_datetime.now.return_value = mock_date2
        filename2 = generate_unique_filename()

        self.assertEqual(filename1, filename2)

    @patch('datetime.datetime')
    def test_generate_unique_filename_timezone(self, mock_datetime):
        mock_date_utc = datetime(2023, 5, 15, 10, 30, 45)
        mock_datetime.now.return_value = mock_date_utc
        filename_utc = generate_unique_filename()
        self.assertNotEqual(filename_utc, "file_20230515_103045.txt")

        mock_date_other = datetime(2023, 5, 15, 12, 30, 45)
        mock_datetime.now.return_value = mock_date_other
        filename_other = generate_unique_filename()
        self.assertNotEqual(filename_other, "file_20230515_123045.txt")


class WeatherService:
    def __init__(self, api_url="https://api.weather.example.com"):
        self.api_url = api_url

    def get_current_temperature(self, city):
        try:
            response = requests.get(f"{self.api_url}/weather/{city}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('temperature')
            elif response.status_code == 404:
                return None
            else:
                response.raise_for_status()
        except Timeout:
            return "Timeout error"
        except Exception as e:
            return f"Error: {str(e)}"


class TestWeatherService(unittest.TestCase):
    @patch('requests.get')
    def test_get_current_temperature_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"temperature": 25}
        mock_get.return_value = mock_response

        service = WeatherService()
        temperature = service.get_current_temperature("Warsaw")

        self.assertEqual(temperature, 25)
        mock_get.assert_called_once_with("https://api.weather.example.com/weather/Warsaw", timeout=5)

    @patch('requests.get')
    def test_get_current_temperature_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        service = WeatherService()
        temperature = service.get_current_temperature("NonExistentCity")

        self.assertIsNone(temperature)

    @patch('requests.get')
    def test_get_current_temperature_timeout(self, mock_get):
        mock_get.side_effect = Timeout("Connection timed out")
        service = WeatherService()
        result = service.get_current_temperature("Warsaw")
        self.assertEqual(result, "Timeout error")


class DataContainer:
    def __init__(self):
        self.data = {}
        self.list_data = []

    def __iadd__(self, item):
        self.list_data.append(item)
        return self

    def __getitem__(self, key):
        if isinstance(key, int):
            if 0 <= key < len(self.list_data):
                return self.list_data[key]
            raise IndexError("Index out of range")
        else:
            if key in self.data:
                return self.data[key]
            raise KeyError(f"Key '{key}' not found")

    def __str__(self):
        return f"DataContainer(data={self.data}, list_data={self.list_data})"

    def __len__(self):
        return len(self.list_data) + len(self.data)

    def __enter__(self):
        self._backup = (self.data.copy(), self.list_data.copy())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.data, self.list_data = self._backup
            del self._backup
            return True
        del self._backup
        return False

    def add(self, key, value):
        self.data[key] = value

    def remove(self, key):
        if isinstance(key, int):
            if 0 <= key < len(self.list_data):
                del self.list_data[key]
            else:
                raise IndexError("Index out of range")
        else:
            if key in self.data:
                del self.data[key]
            else:
                raise KeyError(f"Key '{key}' not found")


class TestDataContainer(unittest.TestCase):
    def test_iadd_operator(self):
        container = DataContainer()
        container += "test"
        container += 123
        self.assertEqual(container.list_data, ["test", 123])

    def test_getitem_by_index(self):
        container = DataContainer()
        container += "test"
        container += 123
        self.assertEqual(container[0], "test")
        self.assertEqual(container[1], 123)
        with self.assertRaises(IndexError):
            _ = container[2]

    def test_getitem_by_key(self):
        container = DataContainer()
        container.add("name", "John")
        container.add("age", 30)
        self.assertEqual(container["name"], "John")
        self.assertEqual(container["age"], 30)
        with self.assertRaises(KeyError):
            _ = container["nonexistent"]

    def test_str_representation(self):
        container = DataContainer()
        container += "test"
        container.add("key", "value")
        expected_str = "DataContainer(data={'key': 'value'}, list_data=['test'])"
        self.assertEqual(str(container), expected_str)

    def test_len_method(self):
        container = DataContainer()
        container += "item1"
        container += "item2"
        container.add("key1", "value1")
        container.add("key2", "value2")
        self.assertEqual(len(container), 4)

    def test_context_manager_success(self):
        container = DataContainer()
        container += "initial"
        container.add("key", "initial")

        with container as c:
            c += "new_item"
            c.add("new_key", "new_value")

        self.assertEqual(container.list_data, ["initial", "new_item"])
        self.assertEqual(container.data, {"key": "initial", "new_key": "new_value"})

    def test_context_manager_exception(self):
        container = DataContainer()
        container += "initial"
        container.add("key", "initial")

        try:
            with container as c:
                c += "new_item"
                c.add("new_key", "new_value")
                raise ValueError("Test exception")
        except ValueError:
            pass

        self.assertEqual(container.list_data, ["initial"])
        self.assertEqual(container.data, {"key": "initial"})

    def test_with_magic_mock(self):
        mock_container = MagicMock(spec=DataContainer)
        mock_container.__iadd__.return_value = mock_container
        result = mock_container.__iadd__("test")
        self.assertEqual(result, mock_container)
        mock_container.__iadd__.assert_called_with("test")

        mock_container.__getitem__.return_value = "mocked_value"
        value = mock_container.__getitem__(0)
        self.assertEqual(value, "mocked_value")
        mock_container.__getitem__.assert_called_with(0)

        mock_container.__len__.return_value = 5
        length = mock_container.__len__()
        self.assertEqual(length, 5)

    def test_event_sequence(self):
        mock_container = MagicMock(spec=DataContainer)
        mock_container.add("key1", "value1")
        mock_container.__iadd__("item1")
        mock_container.add("key2", "value2")

        expected_calls = [
            call.add("key1", "value1"),
            call.__iadd__("item1"),
            call.add("key2", "value2")
        ]

        mock_container.assert_has_calls(expected_calls, any_order=False)
        mock_container.assert_has_calls([
            call.add("key2", "value2"),
            call.add("key1", "value1")
        ], any_order=True)

    def test_mock_vs_magic_mock(self):
        regular_mock = MagicMock()
        magic_mock = MagicMock(spec=DataContainer)

        regular_mock.__len__.return_value = 5
        length = regular_mock.__len__()
        self.assertEqual(length, 5)

        magic_mock.__len__.return_value = 10
        self.assertEqual(magic_mock.__len__(), 10)


if __name__ == "__main__":
    unittest.main()