import librosa as lb
import numpy as np
import plotly.graph_objects as go
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
        
    def display_waveform(self, audio, sr):
        time = np.arange(len(audio)) / sr
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time,
            y=audio,
            mode="lines",
            hovertemplate="Time: %{x:.2f}s<br>Amplitude: %{y:.3f}"
        ))
        fig.update_layout(title="Waveform", xaxis_title="Time (s)", yaxis_title="Amplitude")
        return fig

    def display_spectrogram(self, audio, sr):
        X = lb.stft(audio)
        Xdb = lb.amplitude_to_db(np.abs(X))
        times = np.arange(Xdb.shape[1]) * (len(audio) / sr) / Xdb.shape[1]
        freqs = np.linspace(0, sr / 2, Xdb.shape[0])
        fig = go.Figure(data=go.Heatmap(
            z=Xdb,
            x=times,
            y=freqs,
            colorscale='Viridis',
            colorbar=dict(title='dB'),
            hovertemplate='Time: %{x:.2f}s<br>Frequency: %{y:.1f}Hz<br>Amplitude: %{z:.1f}dB'
        ))
        fig.update_layout(
            title="Spectrogram",
            xaxis_title="Time (s)",
            yaxis_title="Frequency (Hz)",
            yaxis=dict(autorange='reversed')
        )
        return fig

    def detect_beats(self, audio, sr):
        tempo, beat_frames = lb.beat.beat_track(y=audio, sr=sr)
        beat_times = lb.frames_to_time(beat_frames, sr=sr)
        return tempo, beat_times

    def get_pitch(self, audio, sr):
        pitch, _ = lb.piptrack(y=audio, sr=sr)
        pitches = pitch[pitch > 0]
        return pitches[:20]

    def display_chromagram(self, audio, sr):
        chroma = lb.feature.chroma_stft(y=audio, sr=sr)
        times = np.arange(chroma.shape[1]) * (len(audio) / sr) / chroma.shape[1]
        chroma_labels = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        fig = go.Figure(data=go.Heatmap(
            z=chroma,
            x=times,
            y=chroma_labels,
            colorscale='Viridis',
            colorbar=dict(title='Amplitude'),
            hovertemplate='Time: %{x:.2f}s<br>Chroma: %{y}<br>Amplitude: %{z:.2f}<extra></extra>'
        ))
        fig.update_layout(
            title="Chromagram",
            xaxis_title="Time (s)",
            yaxis_title="Chroma",
            yaxis=dict(autorange='reversed')
        )
        return fig

    def display_mel_spectrogram(self, audio, sr):
        mel = lb.feature.melspectrogram(y=audio, sr=sr)
        mel_db = lb.power_to_db(mel, ref=np.max)
        times = np.arange(mel_db.shape[1]) * (len(audio) / sr) / mel_db.shape[1]
        mel_freqs = lb.mel_frequencies(n_mels=mel_db.shape[0], fmin=0, fmax=sr/2)
        fig = go.Figure(data=go.Heatmap(
            z=mel_db,
            x=times,
            y=mel_freqs,
            colorscale='Viridis',
            colorbar=dict(title='dB'),
            hovertemplate='Time: %{x:.2f}s<br>Mel Frequency: %{y:.1f}Hz<br>Amplitude: %{z:.1f} dB<extra></extra>'
        ))
        fig.update_layout(
            title="Mel Spectrogram",
            xaxis_title="Time (s)",
            yaxis_title="Mel Frequency (Hz)",
            yaxis=dict(autorange='reversed')
        )
        return fig

# For manipulation:
# librosa.effects.time_stretch(audio, rate=1.25)  # speed up
# librosa.effects.pitch_shift(audio, sr=sr, n_steps=4)  # shift up 4 semitones