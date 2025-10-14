<h1>The Issues are with the virtual enviroment making , libs installations, linux env calls</h1>

<h2>Solution:</h2>
✅All the <a herf="https://github.com/itz-real-ks/Eleven-Labs/blob/main/requirements.txt">requirements.txt</a>  listed ones are corrected accordingly for win11 22h2 and linux 6.12.38+kali-amd64
Also needed to install dependency for this program : 
<pre><code>
 # For Debian/Ubuntu-based Systems
    sudo apt-get update
    sudo apt-get install portaudio19-dev
 # For Fedora/RHEL-based Systems
    sudo dnf install portaudio-devel
 # For macOS
    brew install portaudio
</code></pre>
