import pyttsx3
import re
import numpy as np
import argparse

# Define the command-line arguments
parser = argparse.ArgumentParser(description="Text-to-Speech Generator")
parser.add_argument("-t", "--text", help="Text to convert to speech")
parser.add_argument("-f", "--file", help="Path to the script file")
parser.add_argument("-o", "--output", help="Output file path")

# Parse the command-line arguments
args = parser.parse_args()

# Initialize the TTS engine
try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    exit(1)

# Define a dictionary of emotions and their corresponding speech rates
emotions = {
    "whispering": 0.5,
    "sarcastic": 1.2,
    "softly": 0.8,
    "exhales": 1.0,
    "angry": 1.5,
    "happy": 1.2,
    "sad": 0.8,
}

# Get the text to convert to speech
if args.text:
    text = args.text
elif args.file:
    try:
        with open(args.file, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print("File not found")
        exit(1)
else:
    print("Please provide text or a file path")
    exit(1)

# Define a function to generate the audio
def generate_audio(text):
    # Split the text into blocks
    blocks = re.split(r"($$.*?$$)", text)

    # Iterate over the blocks
    for block in blocks:
        # Check if the block is an emotion block
        if block.startswith("[") and block.endswith("]"):
            # Get the emotion
            emotion = block[1:-1]

            # Check if the emotion is in the dictionary
            if emotion in emotions:
                # Set the speech rate
                engine.setProperty("rate", emotions[emotion] * 150)
        else:
            # Generate the audio for the text block
            engine.say(block)

    # Run the audio
    engine.runAndWait()

# Generate the audio
try:
    generate_audio(text)
except Exception as e:
    print(f"Error generating audio: {e}")
    exit(1)

# Save the audio to a file if specified
if args.output:
    try:
        engine.save_to_file(text, args.output)
        engine.runAndWait()
    except Exception as e:
        print(f"Error saving audio to file: {e}")
        exit(1)

# Use NumPy to manipulate the audio data
try:
    import sounddevice as sd
    from scipy.io.wavfile import read
    from scipy.io.wavfile import write

    # Read the audio file
    fs, data = read(args.output)

    # Manipulate the audio data using NumPy
    data = np.array(data, dtype=np.float32)
    data = data * 0.5  # Reduce the volume by half

    # Write the manipulated audio data to a new file
    write("manipulated_audio.wav", fs, data)
except Exception as e:
    print(f"Error manipulating audio data: {e}")
    exit(1)
