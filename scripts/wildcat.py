import librosa as lb
import numpy as np
import matplotlib.pyplot as plt
import argparse
from pydub import AudioSegment

class WildCat:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def read_audio(self):
        audio, sr = lb.load(self.audio_file, sr=None)
        print(audio.shape, sr)
        return audio, sr

    def convert_file(self):
        if self.audio_file.endswith('.wav'):
            self.audio_file = self.audio_file
        elif self.audio_file.endwith('.m4a'):
            audio = AudioSegment.from_file(self.audio_file, format="m4a")
            audio.export(f"{self.audio_file.replace('.m4a','.wav')}", format="wav")
            self.audio_file = f"{self.audio_file}.wav"
        
    def display_waveform(self, audio):
        plt.plot(audio)
        plt.title("Waveform")
        plt.show()

    def display_spectogram(self, audio, sr):
        X = lb.stft(audio)
        Xdb = lb.amplitude_to_db(abs(X))
        plt.figure(figsize=(12,4))
        lb.display.specshow(Xdb, sr=sr, x_axis="time", y_axis="hz")
        plt.colorbar()
        plt.title("Spectrogram")
        plt.show()

    def detect_beats(self, audio, sr):
        tempo, beat_frames = lb.beat.beat_track(y=audio, sr=sr)
        beat_times = lb.frames_to_time(beat_frames, sr=sr)
        print(f"Tempo: {tempo}")
        print(f"Beat Times: {beat_times}")

    def get_pitch(self, audio, sr):
        pitch, mag = lb.piptrack(y=audio, sr=sr)
        pitches = pitch[pitch > 0]
        print(f"Estimated pitch values: {pitches[:20]}")

    def display_chromagram(self, audio, sr):
        chroma = lb.feature.chroma_stft(y=audio, sr=sr)
        plt.figure(figsize=(12, 4))
        lb.display.specshow(chroma, x_axis="time", y_axis="chroma", sr=sr)
        plt.colorbar()
        plt.title("Chromagram")
        plt.show()

    def display_mel_spectogram(self, audio, sr):
        mel = lb.feature.melspectrogram(y=audio, sr=sr)
        mel_db = lb.power_to_db(mel, ref=np.max)
        plt.figure(figsize=(12, 4))
        lb.display.specshow(mel_db, sr=sr, x_axis="time", y_axis="mel")
        plt.colorbar()
        plt.title("Mel Spectrogram")
        plt.show()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-af", "--audio_file", help="Audio File to Remix")
    args = parser.parse_args()
    wc = WildCat(args.audio_file)
    wc.convert_file()
    audio, sr = wc.read_audio()
    wc.display_spectogram(audio, sr)

# For manipulation:
# librosa.effects.time_stretch(audio, rate=1.25)  # speed up
# librosa.effects.pitch_shift(audio, sr=sr, n_steps=4)  # shift up 4 semitones