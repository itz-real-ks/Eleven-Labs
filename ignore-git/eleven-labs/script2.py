import os
import json
import re
import base64
import requests
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# ————— CONFIG —————
SCRIPT_FILE = "script.txt"
OUTPUT_FILE = "output.mp3"
ENDPOINT = "https://api.elevenlabs.io/v1/text-to-dialogue-anonymous"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    ),
    "Accept": "*/*",
    "Content-Type": "application/json",
    "DNT": "1",
    "Origin": "https://elevenlabs.io",
    "Referer": "https://elevenlabs.io/",
}

# Map your friendly keys to real ElevenLabs voice_id strings
VOICE_MAP = {
    "Sarah":   "EXAVITQu4vr4xnSDxMaL",
    "Laura":   "FGY2WhTYpPnrIDTdsKH5",
    "Jessica": "cgSgspJ2msm6clMCkdW9",
    "Liam":    "TX3LPaxmHKxFdv7VOQHJ",
    "Chris":   "iP95p4xoKVk53GoZ742B",
    "Aria":    "9BWtsMINqrJLrRacOk9x",
    "Charlie": "IKne3meq5aSn9XLyUdCD",
    "George":  "JBFqnCBsd6RMkjVDRZzb",
    "Callum":  "N2lVS1w4EtoT3dr4eOWO",
    "River":   "SAz9YHcvj6GT2YYXdXww",
    "Charlotte":"XB0fDUnXU5powFXDhCwa",
    "Alice":   "Xb7hH8MSUJpSbSDYk0k2",
    "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "Will":    "bIHbv24MWmeRgasZH58o",
    "Brian":   "nPczCjzI2devNBz1zQrb",
    "Daniel":  "onwK4e9ZLuTAKqWW03F9",
    "Lily":    "pFZP5JQG7iQjIQuC4Bku",
    "Bill":    "pqHfZKP75CvOlQylNhV4",
}


def load_or_build_payload() -> dict:
    """
    1) If script.txt contains valid JSON with an "inputs" list, load and return it.
    2) Else parse lines of "VoiceKey | text" and build {"inputs":[...]}.
    """
    if not os.path.isfile(SCRIPT_FILE):
        print(f"{Fore.RED}ERROR: {SCRIPT_FILE} not found.{Style.RESET_ALL}")
        exit(1)

    raw = open(SCRIPT_FILE, encoding="utf-8").read().strip()
    if not raw:
        print(f"{Fore.RED}ERROR: {SCRIPT_FILE} is empty.{Style.RESET_ALL}")
        exit(1)

    # Try JSON first
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "inputs" in data and isinstance(data["inputs"], list):
            print(f"{Fore.GREEN}[+] Detected valid JSON payload in script.txt{Style.RESET_ALL}")
            return data
        else:
            print(f"{Fore.YELLOW}[!] JSON found but missing 'inputs' list; falling back to line parser.{Style.RESET_ALL}")
    except json.JSONDecodeError:
        print(f"{Fore.GREEN}[+] script.txt is not JSON—treating as line-based script.{Style.RESET_ALL}")

    # Line-based parsing: "Key | text"
    inputs = []
    for idx, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            print(f"{Fore.RED}ERROR: line {idx} missing '|': {line}{Style.RESET_ALL}")
            exit(1)
        key, text = map(str.strip, line.split("|", 1))
        if key not in VOICE_MAP:
            print(f"{Fore.RED}ERROR: Unknown voice key '{key}' on line {idx}{Style.RESET_ALL}")
            exit(1)
        inputs.append({"text": text, "voice_id": VOICE_MAP[key]})

    if not inputs:
        print(f"{Fore.RED}ERROR: No valid lines found in script.txt.{Style.RESET_ALL}")
        exit(1)

    print(f"{Fore.GREEN}[+] Built payload from {len(inputs)} lines.{Style.RESET_ALL}")
    return {"inputs": inputs}

def fetch_response(payload: dict):
    """ POST payload and return Response (or exit on error). """
    print(f"{Fore.GREEN}[+] Sending payload with {len(payload['inputs'])} entries…{Style.RESET_ALL}")
    try:
        resp = requests.post(ENDPOINT, headers=HEADERS, json=payload, timeout=60, stream=True)
        resp.raise_for_status()
        total_size = int(resp.headers.get('content-length', 0))
        block_size = 1024
        bar_format = "{l_bar}{bar}| {percentage:.0f}%| {rate_fmt} | {remaining} left | {elapsed} elapsed"
        t = tqdm(total=total_size, unit='B', unit_scale=True, desc=f"{Fore.CYAN}Downloading{Style.RESET_ALL}", bar_format=bar_format, colour="#ff3737")
        raw_bytes = bytearray()
        for data in resp.iter_content(block_size):
            t.update(len(data))
            raw_bytes.extend(data)
        t.close()
        return raw_bytes
    except requests.HTTPError as e:
        print(f"{Fore.RED}HTTP error: {e}{Style.RESET_ALL}")
        print(f"{Fore.RED}Body preview: {resp.text[:300]}{Style.RESET_ALL}")
        exit(1)

def decode_and_save(raw_bytes):
    """ Detect raw/hex/base64 response, decode, and write OUTPUT_FILE. """
    try:
        with open(OUTPUT_FILE, "wb") as f:
            f.write(raw_bytes)
        print(f"{Fore.GREEN}[+] Audio written to {OUTPUT_FILE}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}ERROR: Failed to write audio file: {e}{Style.RESET_ALL}")
        exit(1)


def main():
    payload = load_or_build_payload()
    raw_bytes = fetch_response(payload)
    decode_and_save(raw_bytes)


if __name__ == "__main__":
    main()