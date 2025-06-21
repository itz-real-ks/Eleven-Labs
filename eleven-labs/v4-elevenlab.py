import os
import json
import re
import base64
import requests

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
        print(f"ERROR: {SCRIPT_FILE} not found.")
        exit(1)

    raw = open(SCRIPT_FILE, encoding="utf-8").read().strip()
    if not raw:
        print(f"ERROR: {SCRIPT_FILE} is empty.")
        exit(1)

    # Try JSON first
    try:
        data = json.loads(raw)
        if isinstance(data, dict) and "inputs" in data and isinstance(data["inputs"], list):
            print("[+] Detected valid JSON payload in script.txt")
            return data
        else:
            print("[!] JSON found but missing 'inputs' list; falling back to line parser.")
    except json.JSONDecodeError:
        print("[+] script.txt is not JSON—treating as line-based script.")

    # Line-based parsing: "Key | text"
    inputs = []
    for idx, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "|" not in line:
            print(f"ERROR: line {idx} missing '|': {line}")
            exit(1)
        key, text = map(str.strip, line.split("|", 1))
        if key not in VOICE_MAP:
            print(f"ERROR: Unknown voice key '{key}' on line {idx}")
            exit(1)
        inputs.append({"text": text, "voice_id": VOICE_MAP[key]})

    if not inputs:
        print("ERROR: No valid lines found in script.txt.")
        exit(1)

    print(f"[+] Built payload from {len(inputs)} lines.")
    return {"inputs": inputs}


def fetch_response(payload: dict) -> requests.Response:
    """ POST payload and return Response (or exit on error). """
    print(f"[+] Sending payload with {len(payload['inputs'])} entries…")
    resp = requests.post(ENDPOINT, headers=HEADERS, json=payload, timeout=60)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        print("HTTP error:", e)
        print("Body preview:", resp.text[:300])
        exit(1)
    return resp


def decode_and_save(resp: requests.Response):
    """ Detect raw/hex/base64 response, decode, and write OUTPUT_FILE. """
    ctype = resp.headers.get("Content-Type", "")
    cenc  = resp.headers.get("Content-Encoding", "")
    raw_bytes = None

    # 1) raw audio
    if "audio/" in ctype or "gzip" in cenc:
        print("[+] Detected raw/binary audio.")
        raw_bytes = resp.content
    else:
        txt = resp.text.strip()
        # 2) hex
        if re.fullmatch(r"[0-9A-Fa-f]+", txt) and len(txt) % 2 == 0:
            print("[+] Detected hex-encoded audio.")
            raw_bytes = bytes.fromhex(txt)
        # 3) base64
        elif re.fullmatch(r"[A-Za-z0-9+/=\s]+", txt):
            print("[+] Detected Base64-encoded audio.")
            b64 = re.sub(r"\s+", "", txt)
            try:
                raw_bytes = base64.b64decode(b64, validate=True)
            except Exception as e:
                print("ERROR: base64 decode failed:", e)
                exit(1)
        else:
            print("ERROR: Unknown response format.")
            print("Content-Type:", ctype)
            print("Body preview:", txt[:200])
            exit(1)

    with open(OUTPUT_FILE, "wb") as f:
        f.write(raw_bytes)
    print(f"[+] Audio written to {OUTPUT_FILE}")


def main():
    payload = load_or_build_payload()
    resp = fetch_response(payload)
    decode_and_save(resp)


if __name__ == "__main__":
    main()
