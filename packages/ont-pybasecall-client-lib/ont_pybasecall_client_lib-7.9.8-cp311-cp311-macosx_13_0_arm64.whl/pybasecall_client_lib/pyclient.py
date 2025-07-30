import time
from typing import Any, Callable, List, Union

from pybasecall_client_lib.client_lib import BasecallClient
from pybasecall_client_lib.helper_functions import get_return_code_message


class PyBasecallClient(BasecallClient):
    """Python client interface to dorado_basecall_server

    Any optional server parameters can be accessed via the ``params`` attribute

    :param address: The formatted address and port for the dorado_basecall_server,
        eg '127.0.0.1:5555'
    :type address: str
    :param config: The basecalling config to initialise the server with. This can take the form of
        a config file name or a model set.  Model sets are specified as a canonical basecall model,
        followed by a `|` character, then a comma-separated list of (possibly zero) modbase models,
        followed by a `|` character and then an optional duplex model.
    :type config: str
    :param throttle: Time, in seconds, to delay repeated requests to the server
    :type throttle: float
    :param retries: Number of retry attempts when sending data, if the server is
        not ready
    :type retries: int
    :param num_client_threads: Number of client worker threads for communicating
        with server.
    :type num_client_threads: int
    :param kwargs: Any optional server parameters can be set as keyword arguments
        and will be passed to the server. To see available server parameters see
        the help text for ``set_params``.

    .. note::
        Some server parameters, this list may be incomplete:
            * ``barcode_kits`` `(list)` Strings naming each barcode kit to use. Default is to
                not do barcoding.
            * ``query_timeout`` `(int)` Milliseconds to wait for a server response before timing
                out. Default is 2000.
            * ``connection_timeout`` `(int)` Milliseconds to wait for a server connection attempt.
                Default is 15000ms.
            * ``reconnect_timeout`` `(int)` Seconds to wait for the client to reconnect to the server
                if the connection is broken. Default is 300s.
            * ``max_message_size`` `(int)` Size of blocks to be sent to the server, in samples.
                Default is 256000.
            * ``max_reads_queued`` `(int)` Maximum number of reads (or read batches) to queue for sending
                to the server. Default is 20.
            * ``max_server_read_failures`` `(int)` Maximum number of times a read can be in-flight when the
                client has to reconnect before the client will stop resubmitting the in-flight reads.
                Default is 10.
            * ``priority`` `(ReadPriority)` Priority of the client (low, medium, or high). Default is
                medium.
            * ``move_enabled`` `(bool)` Flag indicating whether to return move data. Default is False.
            * ``barcode_trimming_enabled`` `(bool)` Flag indicating that barcodes should be
                trimmed. Default is False.
            * ``align_ref`` `(str)` Filename of index file to use for alignment
                (if any). Default is to not align.
            * ``bed_file`` `(str)` Filename of BED file to use for alignment (if any). Default
                is to not align.
            * ``server_file_load_timeout`` `(int)` Seconds to wait for files to be loaded on
                the server. Default is 180.
            * ``require_barcodes_both_ends`` `(bool)` Flag indicating that barcodes must be at
                both ends. Default is False.
            * ``chunk_size`` `(int)`  For adaptive sampling. Specify the chunk-size for basecalling. If you are
                truncating reads, send the value you are truncating to.

    :Example:

    >>> client = PyBasecallClient(
        "127.0.0.1:5555",
        "dna_r9.4.1_450bps_fast",
        align_ref="/path/to/index.mmi",
        bed_file="/path/to/targets.bed"
    )
    >>> client.connect()

    .. note:: ``BasecallClient`` does `not` raise raise_errors. Each time an
        action is made a code is returned and must be checked.

         - ``result.align_index_unavailable``
         - ``result.already_connected``
         - ``result.barcode_kit_unavailable``
         - ``result.basecall_config_unavailable``
         - ``result.bed_file_unavailable``
         - ``result.failed``
         - ``result.invalid_response``
         - ``result.no_connection``
         - ``result.not_ready``
         - ``result.success``
         - ``result.timed_out``
    """

    def __init__(
        self,
        address: str,
        config: str,
        throttle: float = 0.01,
        retries: int = 5,
        num_client_threads: int = 1,
        **kwargs,
    ):
        # Set instance vars
        self.address = address
        self.config = config
        self.throttle = throttle
        self.num_clients = num_client_threads
        self.params = kwargs

        # Allow config to use '.cfg' suffix
        suffix = ".cfg"
        if self.config.endswith(suffix):
            self.config = self.config[: -len(suffix)]

        # When server is not ready, how many times should we attempt
        #   to send a read
        self.pass_attempts = retries

        # Init base class
        super().__init__(self.address, self.config, self.num_clients)

        # Pass any params
        self.set_params(self.params)

    def connect(self):
        """Connect to the dorado_basecall_server

        On first connection external files will be loaded (minimap2 index and
        bed file), the ``server_file_load_timeout`` parameter should be set
        if these will take >30 seconds to load.

        :raises ConnectionError: When cannot connect, the connection attempt
            times out, or an invalid response is received
        :raises ValueError: When the barcode kit or a requested file is unavailable.
        :raises RuntimeError: When an undefined return code is returned

        :returns: None

        .. Note::
        If attempting to connect when already connected, the return code will be
        ``already_connected``, but the client will remain connected.
        """
        return_code = super().connect()
        if return_code in [self.already_connected, self.connected]:
            return

        tries = 0
        while self.get_status() != self.connected:
            # Should be in error state, so clear
            self.disconnect()
            return_code = super().connect()
            tries += 1
            if tries >= self.pass_attempts:
                break
            time.sleep(self.throttle)
        else:
            # Should only get here if status is connected
            return

        # Handle return_code
        if return_code == self.success:
            return
        elif return_code == self.failed:
            raise ConnectionError(
                "Could not connect. Is the server running? Check your connection parameters. {!r} : {}".format(
                    return_code, self.get_error_message()
                )
            )
        else:
            exception_type, exception_message = get_return_code_message(return_code)
            if exception_type is None or exception_message is None:
                raise RuntimeError(
                    "Something has gone wrong in the client software: {!r}".format(
                        return_code
                    )
                )
            raise exception_type(exception_message)

    def __repr__(self):
        return (
            "{}(address={!r},"
            " config={!r},"
            " align_ref={!r},"
            " bed_file={!r},"
            " barcodes={!r},"
            " {}, {})"
        ).format(
            self.__class__.__name__,
            self.address,
            self.config,
            self.params.get("align_ref", None),
            self.params.get("bed_file", None),
            self.params.get("barcode_kits", None),
            self.get_status(),
            self.get_error_message(),
        )

    def pass_read(
        self,
        read: Union[dict, Any],
        package_function: Callable[..., dict] = lambda x: x,
    ):
        """Pass a read to the basecall server

        If ``read`` is a dict it must be initialised with the following fields:
            - ``read_tag`` (`int`) 32-bit unsigned integer.
            - ``read_id`` (`str`) Non-empty string.
            - ``raw_data`` (`numpy.ndarray[numpy.int16]`) 1D NumPy array of int 16.
            - ``daq_offset`` (`float`) Offset value for conversion to pA.
            - ``daq_scaling`` (`float`) Scaling value for conversion to pA.
            - ``start_time`` (`int`) 64-bit uint, start time of the read (in samples).
              relative to the experiment start time.
            - ``sampling_rate`` (`float`) The sampling rate of the raw read data.

        If ``read`` is a dict it may also optionally contain the following fields:
            - ``channel`` (`int`): The channel the read came from.
            - ``mux`` (`int`): The mux the read came from.
            - ``run_id`` (`str`): Non-empty string containing the unique run-id.
            - ``sequencing_kit`` (`str`): Non-empty string indicating the
              sequencing-kit used.
            - ``end_reason`` (`str`): Non-empty string indicating the reason the
              read ended.

        Note that duplex basecalling requires the ``channel``, ``mux``, and ``run_id``
        fields in order to properly pair reads. The ``sequencing_kit`` field is needed
        if you want to enable adapter and/or primer trimming.

        :param read: Either a packaged read or object that can be packaged by
            package_function
        :type read: dict or Any
        :param package_function: optional callback function that should return
            a packaged read
        :type package_function: callable

        :raises ValueError: When send fails, this is usually returned when the
            read is malformed
        :raises ConnectionError: Raised when there is no connection
        :raises RuntimeError: Raised when an undefined response is returned

        :return: True if read sent successfully, otherwise False
        :rtype: bool
        """
        current_status = self.get_status()
        if current_status != self.connected:
            raise ConnectionError(
                "Not connected to server. status code: {!r}. {!r}".format(
                    current_status, self
                )
            )

        # Make first attempt to pass read to the server
        read = package_function(read)
        return_code = super().pass_read(read)
        if return_code == self.read_accepted:
            # Read passed successfully, return
            return True

        # Read failed to send
        # reattempt sending if not_ready or handle errors
        for _ in range(self.pass_attempts):
            if return_code == self.queue_full:
                time.sleep(self.throttle)
                return_code = super().pass_read(read)
            else:
                break

        if return_code == self.read_accepted:
            return True
        elif return_code == self.queue_full:
            return False
        elif return_code == self.bad_read:
            raise ValueError(
                "Something went wrong, read dict might be malformed. return_code: {!r}".format(
                    return_code
                )
            )
        elif return_code == self.not_accepting_reads:
            raise ConnectionError(
                "Not accepting reads (disconnected or finished). return_code: {!r}".format(
                    return_code
                )
            )
        else:
            raise RuntimeError("Undefined return_code: {!r}".format(return_code))

    def pass_reads(self, reads):
        """Pass multiple reads to the basecall server

        :param reads: A list of read dicts formatted as with the pass_read method.
        :type reads: list

        :raises ValueError: When send fails, this is usually returned when a
            read is malformed
        :raises ConnectionError: Raised when there is no connection
        :raises RuntimeError: Raised when an undefined response is returned

        :return: True if reads sent successfully, otherwise False
        :rtype: bool

        The reads will be sent to the server in batches, with the requirement that a batch of reads
        will not have a total combined length (in samples) exceeding the maximum message size. Note
        that the client will accept the reads as long as its input queue is not already full. The
        caller should make sure that the number of reads passed to the client in a single call to
        this function is not excessive, to avoid using too much memory.
        """
        current_status = self.get_status()
        if current_status != self.connected:
            raise ConnectionError(
                "Not connected to server. status code: {!r}. {!r}".format(
                    current_status, self
                )
            )

        # Make first attempt to pass reads to the server
        return_code = super().pass_reads(reads)
        if return_code == self.read_accepted:
            # Reads passed successfully, return
            return True

        # Reads failed to send
        # reattempt sending if not_ready or handle errors
        for _ in range(self.pass_attempts):
            if return_code == self.queue_full:
                time.sleep(self.throttle)
                return_code = super().pass_reads(reads)
            else:
                break

        if return_code == self.read_accepted:
            return True
        elif return_code == self.queue_full:
            return False
        elif return_code == self.bad_read:
            raise ValueError(
                "Something went wrong, read dict might be malformed. return_code: {!r}".format(
                    return_code
                )
            )
        elif return_code == self.not_accepting_reads:
            raise ConnectionError(
                "Not accepting reads (disconnected or finished). return_code: {!r}".format(
                    return_code
                )
            )
        else:
            raise RuntimeError("Undefined return_code: {!r}".format(return_code))

    def get_completed_reads(self) -> List[List[dict]]:
        """Get completed reads from the server

        :raises ConnectionError: When not connected to server
        :raises RuntimeError: When could not retrieve reads or an unexpected
            return code was received

        :return: List of dictionaries, where each sub-list contains all splits of the original read and each dict is a called split read
        :rtype: list[list[dict]]

        .. Note::
        Any reads which were too short to be basecalled (less than 100 samples) will have empty sequences and qstrings.
        """
        """Wrapper for get_completed_reads"""
        current_status = self.get_status()
        if current_status != self.connected:
            raise ConnectionError(
                "Not connected to server. status code: {!r}. {!r}".format(
                    current_status, super()
                )
            )

        results = super().get_completed_reads()
        return results

    def set_params(self, params: dict):
        for key, value in params.items():
            return_code = super().set_params({key: value})
            if return_code != self.success:
                if return_code == self.already_connected:
                    raise RuntimeError(
                        "Attempting to set connection parameters while connected is not supported. Please set parameters before connecting."
                    )
                elif return_code == self.failed:
                    raise ValueError(
                        "Could not set server parameter {!r} using value {!r}".format(
                            key,
                            value,
                        )
                    )
                else:
                    raise RuntimeError("Unexpected response from basecall server")

    def __enter__(self):
        """Make a connection to the server.

        This could be slow on the first connection due to loading the alignment
        index
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection to the server."""
        self.disconnect()
