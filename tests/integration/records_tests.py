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

    def test_get_ports_from_regions_with_bad_regions(self):
        results = self.da.get_ports_from_regions(['does_not_exist'])
        self.assertListEqual([], results)

    def test_can_get_ports_from_regions2(self):
        results = self.da.get_ports_from_regions(['north_europe_main', 'uk_main'])
        self.assertListEqual(['NLRTM', 'BEZEE', 'FRLEH', 'DEBRV', 'BEANR', 'GBFXT', 'GBSOU', 'DEHAM'], results)

    def test_get_prices(self):
        orig_ports = ['CNDAL']
        dest_ports = ['NOHAU']
        date_from = date(2016, 1, 1)
        date_to = date(2016, 1, 2)
        result = self.da.get_prices(orig_ports, dest_ports, date_from, date_to)
        print(result)
        self.assertListEqual([('2016-01-01', 1383), ('2016-01-02', 1383)], result)

    def test_get_results(self):
        origin, dest = 'CNDAL', 'NOHAU'
        date_from, date_to = date(2016, 1, 1), date(2016, 1, 31)
        results = self.da.get_results(origin, dest, date_from, date_to)
        self.assertListEqual([('2016-01-01', None),('2016-01-02', None)], results, 'should be null both days')
