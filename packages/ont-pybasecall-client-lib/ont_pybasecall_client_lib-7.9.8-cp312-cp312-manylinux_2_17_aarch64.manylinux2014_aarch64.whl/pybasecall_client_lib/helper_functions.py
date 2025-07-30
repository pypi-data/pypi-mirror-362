#! /usr/bin/env python3

import json
import os
import subprocess
import time
import warnings

import numpy

DEBUG = os.getenv("BUILD_TYPE", "Release").upper() == "DEBUG"

if DEBUG:
    from pybasecall_client_lib.client_libd import BasecallClient
else:
    from pybasecall_client_lib.client_lib import BasecallClient

FAST5_UNAVAILABLE = False
try:
    from ont_fast5_api.fast5_interface import get_fast5_file
    from ont_fast5_api.fast5_read import Fast5Read
except Exception:
    FAST5_UNAVAILABLE = True

POD5_UNAVAILABLE = False
try:
    from pod5 import Reader as Pod5Reader
    from pod5 import ReadRecord as Pod5Read
except Exception:
    POD5_UNAVAILABLE = True


def _cycle():
    # Counter that cycles [0, 2**32)
    while True:
        yield from range(0, int(2**32), 1)


_COUNT = _cycle()
FINISH_TIMEOUT = 3600

warnings.filterwarnings("default", category=DeprecationWarning, module=__name__)


def _check_fast5_or_pod5_api():
    if FAST5_UNAVAILABLE and POD5_UNAVAILABLE:
        raise RuntimeError(
            "at least one of ont_fast5_api or pod5 modules must be installed to use this function"
        )


def pull_read(read):
    _check_fast5_or_pod5_api()
    input_read = None
    if not FAST5_UNAVAILABLE:
        if isinstance(read, Fast5Read):
            input_read = read
        else:
            try:
                if read.endswith(".fast5"):
                    warnings.warn(
                        "pull_read() will no longer support pathnames soon.",
                        DeprecationWarning,
                    )
                    with get_fast5_file(read, mode="r") as f5:
                        input_read = f5.get_read(f5.get_read_ids()[0])
            except Exception:
                pass
    if input_read:
        raw_data = input_read.get_raw_data()
        read_id = input_read.read_id
        run_id = input_read.run_id.decode("UTF-8")
        raw_attrs = input_read.handle[input_read.raw_dataset_group_name].attrs
        mux = int(raw_attrs["start_mux"])
        start_time = int(raw_attrs["start_time"])
        duration = int(raw_attrs["duration"])
        channel_info = input_read.get_channel_info()
        channel = int(channel_info["channel_number"])
        daq_offset = channel_info["offset"]
        daq_scaling = channel_info["range"] / channel_info["digitisation"]
        sampling_rate = channel_info["sampling_rate"]
        sequencing_kit = "unknown"
        end_reason = "unknown"
    elif not POD5_UNAVAILABLE:
        if isinstance(read, Pod5Read):
            input_read = read
        else:
            try:
                if read.endswith(".pod5"):
                    warnings.warn(
                        "pull_read() will no longer support pathnames soon.",
                        DeprecationWarning,
                    )
                    with Pod5Reader(read) as reader:
                        input_read = next(reader.reads())
            except Exception:
                pass
        if input_read:
            raw_data = input_read.signal
            read_id = str(input_read.read_id)
            start_time = input_read.start_sample
            duration = input_read.num_samples
            channel = input_read.pore.channel
            mux = input_read.pore.well
            daq_offset = input_read.calibration.offset
            daq_scaling = input_read.calibration.scale
            sampling_rate = float(input_read.run_info.sample_rate)
            run_id = input_read.run_info.acquisition_id
            sequencing_kit = input_read.run_info.sequencing_kit
            end_reason = input_read.end_reason.name.lower()
    if not input_read:
        raise RuntimeError("Unsupported read type.")

    return {
        "raw_data": raw_data,
        "read_id": read_id,
        "run_id": run_id,
        "channel": channel,
        "mux": mux,
        "start_time": start_time,
        "duration": duration,
        "daq_offset": daq_offset,
        "daq_scaling": daq_scaling,
        "sampling_rate": sampling_rate,
        "sequencing_kit": sequencing_kit,
        "end_reason": end_reason,
    }


