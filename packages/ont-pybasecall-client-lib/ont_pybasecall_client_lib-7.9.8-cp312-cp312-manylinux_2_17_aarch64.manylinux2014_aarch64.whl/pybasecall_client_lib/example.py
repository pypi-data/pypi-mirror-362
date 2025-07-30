ont_core_path = "<ont_core dirpath>"
port_path = "<port uri>"
log_path = "<basecall_server_log dirpath>"
input_path = "<input dirpath>"
align_ref = "<align_ref filepath>"
bed_file = "<bed_file filepath>"

# Interface
# ---------

# ``ont-pybasecall-client-lib`` comprises three Python modules:

# **helper_functions** A set of functions for running a Dorado basecall server and
# loading reads from fast5 and/or pod5 files.
# **client_lib** A compiled library which provides direct Python bindings to Dorado's
# C++ BasecallClient API.
# **pyclient** A user-friendly wrapper around **client_lib**. This is what you
# should use to interact with a Dorado basecall server.
from pybasecall_client_lib import helper_functions

# Documentation and help
# ----------------------
# Information on the methods available may be viewed through Python's help command:
# e.g.
# help(pyclient)
# help(client_lib)


# Starting a basecall server
# --------------------------
# There must be a Dorado basecall server running in order to communicate with it.
# On most Oxford Nanopore devices a basecall server is always running on port 5555.
# On other devices, or if you want to run a separate basecall server, you must start
# one yourself:

# A basecall server requires:
#  * A location to put log files (on your PC)
#  * An initial config file to load
#  * A port to run on
server_args = [
    "--log_path",
    log_path,
    "--config",
    "dna_r9.4.1_450bps_fast.cfg",
    "--port",
    port_path,
]
# The second argument is the directory where the dorado_basecall_server executable
# is found. Update this as  appropriate.
helper_functions.run_server(server_args, ont_core_path + "/bin")


# Basecall and align using PyBasecallClient
# --------------------------------------

print("Starting PyBasecallClient...")
from pybasecall_client_lib.pyclient import PyBasecallClient

client = PyBasecallClient(
    port_path, "dna_r9.4.1_450bps_fast", align_ref=align_ref, bed_file=bed_file
)
client.connect()
print(client)

# Using the client generated in the previous example
print("Basecalling...")
called_reads = helper_functions.basecall_with_pybasecall_client(client, input_path)

for read in called_reads:
    read_id = read["metadata"]["read_id"]
    alignment_genome = read["metadata"]["alignment_genome"]
    sequence = read["datasets"]["sequence"]
    print(
        f"{read_id} sequence length is {len(sequence)}"
        f" alignment_genome is {alignment_genome}"
    )


# Basecall and get states, moves and modbases using BasecallClient
# -------------------------------------------------------------
# In order to retrieve the ``movement`` dataset, the ``move_enabled``
# option must be set to ``True``.
# NOTE: You shouldn't turn on ``move_enabled`` if you don't need it,
# because it generates a LOT of extra output data so it can hurt performance.

print("Starting BasecallClient...")
from pybasecall_client_lib.pyclient import PyBasecallClient

options = {
    "priority": PyBasecallClient.high_priority,
    "client_name": "test_client",
    "move_enabled": True,
}

# Note that we start the client with a dorado model set here rather than a config file name
client = PyBasecallClient(
    port_path,
    "dna_r10.4.1_e8.2_400bps_hac@v5.0.0|dna_r10.4.1_e8.2_400bps_hac@v5.0.0_5mC_5hmC@v2|",
)
result = client.set_params(options)
result = client.connect()
print(client)

print("Basecalling...")
called_reads = helper_functions.basecall_with_pybasecall_client(client, input_path)

