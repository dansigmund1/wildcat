from flask import Flask, render_template
from scripts.wildcat import WildCat

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html", name="Flask")

@app.route("/dashboard")
def dashboard(audio_file):
    wc = WildCat(audio_file)
    wc.convert_file()
    audio, sr = wc.read_audio()
    waveform = wc.display_waveform(audio)
    spectogram = wc.display_spectogram(audio, sr)
    beats = wc.detect_beats(audio, sr)
    pitch = wc.get_pitch(audio, sr)
    chromagram = wc.display_chromagram(audio, sr)
    mel_spectogram = wc.display_mel_spectogram(audio, sr)
    return waveform, spectogram, beats, pitch, chromagram, mel_spectogram

if __name__=="__main__":
    app.run(debug=True)