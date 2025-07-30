import logging
import unittest

__version__ = "7.9.8"

TEST_SERVER_PORT = None

# Set up a default NullHandler in case we don't end up using another one
# Taken from http://docs.python-guide.org/en/latest/writing/logging/
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

def test(exit_on_completion=False, run_basecall_server=False, server_log_dir=None):
    import os
    import sys
    import shutil
    import unittest
    import tempfile
    from pybasecall_client_lib.helper_functions import run_server

    if server_log_dir is not None:
        log_path = server_log_dir
    else:
        log_path = tempfile.mkdtemp()
    config = 'dna_r9.4.1_450bps_fast.cfg'

    # Start the dorado_basecall_server
    server_args = ['--log_path', log_path,
                   '--config', config,
                   '--port', 'auto',
                   '--disable_pings'
                  ]
    if os.environ.get("USE_CUDA"):
        server_args.extend(["-x", "cuda:0"])
    elif os.environ.get("USE_METAL"):
        server_args.extend(["-x", "metal"])
    if run_basecall_server:
        server, port_string = run_server(server_args)
        assert(port_string != 'ERROR')
        global TEST_SERVER_PORT
        TEST_SERVER_PORT = port_string
    else:
        server, port_string = (None, 'skip')

    the_tests = unittest.defaultTestLoader.discover(
        os.path.join(os.path.dirname(__file__),
                     'test'))

    try:
        runner = unittest.TextTestRunner()
        test_run = runner.run(the_tests)
        success = test_run.wasSuccessful()
    finally:
        if server is not None:
            server.stdout.close()
            server.kill()
            server.wait()
        if server_log_dir is None:
            shutil.rmtree(log_path)

    if not exit_on_completion:
        return success
    elif success:
        sys.exit(0)
    else:
        sys.exit(1)
