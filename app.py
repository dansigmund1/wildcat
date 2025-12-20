from flask import Flask, render_template, request, redirect, url_for
from scripts.wildcat import WildCat
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html", name="Flask")

@app.route("/dashboard", methods=["POST"])
def dashboard():
    file = request.files.get("file")
    if not file or file.filename == "":
        return "No file uploaded", 400
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    wc = WildCat(filepath)
    wc.convert_file()
    audio, sr = wc.read_audio()
    waveform = wc.display_waveform(audio, sr).to_html(full_html=False)
    spectrogram = wc.display_spectrogram(audio, sr).to_html(full_html=False)
    chromagram = wc.display_chromagram(audio, sr).to_html(full_html=False)
    mel_spectrogram = wc.display_mel_spectrogram(audio, sr).to_html(full_html=False)
    beats = wc.detect_beats(audio, sr)
    pitch = wc.get_pitch(audio, sr)
    return render_template("dashboard.html", 
                           waveform=waveform,
                           spectrogram=spectrogram,
                           chromagram=chromagram,
                           mel_spectrogram=mel_spectrogram,
                           beats=beats,
                           pitch=pitch,
                           filename=file.filename)

if __name__=="__main__":
    app.run(debug=True)