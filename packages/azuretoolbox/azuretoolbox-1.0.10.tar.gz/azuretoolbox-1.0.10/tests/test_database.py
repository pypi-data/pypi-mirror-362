import unittest
from unittest.mock import patch
from tests.mocks import mock_imports
from datetime import datetime
from decimal import Decimal


@patch.dict('os.environ', {
    'AzureSql_Server': 'test_server',
    'AzureSql_Database': 'test_database'})
class TestDatabase(unittest.TestCase):
    @mock_imports()
    def get_database(self):
        from src.azuretoolbox.database import Database
        return Database()

    def test_database_connection_returns_true(self):
        # Arrange
        db = self.get_database()

        # Act
        result = db.connect('test_server', 'test_database',
                            'test_user', 'test_password')

        # Assert
        self.assertTrue(result)

    def test_database_disconnection_returns_true_when_connection_is_not_open(self):
        # Arrange
        db = self.get_database()

        # Act
        result = db.disconnect()

        # Assert
        self.assertTrue(result)

    def test_database_disconnection_returns_true_when_connection_is_open(self):
        # Arrange
        db = self.get_database()
        db.connect(
            'test_server', 'test_database',
            'test_user', 'test_password')

        # Act
        result = db.disconnect()

        # Assert
        self.assertTrue(result)

    def test_database_query_returns_expected_values(self):
        # Arrange
        db = self.get_database()
        db.connect(
            'test_server', 'test_database',
            'test_user', 'test_password')

        # Act & Assert
        self.assertIsNotNone(db.query('SELECT 1'))

    def test_database_query_raises_exception_when_connection_is_not_open(self):
        # Arrange
        db = self.get_database()

        # Act & Assert
        with self.assertRaises(Exception) as context:
            db.query('SELECT 1')
        self.assertEqual(
            str(context.exception), 'Connection not established')

    def test_parsing_response_returns_expected_values(self):
        # Arrange
        db = self.get_database()
        response = [(1, 'test')]
        header = (('id', None), ('name', None))

        # Act
        result = db.__parse__(response, header)

        # Assert
        self.assertEqual(result, [{'id': 1, 'name': 'test'}])

    def test_parsing_response_returns_expected_date(self):
        # Arrange
        db = self.get_database()
        response = [(1, 'test', datetime.strptime(
            '2024-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'))]
        header = (('id', None), ('name', None), ('date', None))

        # Act
        result = db.__parse__(response, header)

        # Assert
        self.assertEqual(
            result, [{'id': 1, 'name': 'test', 'date': '2024-01-01 00:00:00'}])

    def test_parsing_response_returns_expected_float(self):
        # Arrange
        db = self.get_database()
        response = [(1, 'test', Decimal('1.0'))]
        header = (('id', None), ('name', None), ('decimal', None))

        # Act
        result = db.__parse__(response, header)

        # Assert
        self.assertEqual(
            result, [{'id': 1, 'name': 'test', 'decimal': 1.0}])

    def test_parsing_response_returns_expected_undefined_value(self):
        # Arrange
        db = self.get_database()
        response = [(1, 'test', None)]
        header = (('id', None), ('name', None), ('undefined', None))

        # Act
        result = db.__parse__(response, header)

        # Assert
        self.assertEqual(
            result, [{'id': 1, 'name': 'test', 'undefined': None}])

    def test_parsing_response_returns_expected_bytes(self):
        # Arrange
        db = self.get_database()
        response = [(1, 'test', b'test')]
        header = (('id', None), ('name', None), ('bytes', None))

        # Act
        result = db.__parse__(response, header)

        # Assert
        self.assertEqual(
            result, [{'id': 1, 'name': 'test', 'bytes': 'test'}])

    def test_updating_record_returns_true(self):
        # Arrange
        db = self.get_database()
        db.connect(
            'test_server', 'test_database',
            'test_user', 'test_password')

        # Act
        result = db.command('UPDATE test_table SET test_column = 1')

        # Assert
        self.assertTrue(result)

    def test_updating_record_raises_exception_when_connection_is_not_open(self):
        # Arrange
        db = self.get_database()

        # Act & Assert
        with self.assertRaises(Exception) as context:
            db.command('UPDATE test_table SET test_column = 1')
        self.assertEqual(
            str(context.exception), 'Connection not established')


if __name__ == '__main__':
    unittest.main()
