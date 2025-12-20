import librosa as lb
import numpy as np
import matplotlib.pyplot as plt
# import argparse
import io
import base64
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
        elif self.audio_file.endswith('.m4a'):
            audio = AudioSegment.from_file(self.audio_file, format="m4a")
            audio.export(f"{self.audio_file.replace('.m4a','.wav')}", format="wav")
            self.audio_file = f"{self.audio_file}.wav"

    def convert_figure(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        buf.close()
        return img_base64
        
    def display_waveform(self, audio):
        fig, ax = plt.subplots()
        ax.plot(audio)
        ax.set_title("Waveform")
        return fig

    def display_spectogram(self, audio, sr):
        X = lb.stft(audio)
        Xdb = lb.amplitude_to_db(abs(X))
        fig, ax = plt.subplots(figsize=(12,4))
        img = lb.display.specshow(
            Xdb,
            sr=sr,
            x_axis="time",
            y_axis="hz",
            ax=ax
        )
        fig.colorbar(img, ax=ax)
        ax.set_title("Spectrogram")
        return fig

    def detect_beats(self, audio, sr):
        tempo, beat_frames = lb.beat.beat_track(y=audio, sr=sr)
        beat_times = lb.frames_to_time(beat_frames, sr=sr)
        # print(f"Tempo: {tempo}")
        # print(f"Beat Times: {beat_times}")
        return tempo, beat_times

    def get_pitch(self, audio, sr):
        pitch, mag = lb.piptrack(y=audio, sr=sr)
        pitches = pitch[pitch > 0]
        # print(f"Estimated pitch values: {pitches[:20]}")
        return pitches[:20]

    def display_chromagram(self, audio, sr):
        chroma = lb.feature.chroma_stft(y=audio, sr=sr)
        fig, ax = plt.subplots(figsize=(12, 4))
        img = lb.display.specshow(
            chroma,
            x_axis="time",
            y_axis="chroma",
            sr=sr,
            ax=ax
        )
        fig.colorbar(img, ax=ax)
        ax.set_title("Chromagram")
        return fig

    def display_mel_spectogram(self, audio, sr):
        mel = lb.feature.melspectrogram(y=audio, sr=sr)
        mel_db = lb.power_to_db(mel, ref=np.max)
        fig, ax = plt.subplots(figsize=(12, 4))
        img = lb.display.specshow(
            mel_db,
            sr=sr,
            x_axis="time",
            y_axis="mel",
            ax=ax
        )
        fig.colorbar(img, ax=ax)
        ax.set_title("Mel Spectrogram")
        return fig

#     def display_dashboard(self):
#         self.convert_file()
#         audio, sr = self.read_audio()
#         waveform = self.convert_figure(self.display_waveform(audio))
#         spectogram = self.convert_figure(self.display_spectogram(audio, sr))
#         retdict = {'waveform':waveform,
#                    'spectogram':spectogram}# ,
#                 #    'beats':self.detect_beats(audio, sr),
#                 #    'pitch':self.get_pitch(audio, sr),
#                 #    'chromagram':self.display_chromagram(audio, sr),
#                 #    'mel_spectogram':self.display_mel_spectogram(audio, sr)}
#         return retdict

# if __name__=="__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-af", "--audio_file", help="Audio File to Remix")
#     args = parser.parse_args()
#     wc = WildCat(args.audio_file)
#     wc.display_dashboard()

# For manipulation:
# librosa.effects.time_stretch(audio, rate=1.25)  # speed up
# librosa.effects.pitch_shift(audio, sr=sr, n_steps=4)  # shift up 4 semitones