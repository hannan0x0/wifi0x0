#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tool Name : WiFi0x0
Author    : Bunny0x0
Version   : 3.0
Mode      : Framework / Safe
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime
from pathlib import Path
import collections

# ============================
# GLOBAL CONFIG
# ============================

TOOL_NAME = "WiFi0x0"
VERSION = "3.0"

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / "logs"
SESSION_DIR = BASE_DIR / "sessions"

LOG_DIR.mkdir(exist_ok=True)
SESSION_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "wifi0x0.log"

# ============================
# LOGGING
# ============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# ============================
# UTILS
# ============================

def banner():
    print(f"""
╔══════════════════════════════╗
║         WiFi0x0 Tool         ║
║     Version : {VERSION:<10}   ║
║     Author  : Bunny0x0       ║
╚══════════════════════════════╝
""")

def slow(text, t=0.002):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(t)
    print()

# ============================
# STATUS CLASS
# ============================

class Status:
    def __init__(self):
        self.start = datetime.now()
        self.counter = 0

    def tick(self):
        self.counter += 1

# ============================
# CORE ENGINE
# ============================

class WiFi0x0:
    def __init__(self, interface, debug=False):
        self.interface = interface
        self.debug = debug
        self.status = Status()

        logging.info("Tool started")
        logging.info(f"Interface: {interface}")

    def start(self):
        banner()
        print(f"[+] Interface : {self.interface}")
        print(f"[+] Mode      : SAFE")
        print(f"[+] Log File  : {LOG_FILE}")
        print()

        self.menu()

    # ============================
    # MENU
    # ============================

    def menu(self):
        while True:
            print("""
[1] Show Status
[2] Show Session Info
[3] Dummy Scan (safe)
[4] Clear Screen
[0] Exit
""")
            choice = input("WiFi0x0 > ").strip()

            if choice == "1":
                self.show_status()
            elif choice == "2":
                self.session_info()
            elif choice == "3":
                self.fake_scan()
            elif choice == "4":
                os.system("clear")
            elif choice == "0":
                print("[+] Exiting...")
                break
            else:
                print("[!] Invalid option")

    # ============================
    # FEATURES
    # ============================

    def show_status(self):
        print("\n[STATUS]")
        print(f"Started : {self.status.start}")
        print(f"Actions : {self.status.counter}")
        print()

    def session_info(self):
        print("\n[SESSION INFO]")
        print(f"Session Dir : {SESSION_DIR}")
        print(f"Log File    : {LOG_FILE}")
        print()

    def fake_scan(self):
        print("\n[SCAN] Simulating scan...")
        for i in range(1, 6):
            print(f"[*] Scanning channel {i}...")
            time.sleep(0.6)
        print("[✓] Scan complete (safe mode)")
        self.status.tick()


# ============================
# ARGUMENT PARSER
# ============================

def parse_args():
    parser = argparse.ArgumentParser(description="WiFi0x0 Framework")
    parser.add_argument("-i", "--interface", default="wlan0", help="Wireless interface")
    parser.add_argument("--debug", action="store_true", help="Debug mode")
    return parser.parse_args()


# ============================
# ENTRY POINT
# ============================

if __name__ == "__main__":
    args = parse_args()
    app = WiFi0x0(interface=args.interface, debug=args.debug)
    app.start()
