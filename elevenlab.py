"""
eleven_tts_with_choice.py

Streams text-to-speech from ElevenLabs, allows you to pick a narrator,
bypassing Cloudflare, and writes the result to output.mp3.
"""

import json
import base64
import sys
from pathlib import Path
import cloudscraper
from requests.exceptions import HTTPError, RequestException
import chardet


# ----- CONFIGURATION -----

# Predefined voices (name -> voice_id)
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
    "Charlotte":"XB0fDUnXU5powFXDhCwa",
    "Alice":   "Xb7hH8MSUJpSbSDYk0k2",
    "Matilda": "XrExE9yKIg1WjnnlVkGX",
    "Will":    "bIHbv24MWmeRgasZH58o",
    "Brian":   "nPczCjzI2devNBz1zQrb",
    "Daniel":  "onwK4e9ZLuTAKqWW03F9",
    "Lily":    "pFZP5JQG7iQjIQuC4Bku",
    "Bill":    "pqHfZKP75CvOlQylNhV4",
}

BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream/with-timestamps?allow_unauthenticated=1"

HEADERS = {
    "Accept": "*/*", "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9", "Content-Type": "application/json",
    "Origin": "https://elevenlabs.io", "Referer": "https://elevenlabs.io/",
    "DNT": "1", "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
}

OUTPUT_FILE = Path("output.mp3")
WORD_LIMIT = 1000

def choose_voice() -> str:
    print("Available narrators:")
    for name in sorted(VOICES):
        print(f"  • {name}")
    while True:
        choice = input("\nEnter narrator name (or paste voice_id): ").strip()
        if choice in VOICES:
            return VOICES[choice]
        if choice in VOICES.values():
            return choice
        print(f"\nError: '{choice}' is not a valid narrator name or voice_id.")

def get_text_from_input() -> tuple:
    print("\nEnter the text you want to convert. Finish with an empty line:")
    lines = []
    word_count = 0
    while True:
        line = input()
        if not line:
            break
        words = line.split()
        word_count += len(words)
        if word_count > WORD_LIMIT * 0.9:  # break before reaching the limit
            text = "\n".join(lines)
            return text, True
        lines.append(line)
    text = "\n".join(lines).strip()
    if not text:
        return None, False
    return text, False

def get_text_from_file(path: Path) -> tuple:
    with open(path, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding is None:
            encoding = 'utf-8'  # default encoding
        try:
            with open(path, 'r', encoding=encoding, errors='ignore') as file:
                text = file.read()
                lines = text.splitlines()
                word_count = sum(len(line.split()) for line in lines)
                if word_count > WORD_LIMIT * 0.9:
                    print("\nWord limit reached. Breaking script into two parts.")
                    return text, True
                return text, False
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)

def get_text() -> str:
    print("How would you like to enter the text?")
    print("1. Type the text directly")
    print("2. Read from a file (specify path)")
    print("3. Read from 'script.txt' in the current directory")
    choice = input("Enter your choice (1/2/3): ")
    if choice == "1":
        text, limit_reached = get_text_from_input()
        if limit_reached:
            print("\nWord limit reached. Breaking script into two parts.")
        return text
    elif choice == "2":
        path = input("Enter the file path: ")
        text, limit_reached = get_text_from_file(Path(path))
        if limit_reached:
            print("\nWord limit reached. Breaking script into two parts.")
        return text
    elif choice == "3":
        text, limit_reached = get_text_from_file(Path("script.txt"))
        if limit_reached:
            print("\nWord limit reached. Breaking script into two parts.")
        return text
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

def get_remaining_text() -> str:
    print("\nEnter the remaining text you want to convert. Finish with an empty line:")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    text = "\n".join(lines).strip()
    if not text:
        print("No text entered—exiting.")
        sys.exit(0)
    return text

def stream_tts_to_mp3(voice_id: str, text: str, out_path: Path) -> None:
    """
    Streams TTS audio using the selected voice_id, decodes base64 chunks,
    concatenates them, and writes out as a single MP3 file.
    """
    url = BASE_URL.format(voice_id=voice_id)
    payload = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": {"speed": 1},
    }

    scraper = cloudscraper.create_scraper()
    audio_data = bytearray()

    try:
        print(f"\n→ Sending request to ElevenLabs (voice_id={voice_id})…")
        resp = scraper.post(url, headers=HEADERS, json=payload, stream=True, timeout=60)
        resp.raise_for_status()

        print("← Response OK. Streaming audio…")
        for idx, line in enumerate(resp.iter_lines(decode_unicode=True), 1):
            if not line:
                continue

            try:
                chunk = json.loads(line)
            except json.JSONDecodeError:
                print(f"[Line {idx}] JSON decode error, skipping")
                continue

            if err := chunk.get("error"):
                print(f"[API ERROR @ chunk {idx}]: {err}")
                continue

            b64 = chunk.get("audio_base64")
            if not b64:
                print(f"[Warning @ chunk {idx}]: no audio_base64")
                continue

            try:
                audio_data.extend(base64.b64decode(b64))
            except Exception as exc:
                print(f"[Base64 Error @ chunk {idx}]: {exc}")
                continue

    except HTTPError as he:
        print(f"[HTTP ERROR] {he.response.status_code}: {he.response.text}")
        sys.exit(1)
    except RequestException as re:
        print(f"[REQUEST ERROR] {re}")
        sys.exit(1)
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        sys.exit(1)

    # Write MP3
    try:
        out_path.write_bytes(audio_data)
        print(f"✔ Wrote {len(audio_data)} bytes to {out_path}\n")
    except Exception as fe:
        print(f"[FILE WRITE ERROR] {fe}")
        sys.exit(1)

def main():
    print("=== ElevenLabs TTS with Narrator Selection ===")
    voice_id = choose_voice()
    text = get_text()
    if len(text.split()) > WORD_LIMIT:
        stream_tts_to_mp3(voice_id, text, OUTPUT_FILE)
        remaining_text = get_remaining_text()
        if len(remaining_text.split()) > WORD_LIMIT:
            print("Error: Remaining text exceeds word limit. Please reduce the text length.")
            sys.exit(1)
        stream_tts_to_mp3(voice_id, remaining_text, OUTPUT_FILE.with_suffix(".mp3"))
    else:
        stream_tts_to_mp3(voice_id, text, OUTPUT_FILE)


if __name__ == "__main__":
    main()
