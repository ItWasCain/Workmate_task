import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock

from main import read_employees, get_rate_column, generate_payout_report


class TestMain(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

        # Валидный файл с rate
        f1 = tempfile.NamedTemporaryFile(
            mode='w+', suffix='.csv', delete=False
        )
        f1.write("name,department,hours_worked,rate\n")
        f1.write("John Doe,IT,40,25\n")
        f1.write("Jane Smith,HR,35,30\n")
        f1.close()
        self.temp_files.append(f1.name)

        # Валидный файл с hourly_rate
        f2 = tempfile.NamedTemporaryFile(
            mode='w+', suffix='.csv', delete=False
        )
        f2.write("name,department,hours_worked,hourly_rate\n")
        f2.write("Bob Johnson,IT,45,20\n")
        f2.close()
        self.temp_files.append(f2.name)

        # Файл с отсутствующим столбцом
        f3 = tempfile.NamedTemporaryFile(
            mode='w+', suffix='.csv', delete=False
        )
        f3.write("name,department,wage\n")
        f3.write("Alice Brown,Finance,50\n")
        f3.close()
        self.temp_files.append(f3.name)

        # Файл с невалидными данными
        f4 = tempfile.NamedTemporaryFile(
            mode='w+', suffix='.csv', delete=False
        )
        f4.write("name,department,hours_worked,rate\n")
        f4.write("Tom Wilson,Sales,invalid,15\n")
        f4.close()
        self.temp_files.append(f4.name)

    def tearDown(self):
        for f in self.temp_files:
            if os.path.exists(f):
                os.unlink(f)

    def test_read_employees_valid(self):
        employees = read_employees([self.temp_files[0], self.temp_files[1]])
        self.assertEqual(len(employees), 3)
        self.assertEqual(employees[0]['name'], "John Doe")
        self.assertEqual(employees[1]['hours_worked'], 35.0)
        self.assertEqual(employees[2]['hourly_rate'], 20.0)

    def test_read_employees_missing_columns(self):
        with self.assertRaises(ValueError):
            read_employees([self.temp_files[2]])

    def test_read_employees_invalid_data(self):
        with self.assertRaises(ValueError):
            read_employees([self.temp_files[3]])

    def test_get_rate_column(self):
        employee1 = {'name': 'John', 'rate': 25}
        employee2 = {'name': 'Jane', 'hourly_rate': 30}
        employee3 = {'name': 'Bob', 'salary': 40}

        self.assertEqual(get_rate_column(employee1), 'rate')
        self.assertEqual(get_rate_column(employee2), 'hourly_rate')
        self.assertEqual(get_rate_column(employee3), 'salary')

    def test_generate_payout_report(self):
        employees = [
            {
                'name': 'John',
                'department': 'IT',
                'hours_worked': 40,
                'rate': 25
            },
            {
                'name': 'Jane',
                'department':
                'HR',
                'hours_worked': 35,
                'rate': 30
            },
            {
                'name': 'Bob',
                'department':
                'IT',
                'hours_worked': 45,
                'rate': 20
            }
        ]

        table = generate_payout_report(employees)
        self.assertIsNotNone(table)

        table_str = str(table)
        self.assertIn("IT", table_str)
        self.assertIn("HR", table_str)
        self.assertIn("85.00", table_str)  # Сумма часов для IT
        self.assertIn("1900.00", table_str)  # сумма зарплаты для IT

    def test_generate_payout_report_empty(self):
        table = generate_payout_report([])
        self.assertIsNone(table)

    @patch('main.export_to_csv')
    @patch('main.argparse.ArgumentParser.parse_args')
    def test_main(self, mock_parse, mock_export):
        mock_args = MagicMock()
        mock_args.files = [self.temp_files[0]]
        mock_args.report = 'payout'
        mock_args.export = None
        mock_parse.return_value = mock_args

        with patch('builtins.print') as mock_print:
            import main
            main.main()

            self.assertTrue(mock_print.called)

        mock_args.export = 'report.csv'
        with patch('builtins.print') as mock_print:
            import main
            main.main()
            mock_export.assert_called_once()


if __name__ == '__main__':
    unittest.main()