def _get_all_read_ids(fast5_files, pod5_files):
    read_ids = []
    for filename in fast5_files:
        with get_fast5_file(filename, mode="r") as f5:
            read_ids += f5.get_read_ids()
    for filename in pod5_files:
        with Pod5Reader(filename) as reader:
            read_ids += [record.read_id for record in reader.reads()]
    return read_ids


def _read_generator(fast5_files, pod5_files):
    for filename in fast5_files:
        with get_fast5_file(filename, mode="r") as f5:
            for read_id in f5.get_read_ids():
                yield f5.get_read(read_id)
    for filename in pod5_files:
        with Pod5Reader(filename) as reader:
            for record in reader.reads():
                yield record


def _get_reads(generator, count, next_tag):
    n = 0
    reads = []
    while n < count:
        next_read = next(generator)
        read = pull_read(next_read)
        read["read_tag"] = next_tag + n
        reads.append(read)
        n += 1
    return reads


def send_reads_with_pybasecall_client(
    client, input_path, batch_size=1, fast5=True, pod5=True
):
    if fast5:
        fast5_files = [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.endswith(".fast5")
        ]
    else:
        fast5 = []
    if pod5:
        pod5_files = [
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.endswith(".pod5")
        ]
    else:
        pod5_files = []

    if fast5_files and FAST5_UNAVAILABLE:
        warnings.warn(
            "Skipping fast5 input since `ont_fast5_api` module is not installed."
        )
        fast5_files = []
    if pod5_files and POD5_UNAVAILABLE:
        warnings.warn("Skipping pod5 input since `pod5` module is not installed.")
        pod5_files = []

    all_reads = _get_all_read_ids(fast5_files, pod5_files)
    read_count = len(all_reads)
    generator = _read_generator(fast5_files, pod5_files)
    num_reads_sent = 0
    called_reads = []
    called_ids = []
    num_reads_split = 0
    while num_reads_sent < read_count:
        num = batch_size
        if num + num_reads_sent > read_count:
            num = read_count - num_reads_sent
        reads = _get_reads(generator, num, num_reads_sent)
        if len(reads) == 1:
            result = BasecallClient.pass_read(client, reads[0])
        else:
            result = BasecallClient.pass_reads(client, reads)
        while result == BasecallClient.queue_full:
            time.sleep(0.05)
            if len(reads) == 1:
                result = BasecallClient.pass_read(client, reads[0])
            else:
                result = BasecallClient.pass_reads(client, reads)
        if result == BasecallClient.read_accepted:
            num_reads_sent += len(reads)
        else:
            raise Exception(
                "Attempt to pass read to server failed. Return value is {}.".format(
                    result
                )
            )
        (
            new_called_reads,
            new_called_ids,
            new_num_reads_split,
        ) = get_called_reads_from_pybasecall_client(client)
        called_reads.extend(new_called_reads)
        called_ids.extend(new_called_ids)
        num_reads_split += new_num_reads_split
    return called_reads, called_ids, all_reads, num_reads_split


def get_called_reads_from_pybasecall_client(client):
    called_ids = []
    called_reads = []
    num_reads_split = 0
    completed_reads = BasecallClient.get_completed_reads(client)
    for split_read in completed_reads:
        for read in split_read:
            called_ids.append((read["read_tag"], read["sub_tag"]))
            called_reads.append(read)
            if read["sub_tag"] != 0:
                num_reads_split += 1
    return called_reads, called_ids, num_reads_split


