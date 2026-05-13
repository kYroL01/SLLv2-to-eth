# MIT License

# Copyright (c) 2024-2025 Michele Campus (michelecampus5@gmail.com)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import signal
from scapy.all import *

running = True

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Convert SLL2 PCAP to Ethernet PCAP with custom MAC addresses.")
parser.add_argument("input_file", help="Path to the input PCAP file (SLL2 format)")
parser.add_argument("output_file", help="Path to the output PCAP file (Ethernet format)")
parser.add_argument("--src-mac", default="aa:bb:cc:dd:ee:ff", help="Source MAC address (default: aa:bb:cc:dd:ee:ff)")
parser.add_argument("--dst-mac", default="ff:ee:dd:cc:bb:aa", help="Destination MAC address (default: ff:ee:dd:cc:bb:aa)")
parser.add_argument("--progress", action="store_true", help="Show conversion progress in 10% steps")

args = parser.parse_args()

# Set up signal handler for graceful interruption
def handle_sigint(sig, frame):
    global running
    running = False

signal.signal(signal.SIGINT, handle_sigint)

# Count packets first so we can report conversion progress in 10% steps.
total_packets = 0
next_progress = 10
if args.progress:
    with PcapReader(args.input_file) as pcap_reader:
        total_packets = sum(1 for _ in pcap_reader)
        if total_packets == 0:
            print("Input file has no packets. Nothing to convert.")
            raise SystemExit(0)

# Read packets from the input SLL2 PCAP file
processed = 0
with PcapReader(args.input_file) as pcap_reader, PcapWriter(args.output_file, append=False, sync=True) as pcap_writer:
    for pkt in pcap_reader:
        if not running:
            break

        if pkt.haslayer("Raw") or pkt.haslayer("CookedLinuxV2"):
            # Create a new Ethernet frame with specified MACs and original packet payload
            eth_pkt = Ether(src=args.src_mac, dst=args.dst_mac) / pkt.payload
            eth_pkt.time = pkt.time  # Keep the original timestamp
            pcap_writer.write(eth_pkt)

        processed += 1
        if args.progress and processed >= (next_progress * total_packets) // 100:
            print(f"Progress: {next_progress}% ({processed}/{total_packets})")
            next_progress += 10

print(f"Converted {processed} packets to Ethernet format and saved as {args.output_file}")
