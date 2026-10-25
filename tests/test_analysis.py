import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


class AnalysisTests(unittest.TestCase):
    def test_analysis_reproduces_the_archived_tables(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as folder:
            work = Path(folder)
            shutil.copytree(ROOT / 'src', work / 'src')
            shutil.copytree(ROOT / 'data', work / 'data')
            result = subprocess.run(
                [sys.executable, str(work / 'src/analyze.py')],
                cwd=work,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
                capture_output=True,
                text=True,
                encoding='utf-8',
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name in ['team_summary.csv', 'capacity_forecast.csv']:
                with self.subTest(output=name):
                    pd.testing.assert_frame_equal(
                        pd.read_csv(ROOT / 'output' / name),
                        pd.read_csv(work / 'output' / name),
                    )

    def test_csv_and_database_contain_the_same_records(self):
        with sqlite3.connect(ROOT / 'data/resource_ops.db') as connection:
            actual = pd.read_sql_query('SELECT * FROM resource_usage', connection)
        pd.testing.assert_frame_equal(pd.read_csv(ROOT / 'data/resource_usage.csv'), actual)


if __name__ == '__main__':
    unittest.main()
