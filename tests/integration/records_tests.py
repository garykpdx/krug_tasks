import unittest
from datetime import date

from task.data_access import DataAccess


class RecordsIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.da = DataAccess()

    def tearDown(self) -> None:
        self.da.close()

    def test_can_get_sub_regions(self):
        results = self.da.get_all_subregions('china_main')
        self.assertListEqual(['china_main', 'china_east_main', 'china_south_main', 'china_north_main'], results)

    def test_can_get_ports_from_regions(self):
        results = self.da.get_ports_from_regions(['finland_main'])
        self.assertListEqual(['FIHEL', 'FIKTK', 'FIRAU'], results)

    def test_get_prices(self):
        orig_ports = ['CNDAL']
        dest_ports = ['NOHAU']
        result = self.da.get_prices(orig_ports, dest_ports)
        self.assertListEqual([(date(2016, 1, 1), 1383), (date(2016, 1, 2), 1383)], result)
