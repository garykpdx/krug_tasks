import unittest

from task.utils import get_daily_averages


class UtilTests(unittest.TestCase):
    def test_get_daily_averages_returns_null(self):
        result = get_daily_averages([('2016-01-01', 500), ('2016-01-03', 500), ('2016-01-04', 500)])
        self.assertListEqual([('2016-01-01', None), ('2016-01-03', None), ('2016-01-04', None)], result)

    def test_get_daily_averages_returns_average(self):
        result = get_daily_averages(
            [('2016-01-01', 800), ('2016-01-01', 700), ('2016-01-01', 700), ('2016-01-01', 1000)])
        self.assertListEqual([('2016-01-01', 800)], result)
