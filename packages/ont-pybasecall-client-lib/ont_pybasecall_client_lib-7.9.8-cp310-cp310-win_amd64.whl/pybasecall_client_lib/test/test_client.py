#! /usr/bin/env python3

import importlib.resources
import os
import unittest

from pybasecall_client_lib import TEST_SERVER_PORT
from pybasecall_client_lib.client_lib import BasecallClient
from pybasecall_client_lib.helper_functions import basecall_with_pybasecall_client

# We will skip the tests if ont_fast5_api is not available.
FAST5_UNAVAILABLE = False
try:
    import ont_fast5_api  # noqa: F401
except Exception:
    FAST5_UNAVAILABLE = True

POD5_UNAVAILABLE = False
try:
    from pod5 import Reader as Pod5Reader  # noqa: F401
    from pod5 import ReadRecord as Pod5Read  # noqa: F401
except Exception:
    POD5_UNAVAILABLE = True


class TestBasecallClientLib(unittest.TestCase):
    # TEST_SERVER_PORT can be set automatically in the main __init__.py when a
    # server is started, but if it's not we'll check for an environment
    # variable.
    SERVER_ADDRESS = TEST_SERVER_PORT
    if SERVER_ADDRESS is None:
        SERVER_ADDRESS = os.environ.get("TEST_SERVER_PORT")
    DNA_CONFIG = "dna_r9.4.1_450bps_fast"
    MODEL_SET = "dna_r9.4.1_e8_fast@v3.4|dna_r9.4.1_e8_fast@v3.4_5mCG@v0.1|"
    DNA_FOLDER = "dna"
    print("Server address is {}".format(SERVER_ADDRESS))

    def setUp(self):
        data_dir = os.path.join("test", "data")
        ref = importlib.resources.files("pybasecall_client_lib") / data_dir
        with importlib.resources.as_file(ref) as path:
            self.data_path = path

    def tearDown(self):
        pass

    def test_00_basecalling_test(self):
        if TestBasecallClientLib.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server port has been set.")
        if FAST5_UNAVAILABLE and POD5_UNAVAILABLE:
            raise unittest.SkipTest("Could not import either ont-fast5-api or pod5.")
        input_folder = os.path.join(self.data_path, TestBasecallClientLib.DNA_FOLDER)
        client = BasecallClient(
            TestBasecallClientLib.SERVER_ADDRESS, TestBasecallClientLib.DNA_CONFIG
        )
        client.set_params({"client_name": "basecall_client_test_00_basecalling_test"})
        self.assertEqual(
            BasecallClient.disconnected,
            client.get_status(),
            "validate connection status disconnected prior to connect.",
        )
        result = client.connect()
        self.assertEqual(BasecallClient.success, result)
        self.assertEqual(
            BasecallClient.connected,
            client.get_status(),
            "validate connection status after connecting.",
        )
        try:
            basecall_with_pybasecall_client(client, input_folder)
        finally:
            client.disconnect()

    def test_01_basecalling_model_set_test(self):
        if TestBasecallClientLib.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server port has been set.")
        if FAST5_UNAVAILABLE and POD5_UNAVAILABLE:
            raise unittest.SkipTest("Could not import either ont-fast5-api or pod5.")
        input_folder = os.path.join(self.data_path, TestBasecallClientLib.DNA_FOLDER)
        client = BasecallClient(
            TestBasecallClientLib.SERVER_ADDRESS, TestBasecallClientLib.MODEL_SET
        )
        client.set_params(
            {"client_name": "basecall_client_test_01_basecalling_model_set_test"}
        )
        self.assertEqual(
            BasecallClient.disconnected,
            client.get_status(),
            "validate connection status disconnected prior to connect.",
        )
        result = client.connect()
        self.assertEqual(BasecallClient.success, result)
        self.assertEqual(
            BasecallClient.connected,
            client.get_status(),
            "validate connection status after connecting.",
        )
        try:
            basecall_with_pybasecall_client(client, input_folder)
        finally:
            client.disconnect()
