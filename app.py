from flask import Flask, render_template, request, redirect, url_for
from scripts.wildcat import WildCat
import plotly.graph_objects as go
import numpy as np
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
    time = np.arange(len(audio)) / sr
    fig = go.Figure()
    fig.add_trace(go.Scatter(
    x=time,
    y=audio,
    mode="lines",
    hovertemplate="Time: %{x:.2f}s<br>Amplitude: %{y:.3f}"
    ))
    waveform = wc.convert_figure(wc.display_waveform(audio))
    spectogram = wc.convert_figure(wc.display_spectogram(audio, sr))
    chromagram = wc.convert_figure(wc.display_chromagram(audio, sr))
    mel_spectogram = wc.convert_figure(wc.display_mel_spectogram(audio, sr))
    beats = wc.detect_beats(audio, sr)
    pitch = wc.get_pitch(audio, sr)
    return render_template("dashboard.html", 
                           waveform=waveform,
                           spectogram=spectogram,
                           chromagram=chromagram,
                           mel_spectogram=mel_spectogram,
                           beats=beats,
                           pitch=pitch,
                           filename=file.filename,
                           graph=fig.to_html(full_html=False))

if __name__=="__main__":
    app.run(debug=True)