def basecall_with_pybasecall_client(client, input_path, save_file=None, batch_size=1):
    _check_fast5_or_pod5_api()
    if save_file is not None:
        out = open(save_file, "w")
        out.write("read_id\tsequence_length\tparent_read_id\tstrand_1\tstrand_2\n")
    else:
        out = None

    try:
        (
            called_reads,
            called_ids,
            all_reads,
            num_reads_split,
        ) = send_reads_with_pybasecall_client(client, input_path, batch_size)
        read_count = len(all_reads)
        num_reads_called = len(called_reads)

        result = BasecallClient.finish(client, FINISH_TIMEOUT)
        if BasecallClient.success != result:
            raise Exception(
                "Call to finish() method did not complete quickly enough. Return value is {}.".format(
                    result
                )
            )

        more_reads, more_ids, more_split = get_called_reads_from_pybasecall_client(
            client
        )
        num_reads_called += len(more_reads)
        num_reads_split += more_split
        called_reads.extend(more_reads)
        called_ids.extend(more_ids)
        if out is not None:
            for read in called_reads:
                read_id = read["metadata"]["strand_id"]
                parent_read_id = read["metadata"]["read_id"]
                strand_1 = "NA"
                strand_2 = "NA"
                if "duplex_strand_1" in read["metadata"]:
                    strand_1 = read["metadata"]["duplex_strand_1"]
                if "duplex_strand_2" in read["metadata"]:
                    strand_2 = read["metadata"]["duplex_strand_2"]
                sequence_length = read["metadata"]["sequence_length"]
                out.write(
                    "{}\t{}\t{}\t{}\t{}\n".format(
                        read_id, sequence_length, parent_read_id, strand_1, strand_2
                    )
                )
    finally:
        if out is not None:
            out.close()
    unique_ids = set(called_ids)
    assert read_count + num_reads_split == num_reads_called
    assert read_count + num_reads_split == len(unique_ids)
    return called_reads


def run_server(options, bin_path=None):
    """
    Start a basecall server with the specified parameters.
    :param options: List of command line options for the server.
    :param bin_path: Optional path to basecall server binary executable.
    :return: A tuple containing the handle to the server process, and the port the server is listening on.

    If the server cannot be started, the port will be returned as 'ERROR'.
    Use the 'auto' option for the port to have the server automatically select an available port.
    """
    executable = "dorado_basecall_server"
    if DEBUG:
        executable = executable + "d"
    if bin_path is not None:
        executable = os.path.join(bin_path, executable)
    server_args = [executable]
    server_args.extend(options)

    print("Server command line: ", " ".join(server_args))
    server = subprocess.Popen(server_args, stdout=subprocess.PIPE)
    for line in iter(server.stdout.readline, ""):
        message_to_find = b"Starting server on port: "
        if message_to_find in line:  # This will be true when the server has started up.
            port_string = line[len(message_to_find) :].decode("ascii").strip()
            break
        if len(line) == 0:  # If something goes wrong, this prevents an endless loop.
            server.kill()
            raise RuntimeError("Failed to read line from server")
    print("Server started on port: {}".format(port_string))
    return server, port_string


def package_read(
    read_id: str,
    raw_data: "numpy.ndarray[numpy.int16]",
    daq_offset: float,
    daq_scaling: float,
    read_tag: int = None,
    **kwargs,
) -> dict:
    """Package a read for pybasecall_client_lib

    :param read_id: Read ID for the read, doesn't need to be unique but must
        not be empty
    :type read_id: str
    :param raw_data: 1d numpy array of signed 16 bit integers
    :type raw_data: numpy.ndarray[numpy.int16]
    :param daq_offset: Offset for pA conversion
    :type daq_offset: float
    :param daq_scaling: Scale factor for pA conversion
    :type daq_scaling: float
    :param read_tag: 32 bit positive integer, must be unique to each read. If
        ``None`` will be assigned a value from the pybasecall_client global counter
    :type read_tag: int

    :returns: read data packaged for pybasecall_client
    :rtype: dict
    """
    if read_tag is None:
        read_tag = next(_COUNT)
    read = {
        "read_tag": read_tag,
        "read_id": read_id,
        "raw_data": raw_data,
        "daq_offset": daq_offset,
        "daq_scaling": daq_scaling,
    }
    read.update(kwargs)
    return read


def get_barcode_kits(address: str, timeout: int) -> list:
    """Get available barcode kits from server

    :param address: dorado_basecall_server address eg: 127.0.0.1:5555
    :type address: str
    :param timeout: Timeout in milliseconds
    :type timeout: int

    :raises RuntimeError: if failed to retrieve barcode kits from server.

    :returns: List of barcode kits supported by the server
    :rtype: list
    """
    result, status = BasecallClient.get_barcode_kits(address, timeout)
    if status != BasecallClient.success:
        raise RuntimeError("Could not get barcode kits")
    return result


