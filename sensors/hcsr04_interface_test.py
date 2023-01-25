import mock_csv_writer
import mock_hcsr04
import unittest
import hcsr04_interface
import time

class hcsr04_unittest(unittest.TestCase):
    @classmethod
    def setUp(self):
        self._hcsr04 = mock_hcsr04.mock_hcsr04()
        self._csv_writer = mock_csv_writer.mock_csv_writer()
        self._hcsr04_interface = hcsr04_interface.hcsr04_interface("HCSR04_Test", self._hcsr04, self._csv_writer)

    def test_init_sensor(self):
        ret = self._hcsr04_interface.init_sensor()
        self.assertTrue(ret)

    def test_start_data_collection(self):
        ret = self._hcsr04_interface.start_data_collection()
        self.assertTrue(ret)
        time.sleep(5)
        ret = self._hcsr04_interface.stop_data_collection()
        self.assertTrue(ret)

    def test_heartbeat(self):
        ret = self._hcsr04_interface.start_heartbeat()
        self.assertTrue(ret)
        time.sleep(10)
        ret = self._hcsr04_interface.stop_heartbeat()
        self.assertTrue(ret)
        

    

