import argparse
import json
import base64
import sys
from pathlib import Path
import cloudscraper
from requests.exceptions import HTTPError, RequestException
import chardet
from tqdm import tqdm
from colorama import init, Fore, Style
import tempfile
import os
import webbrowser
import io
import pydub

free_working_models = ["eleven_turbo_v2_5","eleven_turbo_v2","eleven_flash_v2","eleven_v3"]

init(autoreset=True)

# ----- CONFIGURATION -----
VOICES = {
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
    "Charlotte": "XB0fDUnXU5powFXDhCwa",
    "Alice":   "Xb7hH8MSUJpSbSDYk0k2",
    "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "Will":    "bIHbv24MWmeRgasZH58o",
    "Brian":   "nPczCjzI2devNBz1zQrb",
    "Daniel":  "onwK4e9ZLuTAKqWW03F9",
    "Lily":    "pFZP5JQG7iQjIQuC4Bku",
    "Bill":    "pqHfZKP75CvOlQylNhV4",
    "Eric":    "cjVigY5qzO86Huf0OWal",
}

BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream/with-timestamps?allow_unauthenticated=1"
HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://elevenlabs.io",
    "Referer": "https://elevenlabs.io/",
    "DNT": "1",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
}

# ----- ARGUMENTS -----
parser = argparse.ArgumentParser(description='Text-to-Speech Converter')
parser.add_argument('-s', '--script', help='Script file', default='script.txt')
parser.add_argument('-o', '--output', help='Output file')
parser.add_argument('-f', '--format', help='Output format (mp3 or wav)', default='mp3')
parser.add_argument('-sf', '--subtitle_format', help='Subtitle format (srt, txt, or json)', default='srt')
parser.add_argument('--speed', type=float, default=1.0, help='Speech speed (e.g., 0.5 for slow, 2.0 for fast)')
parser.add_argument('--model', choices=['eleven_monolingual_v1', 'eleven_multilingual_v1', 'eleven_v3'], default='eleven_v3', help='Voice model version')
parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
parser.add_argument('--stream', action='store_true', help='Stream audio without saving')
args = parser.parse_args()

def choose_voice():
    if args.interactive:
        print("Available narrators:")
        for name in sorted(VOICES):
            print(f"  • {name}")
        while True:
            choice = input("\nEnter narrator name or voice_id: ").strip()
            if choice in VOICES:
                return VOICES[choice]
            if choice in VOICES.values():
                return choice
            print(f"'{choice}' is not valid. Try again.")
    else:
        return list(VOICES.values())[0]  # default

def get_text_from_file(path: Path):
    with open(path, 'rb') as f:
        encoding = chardet.detect(f.read())['encoding'] or 'utf-8'
    with open(path, 'r', encoding=encoding, errors='ignore') as f:
        return f.read().strip()

def stream_tts_to_mp3(voice_id: str, text: str):
    url = BASE_URL.format(voice_id=voice_id)
    payload = {
        "text": text,
        "model_id": args.model,
        "voice_settings": {"speed": args.speed},
    }

    scraper = cloudscraper.create_scraper()
    audio_data = bytearray()
    subtitles = []

    try:
        resp = scraper.post(url, headers=HEADERS, json=payload, stream=True, timeout=60)
        resp.raise_for_status()

        for idx, line in enumerate(resp.iter_lines(decode_unicode=True), 1):
            if not line:
                continue
            try:
                chunk = json.loads(line)
            except json.JSONDecodeError:
                continue

            if err := chunk.get("error"):
                print(f"[API ERROR @ chunk {idx}]: {err}")
                continue

            b64 = chunk.get("audio_base64")
            if b64:
                try:
                    audio_data.extend(base64.b64decode(b64))
                except Exception as exc:
                    print(f"[Base64 Error @ chunk {idx}]: {exc}")

            if all(k in chunk for k in ("start", "end", "text")):
                start = chunk['start'] / 1000
                end = chunk['end'] / 1000
                subtitles.append({
                    "start_time": f"{start:.3f}".replace('.', ','),
                    "end_time": f"{end:.3f}".replace('.', ','),
                    "text": chunk['text']
                })

    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    return audio_data, subtitles