def get_server_stats(address: str, timeout: int) -> dict:
    """Get statistics from server

    :param address: dorado_basecall_server address eg: 127.0.0.1:5555
    :type address: str
    :param timeout: Timeout in milliseconds
    :type timeout: int

    :raises RuntimeError: if failed to retrieve statistics from server

    :returns: Dictionary of server stats
    :rtype: dict
    """
    result, status = BasecallClient.get_server_stats(address, timeout)
    if status != BasecallClient.success:
        raise RuntimeError("Could not get server stats")
    return result


def get_server_information(address: str, timeout: int) -> dict:
    """Get server information

    :param address: dorado_basecall_server address eg: 127.0.0.1:5555
    :type address: str
    :param timeout: Timeout in milliseconds
    :type timeout: int

    :raises RuntimeError: if failed to retrieve information from server

    :returns: Dictionary of server information
    :rtype: dict
    """
    result_str, status = BasecallClient.get_server_information(address, timeout)
    if status == BasecallClient.timed_out:
        raise RuntimeError("Request for server information timed out")
    if status != BasecallClient.success:
        raise RuntimeError(
            "An error occurred attempting to retrieve server information"
        )
    result_dict = json.loads(result_str)
    return result_dict


def get_return_code_message(return_code):
    """This function provides string messages for each of the return code types that queries to the
    server may make.

    :param return_code: The return code from the query to the server.
    :return: A tuple with two entries. The first is the exception type that should be raised if
             raising an exception is appropriate for the call. The second is the string message
             that should be passed to the exception.

    Note that for return codes for which raising an exception would never be appropriate, the first
    value is returned as None. If the second value is also returned as None, then this means that
    the return code has not been included in this function. This should be considered to be a bug.

    This function is used to handle the wide range of return codes that can come back from a
    connection attempt, and may be used in the future to handle return codes from other methods.
    However, it's primary purpose is to support unit testing, and specifically to help with making
    sure that no new return codes have been added to the library without also updating the pyclient
    wrapper code to properly handle it.
    """
    if return_code == BasecallClient.success:
        return None, "Success"
    elif return_code == BasecallClient.not_ready:
        return None, "Server not ready"
    elif return_code == BasecallClient.no_connection:
        return ConnectionError, "No connection: {!r}".format(return_code)
    elif return_code == BasecallClient.already_connected:
        return ConnectionError, "Client is already connected: {!r}".format(return_code)
    elif return_code == BasecallClient.timed_out:
        return ConnectionError, "Query timed out: {!r}".format(return_code)
    elif return_code == BasecallClient.invalid_response:
        return ConnectionError, "Received invalid response: {!r}".format(return_code)
    elif return_code == BasecallClient.basecall_config_unavailable:
        return ValueError, "Basecalling config unavailable: {!r}".format(return_code)
    elif return_code == BasecallClient.barcode_kit_unavailable:
        return ValueError, "Barcode kit unavailable: {!r}".format(return_code)
    elif return_code == BasecallClient.align_index_unavailable:
        return ValueError, "Alignment index file unavailable: {!r}".format(return_code)
    elif return_code == BasecallClient.bed_file_unavailable:
        return ValueError, "Alignment bed file unavailable: {!r}".format(return_code)
    elif return_code == BasecallClient.file_load_timeout:
        return RuntimeError, "Timeout during file load: {!r}".format(return_code)
    elif return_code == BasecallClient.failed:
        return RuntimeError, "Query failed: {!r}".format(return_code)
    elif return_code == BasecallClient.bad_request:
        return ValueError, "Query not recognized by server: {!r}".format(return_code)
    elif return_code == BasecallClient.bad_reply:
        return RuntimeError, "Server response not formatted correctly: {!r}".format(
            return_code
        )
    elif return_code == BasecallClient.invalid_aligner_options:
        return ValueError, "Invalid aligner options : {!r}".format(return_code)
    else:
        return None, None
