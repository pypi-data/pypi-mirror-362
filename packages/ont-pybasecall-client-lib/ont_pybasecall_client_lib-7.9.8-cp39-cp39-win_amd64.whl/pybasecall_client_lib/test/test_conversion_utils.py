#! /usr/bin/env python3

import unittest

import numpy as np
from pybasecall_client_lib import client_lib


class TestConversionUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_00_metadata_to_dict(self):
        result = client_lib.test_metadata_to_dict()
        self.assertTrue("read_id" in result)
        self.assertEqual("Test read-id", result["read_id"])
        self.assertTrue("channel" in result)
        self.assertEqual(4, result["channel"])
        self.assertTrue("daq_scaling" in result)
        self.assertAlmostEqual(2.7, result["daq_scaling"], 4)
        self.assertTrue("duration" in result)
        self.assertEqual(12000450138, result["duration"])
        self.assertEqual(4, len(result))

    def test_01_datasets_to_dict(self):
        result = client_lib.test_datasets_to_dict()

        self.assertTrue("raw_data" in result)
        self.assertTrue(isinstance(result["raw_data"], np.ndarray))
        self.assertEqual(1000, result["raw_data"].size)
        for i, val in enumerate(result["raw_data"]):
            self.assertEqual(i, val)

        self.assertTrue("sequence" in result)
        self.assertTrue(isinstance(result["sequence"], str))
        self.assertEqual("ACGTCGTGTT", result["sequence"])

    def test_02_dict_to_readholder(self):
        read = client_lib.test_dict_to_readholder()
        self.assertEqual(4294967286, read["read_tag"])

        result = read["metadata"]
        self.assertEqual(5, len(result))
        self.assertTrue("read_id" in result)
        self.assertEqual("test_read", result["read_id"])
        self.assertTrue("daq_offset" in result)
        self.assertAlmostEqual(1.5, result["daq_offset"], 4)
        self.assertTrue("daq_scaling" in result)
        self.assertAlmostEqual(2.5, result["daq_scaling"], 4)
        self.assertIn("sampling_rate", result)
        self.assertEqual(5.5, result["sampling_rate"])
        self.assertIn("start_time", result)
        self.assertEqual(6, result["start_time"])

        result = read["datasets"]
        self.assertEqual(1, len(result))

        self.assertTrue("raw_data" in result)
        self.assertTrue(isinstance(result["raw_data"], np.ndarray))
        self.assertEqual(100, result["raw_data"].size)
        for i, val in enumerate(result["raw_data"]):
            self.assertEqual(i, val)

    def test_03_readholder_to_dict(self):
        read = client_lib.test_readholder_to_dict()
        self.assertEqual(4294967286, read["read_tag"])
        self.assertEqual(client_lib.BasecallClient.medium_priority, read["priority"])

        result = read["metadata"]
        self.assertTrue("read_id" in result)
        self.assertEqual("Test read-id", result["read_id"])
        self.assertTrue("channel" in result)
        self.assertTrue("daq_offset" in result)
        self.assertAlmostEqual(1.8, result["daq_offset"], 4)
        self.assertEqual(4, result["channel"])
        self.assertTrue("daq_scaling" in result)
        self.assertAlmostEqual(2.7, result["daq_scaling"], 4)
        self.assertTrue("duration" in result)
        self.assertEqual(12000450138, result["duration"])
        self.assertEqual(5, len(result))

        result = read["datasets"]
        self.assertEqual(2, len(result))

        self.assertTrue("raw_data" in result)
        self.assertTrue(isinstance(result["raw_data"], np.ndarray))
        self.assertEqual(1000, result["raw_data"].size)
        for i, val in enumerate(result["raw_data"]):
            self.assertEqual(i, val)

        self.assertTrue("sequence" in result)
        self.assertTrue(isinstance(result["sequence"], str))
        self.assertEqual("ACGTCGTGTT", result["sequence"])

    def test_04_str_list_concat(self):
        input = ["token1", "token2", "token3"]
        (success, s) = client_lib.test_str_list_concat(input)
        self.assertTrue(success)
        self.assertEqual("token1 token2 token3", s)

        input = [1, 2, 3]
        (success, _) = client_lib.test_str_list_concat(input)
        self.assertFalse(success)

    def test_05_config_details_to_dict(self):
        cfgdets = client_lib.test_config_details_to_dict()
        self.assertEqual("test_config_filename.cfg", cfgdets["config_name"])
        self.assertEqual(1, cfgdets["model_stride"])
        self.assertEqual("test_model_type", cfgdets["model_type"])
        self.assertEqual(False, cfgdets["duplex"])
