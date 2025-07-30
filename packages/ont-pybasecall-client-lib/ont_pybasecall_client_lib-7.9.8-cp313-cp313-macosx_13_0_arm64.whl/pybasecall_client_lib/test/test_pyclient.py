#! /usr/bin/env python3

import importlib.resources
import os
import time
import unittest
from pathlib import Path

import numpy as np

DEBUG = os.getenv("BUILD_TYPE", "Release").upper() == "DEBUG"

from pybasecall_client_lib import TEST_SERVER_PORT

if DEBUG:
    from pybasecall_client_lib.client_libd import BasecallClient
else:
    from pybasecall_client_lib.client_lib import BasecallClient

from pybasecall_client_lib.helper_functions import (
    basecall_with_pybasecall_client,
    get_barcode_kits,
    get_return_code_message,
    get_server_information,
    get_server_stats,
    package_read,
    pull_read,
)
from pybasecall_client_lib.pyclient import PyBasecallClient

# We will skip some tests if ont_fast5_api or pod5 is not available.
FAST5_UNAVAILABLE = False
try:
    from ont_fast5_api.fast5_interface import get_fast5_file
except Exception:
    FAST5_UNAVAILABLE = True

POD5_UNAVAILABLE = False
try:
    from pod5 import Read as Pod5Read  # noqa: F401
    from pod5 import Reader as Pod5Reader
except Exception:
    POD5_UNAVAILABLE = True


