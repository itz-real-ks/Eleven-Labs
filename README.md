<h1>Eleven Labs API Exploit 🔥</h1>
<p>Python scripts to use manifest from diff models from <a href="https://elevenlabs.io">elevenlabs.io</a> landing page free model --> Unauthorized = 1 🤖</p>
<p><strong>⚠️ Disclaimer:</strong> For educational purposes only. Ensure compliance with laws and terms of service when testing APIs 📝</p>

<h2>Features 🚀</h2>
<ul>
  <li><strong>API Exploit Exploration:</strong> Discover vulnerabilities 🔓</li>
  <li><strong>Testing Suite:</strong> Script for custom tests 🧪</li>
  <li><strong>Easy Setup:</strong> Simple running process 💻</li>
</ul>

<h2>Installation 💻</h2>
<p>Follow these steps to set up:</p>
<h3>1. Clone the repository 📦</h3>
<pre><code>git clone https://github.com/itz-real-ks/Eleven-Labs-API-Exploit.git
cd Eleven-Labs-API-Exploit</code></pre>
<h3>2. Install Dependencies 📦</h3>
<pre><code>pip install -r requirements.txt</code></pre>

<h1>Usage 🚀</h1>

### ⛔Work is ongoing on Time-stamped script generation!⛔

<p>Run the exploit:</p>
<pre><code> > python .\elevenlabs-web-api.py -h
usage: elevenlabs-web-api.py [-h] [-s SCRIPT] [-o OUTPUT] [-f FORMAT] [-sf SUBTITLE_FORMAT] [--speed SPEED]
                             [--model {eleven_monolingual_v1,eleven_multilingual_v1,eleven_v3}] [-i] [--stream]

Text-to-Speech Converter

options:
  -h, --help            show this help message and exit
  -s, --script SCRIPT   Script file
  -o, --output OUTPUT   Output file
  -f, --format FORMAT   Output format (mp3 or wav)
  -sf, --subtitle_format SUBTITLE_FORMAT
                        Subtitle format (srt, txt, or json)
  --speed SPEED         Speech speed (e.g., 0.5 for slow, 2.0 for fast)
  --model {eleven_monolingual_v1,eleven_multilingual_v1,eleven_v3}
                        Voice model version
  -i, --interactive     Interactive mode
  --stream              Stream audio without saving</code></pre>
<p>Check the help menu for more options 🤔</p>


#### Other Free Models 🤤
- eleven_turbo_v2_5 
- eleven_turbo_v2
- eleven_flash_v2

#### Direct arg.s here : 
<pre> <code>
 ----- ARGUMENTS -----
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
</code></pre>

<h2>Contributing 🤝</h2>
<p>Help me by fork-ing, creating a branch, and opening a pull request 📈</p>

<h2>License 📄</h2>
<p>Licensed under the MIT License. See <a href="LICENSE">LICENSE</a> for details 📝</p>

<h2>Contact 📬</h2>
<p>For inquiries, reach out to the maintainer:</p>
<ul>
  <li>Email: <a href="mailto:icy-kept-shucking@duck.com">Mail Me 📧</a></li>
</ul>

<h2>Disclaimer ⚠️</h2>
<p>This repository is for <strong>educational purposes</strong> only. Ensure you have permission before testing any API 🚫</p>
