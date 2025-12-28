#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tool Name : WiFi0x0
Author    : Bunny0x0
Version   : 2.0
Mode      : Framework / Safe Base
"""

import os
import sys
import time
import argparse
import logging
from datetime import datetime
from pathlib import Path
import collections


# =========================
# GLOBAL CONFIG
# =========================

TOOL_NAME = "WiFi0x0"
VERSION = "2.0"

BASE_DIR = Path(__file__).parent
SESSION_DIR = BASE_DIR / "sessions"
LOG_DIR = BASE_DIR / "logs"

SESSION_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)


# =========================
# LOGGING
# =========================

LOG_FILE = LOG_DIR / "wifi0x0.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# =========================
# UTIL
# =========================

def banner():
    print(f"""
╔══════════════════════════════╗
║        WiFi0x0 Tool          ║
║   Version : {VERSION:<10}     ║
║   Author  : Bunny0x0         ║
╚══════════════════════════════╝
""")


def slow_print(text, delay=0.002):
    for c in text + "\n":
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)


# =========================
# CORE CLASSES
# =========================

class NetworkAddress:
    def __init__(self, mac):
        self.mac = mac.upper()

    def __str__(self):
        return self.mac


class Status:
    def __init__(self):
        self.start_time = datetime.now()
        self.counter = 0

    def update(self):
        self.counter += 1


# =========================
# MAIN ENGINE
# =========================

class WiFi0x0:
    def __init__(self, interface, debug=False):
        self.interface = interface
        self.debug = debug
        self.status = Status()

        logging.info("Tool started")
        logging.info(f"Interface: {self.interface}")

    def start(self):
        banner()
        print(f"[+] Interface : {self.interface}")
        print(f"[+] Mode      : SAFE")
        print("[+] Tool loaded successfully\n")

        if self.debug:
            print("[DEBUG] Debug mode enabled")

        self.run()

    def run(self):
        print("[*] Waiting for command...")
        time.sleep(1)
        print("[✓] Framework ready.")
        logging.info("Framework initialized")


# =========================
# ARGUMENT PARSER
# =========================

def parse_args():
    parser = argparse.ArgumentParser(
        description="WiFi0x0 Framework"
    )

    parser.add_argument(
        "-i", "--interface",
        help="Wireless interface (e.g wlan0)",
        default="wlan0"
    )

    parser.add_argument(
        "--debug",
        help="Enable debug mode",
        action="store_true"
    )

    return parser.parse_args()


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    args = parse_args()

    tool = WiFi0x0(
        interface=args.interface,
        debug=args.debug
    )

    tool.start()