class TestPyBasecallClient(unittest.TestCase):
    # TEST_SERVER_PORT can be set automatically in the main __init__.py when a
    # server is started, but if it's not we'll check for an environment
    # variable.
    SERVER_ADDRESS = TEST_SERVER_PORT

    if SERVER_ADDRESS is None:
        SERVER_ADDRESS = os.environ.get("TEST_SERVER_PORT")

    DNA_CONFIG = "dna_r9.4.1_450bps_fast"
    DNA_FOLDER = "dna"
    MODEL_SET = "dna_r9.4.1_e8_fast@v3.4|dna_r9.4.1_e8_fast@v3.4_5mCG@v0.1|"
    print("Server address is {}".format(SERVER_ADDRESS))

    def setUp(self):
        data_dir = os.path.join("test", "data")
        ref = importlib.resources.files("pybasecall_client_lib") / data_dir
        with importlib.resources.as_file(ref) as path:
            self.data_path = path

    def tearDown(self):
        pass

    def test_00_connection(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server port has been set.")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params({"client_name": "basecall_client_test_00_connection"})
        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

        client.disconnect()
        self.assertEqual(client.get_status(), PyBasecallClient.disconnected)

    def test_01_connection_raises(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        client = PyBasecallClient(
            "test_invalid_port", TestPyBasecallClient.DNA_CONFIG, retries=1
        )
        client.set_params({"client_name": "basecall_client_test_01_connection_raises"})

        with self.assertRaises(ConnectionError):
            client.connect()

    def test_02_barcode_raises(self):

        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")

        barcode_kits = [
            k.get("kit_name")
            for k in get_barcode_kits(TestPyBasecallClient.SERVER_ADDRESS, 5000)
        ]

        if not barcode_kits:
            raise unittest.SkipTest("No barcode kits retrieved")

        # Reverse barcode kit name to raise error
        kit = barcode_kits[0][::-1]

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
            barcode_kits=[
                kit,
            ],
            retries=1,
        )
        client.set_params({"client_name": "basecall_client_test_02_barcode_raises"})
        with self.assertRaises(ValueError):
            client.connect()

    def test_03_already_connected(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params({"client_name": "basecall_client_test_03_already_connected"})
        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

    def test_04_pass_fast5_reads_and_get_completed(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if FAST5_UNAVAILABLE:
            raise unittest.SkipTest("ont_fast5_api unavailable")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params(
            {
                "client_name": "basecall_client_test_04_pass_fast5_reads_and_get_completed"
            }
        )
        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

        sent = 0
        recv = 0

        sent_ids = set()
        recv_ids = set()

        input_folder = Path(self.data_path, TestPyBasecallClient.DNA_FOLDER)
        for single_read_file in input_folder.glob("*.fast5"):
            with get_fast5_file(single_read_file, mode="r") as f5:
                f5_read = f5.get_read(f5.get_read_ids()[0])
                read = package_read(**pull_read(f5_read))
            status = client.pass_read(read)
            if status:
                sent += 1
                sent_ids.add(read["read_id"])

        while recv < sent:
            reads = client.get_completed_reads()
            recv += len(reads)
            for split_read in reads:
                for read in split_read:
                    recv_ids.add(read["metadata"]["read_id"])
            time.sleep(0.1)

        self.assertEqual(sent_ids, recv_ids)

    def test_05_pass_pod5_reads_and_get_completed(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if POD5_UNAVAILABLE:
            raise unittest.SkipTest("pod5 unavailable")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params(
            {"client_name": "basecall_client_test_05_pass_pod5_reads_and_get_completed"}
        )
        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

        sent = 0
        recv = 0

        sent_ids = set()
        recv_ids = set()

        input_folder = Path(self.data_path, TestPyBasecallClient.DNA_FOLDER)
        for single_read_file in input_folder.glob("*.pod5"):
            with Pod5Reader(single_read_file) as reader:
                record = next(reader.reads())
                read = package_read(**pull_read(record))
            status = client.pass_read(read)
            if status:
                sent += 1
                sent_ids.add(read["read_id"])

        while recv < sent:
            reads = client.get_completed_reads()
            recv += len(reads)
            for split_read in reads:
                for read in split_read:
                    recv_ids.add(read["metadata"]["read_id"])
            time.sleep(0.1)

        self.assertEqual(sent_ids, recv_ids)

    def test_06_pass_read_malformed(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if FAST5_UNAVAILABLE:
            raise unittest.SkipTest("ont_fast5_api unavailable")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params(
            {"client_name": "basecall_client_test_06_pass_read_malformed"}
        )
        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

        input_folder = Path(self.data_path, TestPyBasecallClient.DNA_FOLDER)
        reads = []
        for single_read_file in input_folder.glob("*.fast5"):
            with get_fast5_file(single_read_file, mode="r") as f5:
                f5_read = f5.get_read(f5.get_read_ids()[0])
                reads.append(package_read(**pull_read(f5_read)))

        if reads:
            read = reads[0]

        # Send greater than 32 bit read_tag
        with self.assertRaises(ValueError):
            mal_read = read.copy()
            mal_read["read_tag"] = int(2**32)
            self.assertGreater(mal_read["read_tag"].bit_length(), 32)
            _ = client.pass_read(mal_read)

        # Send raw data as a list (not ndarray)
        with self.assertRaises(ValueError):
            mal_read = read.copy()
            mal_read["raw_data"] = list(mal_read["raw_data"])
            self.assertIsInstance(mal_read["raw_data"], list)
            _ = client.pass_read(mal_read)

        # Sending non float for daq scaling
        with self.assertRaises(ValueError):
            mal_read = read.copy()
            mal_read["daq_scaling"] = int(mal_read["daq_scaling"])
            self.assertIsInstance(mal_read["daq_scaling"], int)
            _ = client.pass_read(mal_read)

        # Sending non float for daq offset
        with self.assertRaises(ValueError):
            mal_read = read.copy()
            mal_read["daq_offset"] = int(mal_read["daq_offset"])
            self.assertIsInstance(mal_read["daq_offset"], int)
            _ = client.pass_read(mal_read)

        # Sending empty read_id
        # I think this test will fail, the BasecallClient states the read_id
        #   should _not_ be empty, but it accepts them anyway?
        with self.assertRaises(ValueError):
            mal_read = read.copy()
            mal_read["read_id"] = ""
            self.assertFalse(mal_read["read_id"])
            _ = client.pass_read(mal_read)

        # Send a read with length 0. This should not get sent to the server,
        #   nor should it cause an error. The read should get returned without
        #   having been basecalled.
        mal_read1 = read.copy()
        mal_read1["raw_data"] = np.zeros(0, dtype=np.int16)
        self.assertTrue(client.pass_read(mal_read1))
        time.sleep(1)
        # If the read was sent, and crashed the server, the following will time out.
        finished = client.get_completed_reads()
        self.assertEqual(len(finished), 1)
        self.assertEqual(len(finished[0]), 1)
        # Repeat using pass_reads(), which previously incorrectly sent zero length
        #   reads to the server, which crashed the server.
        mal_read2 = read.copy()
        mal_read2["raw_data"] = np.zeros(0, dtype=np.int16)
        self.assertTrue(client.pass_reads([mal_read2]))
        time.sleep(1)
        # If the read was sent, and crashed the server, the following will time out.
        finished = client.get_completed_reads()
        self.assertEqual(len(finished), 1)
        self.assertEqual(len(finished[0]), 1)

    def test_07_pass_read_connection_error(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if FAST5_UNAVAILABLE:
            raise unittest.SkipTest("ont_fast5_api unavailable")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params(
            {"client_name": "basecall_client_test_07_pass_read_connection_error"}
        )

        input_folder = Path(self.data_path, TestPyBasecallClient.DNA_FOLDER)
        reads = []
        for single_read_file in input_folder.glob("*.fast5"):
            with get_fast5_file(single_read_file, mode="r") as f5:
                f5_read = f5.get_read(f5.get_read_ids()[0])
                reads.append(package_read(**pull_read(f5_read)))

        with self.assertRaises(ConnectionError):
            read = reads.pop()
            _ = client.pass_read(read)

    def test_08_get_completed_reads_raises(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS, TestPyBasecallClient.DNA_CONFIG
        )
        client.set_params(
            {"client_name": "basecall_client_test_08_get_completed_reads_raises"}
        )

        with self.assertRaises(ConnectionError):
            _ = client.get_completed_reads()

    def test_09_context_manager(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params({"client_name": "basecall_client_test_09_context_manager"})

        with client as caller:
            self.assertIsInstance(caller, PyBasecallClient)
            self.assertEqual(caller.get_status(), PyBasecallClient.connected)

        self.assertEqual(client.get_status(), PyBasecallClient.disconnected)

    def test_10_set_params_already_connected(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params(
            {"client_name": "basecall_client_test_10_set_params_already_connected"}
        )

        with self.assertRaises(RuntimeError):
            with client as caller:
                caller.set_params({"query_timeout": 10000})

    def test_11_set_params(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
            query_timeout=1000,
        )
        client.set_params({"client_name": "basecall_client_test_11_set_params"})

        with self.assertRaises(ValueError):
            client = PyBasecallClient(
                TestPyBasecallClient.SERVER_ADDRESS,
                TestPyBasecallClient.DNA_CONFIG,
                this_is_not_a_server_param="undefined",
            )

    def test_12_config_with_suffix(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")

        config = TestPyBasecallClient.DNA_CONFIG + ".cfg"

        client = PyBasecallClient(TestPyBasecallClient.SERVER_ADDRESS, config)
        client.set_params({"client_name": "basecall_client_test_12_config_with_suffix"})
        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

        client.disconnect()
        self.assertEqual(client.get_status(), PyBasecallClient.disconnected)

    def test_13_get_server_stats(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if FAST5_UNAVAILABLE:
            raise unittest.SkipTest("ont_fast5_api unavailable")

        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS,
            TestPyBasecallClient.DNA_CONFIG,
        )
        client.set_params({"client_name": "basecall_client_test_13_get_server_stats"})
        client.connect()
        self.assertEqual(client.get_status(), PyBasecallClient.connected)

        sent = 0
        recv = 0

        sent_ids = set()
        recv_ids = set()

        input_folder = Path(self.data_path, TestPyBasecallClient.DNA_FOLDER)
        for single_read_file in input_folder.glob("*.fast5"):
            with get_fast5_file(single_read_file, mode="r") as f5:
                f5_read = f5.get_read(f5.get_read_ids()[0])
                read = package_read(**pull_read(f5_read))
            status = client.pass_read(read)
            if status:
                sent += 1
                sent_ids.add(read["read_id"])

        while recv < sent:
            reads = client.get_completed_reads()
            recv += len(reads)
            for split_read in reads:
                for read in split_read:
                    recv_ids.add(read["metadata"]["read_id"])
            time.sleep(0.1)

        self.assertEqual(sent_ids, recv_ids)
        server_stats = get_server_stats(TestPyBasecallClient.SERVER_ADDRESS, 5000)
        # check lifetime_reads_in after processing, otherwise we may request this info while the message is still queued
        self.assertGreaterEqual(server_stats["lifetime_reads_in"], sent)
        self.assertGreaterEqual(server_stats["lifetime_reads_out"], recv)
        self.assertEqual(1, len(server_stats["client_statistics"]))

    def test_14_get_server_information(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if FAST5_UNAVAILABLE:
            raise unittest.SkipTest("ont_fast5_api unavailable")

        guppy_version = list(BasecallClient.get_software_version())
        protocol_version = list(BasecallClient.get_protocol_version())
        server_info = get_server_information(TestPyBasecallClient.SERVER_ADDRESS, 5000)

        # The versions in server_info are strings, and may include build information after the patch version.
        server_guppy_version = server_info["guppy_version"].replace("+", ".").split(".")
        self.assertGreaterEqual(len(server_guppy_version), 3)
        server_guppy_version = [int(x) for x in server_guppy_version[0:3]]
        self.assertEqual(guppy_version, server_guppy_version)
        server_protocol_version = (
            server_info["protocol_version"].replace("+", ".").split(".")
        )
        self.assertGreaterEqual(len(server_protocol_version), 3)
        server_protocol_version = [int(x) for x in server_protocol_version[0:3]]
        self.assertEqual(protocol_version, server_protocol_version)

    def test_15_return_code_messages(self):
        # pybind11 enums aren't directly iterable, so the following workaround is required.
        for name, enum_value in BasecallClient.result.__members__.items():
            exception_type, message = get_return_code_message(enum_value)
            # If a return code as been added to BasecallClient.result, but is not handled by the
            # get_return_code_message function, then this test should fail.
            self.assertIsNotNone(
                message,
                "Return code {} not supported by get_return_code_message method.".format(
                    enum_value
                ),
            )

    def test_16_basecall_with_pybasecall_client(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if FAST5_UNAVAILABLE and POD5_UNAVAILABLE:
            raise unittest.SkipTest("ont_fast5_api and pod5 unavailable")
        input_folder = os.path.join(self.data_path, TestPyBasecallClient.DNA_FOLDER)
        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS, TestPyBasecallClient.DNA_CONFIG
        )
        client.set_params(
            {"client_name": "basecall_client_test_16_basecall_with_pybasecall_client"}
        )
        self.assertEqual(
            BasecallClient.disconnected,
            client.get_status(),
            "validate connection status prior to connect.",
        )
        client.connect()
        self.assertEqual(
            BasecallClient.connected,
            client.get_status(),
            "validate connection status after connecting.",
        )
        basecall_with_pybasecall_client(client, input_folder)
        self.assertEqual(
            BasecallClient.disconnected,
            client.get_status(),
            "validate connection status after basecall_with_pybasecall_client.",
        )

    def test_17_model_set_config(self):
        if TestPyBasecallClient.SERVER_ADDRESS is None:
            raise unittest.SkipTest("No server specified")
        if FAST5_UNAVAILABLE and POD5_UNAVAILABLE:
            raise unittest.SkipTest("ont_fast5_api and pod5 unavailable")
        input_folder = os.path.join(self.data_path, TestPyBasecallClient.DNA_FOLDER)
        client = PyBasecallClient(
            TestPyBasecallClient.SERVER_ADDRESS, TestPyBasecallClient.MODEL_SET
        )
        client.set_params({"client_name": "basecall_client_test_17_model_set_config"})
        self.assertEqual(
            BasecallClient.disconnected,
            client.get_status(),
            "validate connection status prior to connect.",
        )
        client.connect()
        self.assertEqual(
            BasecallClient.connected,
            client.get_status(),
            "validate connection status after connecting.",
        )
        basecall_with_pybasecall_client(client, input_folder)
        self.assertEqual(
            BasecallClient.disconnected,
            client.get_status(),
            "validate connection status after basecall_with_pybasecall_client.",
        )