for read in called_reads:
    base_mod_context = read["metadata"]["base_mod_context"]
    base_mod_alphabet = read["metadata"]["base_mod_alphabet"]
    read_id = read["metadata"]["read_id"]

    sequence = read["datasets"]["sequence"]
    movement = read["datasets"]["movement"]
    base_mod_probs = read["datasets"]["base_mod_probs"]

    print(
        f"{read_id} sequence length is {len(sequence)}, "
        f"base_mod_context is {base_mod_context}, base_mod_alphabet is {base_mod_alphabet}, "
        f"movement size is {movement.shape}, base_mod_probs size is {base_mod_probs.shape}"
    )

# Basecall with raw data and assigning mandatory metadata fields
# -------------------------------------------------------------
import numpy as np
from pybasecall_client_lib.client_lib import BasecallClient
from pybasecall_client_lib.pyclient import PyBasecallClient

print("Starting PyBasecallClient...")
client = PyBasecallClient(port_path, "dna_r10.4.1_e8.2_400bps_5khz_fast")
client.connect()
print(client)

rawdata = np.random.randint(low=-32768, high=32767, size=100, dtype="<i2")

read = helper_functions.package_read(
    read_id="test_read_id",
    raw_data=rawdata,
    daq_offset=1.5,
    daq_scaling=2.5,
    sampling_rate=5000.0,
    start_time=940291626,
)

print("Basecalling ...")
result = BasecallClient.pass_read(client, read)
BasecallClient.finish(client)
completed_reads = BasecallClient.get_completed_reads(client)

completed_read = completed_reads[0][0]
read_id = completed_read["metadata"]["read_id"]
sequence = completed_read["datasets"]["sequence"]
print(f"{read_id} sequence length is {len(sequence)}")


# Duplex Basecalling
# ------------------
import os

from pod5 import Reader as Pod5Reader
from pybasecall_client_lib import helper_functions
from pybasecall_client_lib.client_lib import BasecallClient

duplex_input_path = "<input folder for duplex basecalling>"

print("Starting PyBasecallClient...")
client = PyBasecallClient(port_path, "dna_r10.4.1_e8.2_400bps_duplex_hac.cfg")
options = {
    "client_name": "duplex_test_client",
    "pair_by_channel": True,
}
client.set_params(options)
client.connect()
print(client)

pod5_files = [
    os.path.join(duplex_input_path, f)
    for f in os.listdir(duplex_input_path)
    if f.endswith(".pod5")
]

from collections import defaultdict

reads_by_channel = defaultdict(list)
next_tag = 0
for filename in pod5_files:
    with Pod5Reader(filename) as reader:
        for record in reader.reads():
            read = helper_functions.pull_read(record)
            read["read_tag"] = next_tag
            next_tag += 1
            reads_by_channel[record.pore.channel].append(read)

print("Basecalling...")
for channel_reads in reads_by_channel.values():
    for read in channel_reads:
        result = BasecallClient.pass_read(client, read)
        if result != BasecallClient.read_accepted:
            raise Exception(
                "Attempt to pass read to server failed. Return value is {}.".format(
                    result
                )
            )

result = BasecallClient.finish(client, 3600)
if BasecallClient.success != result:
    raise Exception(
        "Call to finish() method did not complete quickly enough. Return value is {}.".format(
            result
        )
    )

(
    called_reads,
    called_ids,
    num_reads_split,
) = helper_functions.get_called_reads_from_pybasecall_client(client)

for read in called_reads:
    read_id = read["metadata"]["read_id"]
    strand_id = read["metadata"]["strand_id"]
    strand_1 = "NA"
    strand_2 = "NA"
    read_tag = read["read_tag"]
    sub_tag = read["sub_tag"]
    if "duplex_strand_1" in read["metadata"]:
        strand_1 = read["metadata"]["duplex_strand_1"]
    if "duplex_strand_2" in read["metadata"]:
        strand_2 = read["metadata"]["duplex_strand_2"]
    sequence_length = read["metadata"]["sequence_length"]
    print(
        "read_id : {}\ttag: {}-{}\tlen: {}\tstrand_id: {}\tstrand1: {}\tstrand2: {}".format(
            read_id, read_tag, sub_tag, sequence_length, strand_id, strand_1, strand_2
        )
    )
