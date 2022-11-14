import unittest

from task.data_access import DataAccess


class RecordsTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_can_get_sub_regions(self):
        da = DataAccess()
        results = [r for r in da.get_all_subregions('china_main')]
        self.assertListEqual(['china_main', 'china_east_main', 'china_south_main', 'china_north_main'], results)
        da.close()

    def test_can_get_ports_from_regions(self):
        da = DataAccess()
        results = da.get_ports_from_regions(['finland_main'])
        self.assertListEqual(['FIHEL', 'FIKTK', 'FIRAU'], results)
        da.close()