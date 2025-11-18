# visualizer.py
import wave
import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm

FILENAME = "society.wav"
CHUNK = 2048
CHANNEL = 0

# -----------------------
# Load WAV
# -----------------------
wf = wave.open(FILENAME, 'rb')
sr = wf.getframerate()
n_channels = wf.getnchannels()
sampwidth = wf.getsampwidth()
n_frames = wf.getnframes()

frames = wf.readframes(n_frames)
audio = np.frombuffer(frames, dtype=np.int16)

if n_channels == 2:
    audio = audio.reshape(-1, 2)[:, CHANNEL]

audio = audio.astype(np.float32) / (2**(8*sampwidth - 1))

# -----------------------
# Playback
# -----------------------
play_obj = sa.play_buffer((audio * 32767).astype(np.int16), 1, 2, sr)

# -----------------------
# Setup plots
# -----------------------
fig, (ax_wave, ax_fft) = plt.subplots(2, 1, figsize=(10, 6))
plt.subplots_adjust(hspace=0.5)  # spread the plots apart

x = np.arange(CHUNK)
line, = ax_wave.plot(x, np.zeros(CHUNK), color='purple')
ax_wave.set_ylim(-1.0, 1.0)
ax_wave.set_xlim(0, CHUNK)
ax_wave.set_title("Waveform", color='white')
ax_wave.set_facecolor('black')
ax_wave.tick_params(colors='white')

freqs = np.fft.rfftfreq(CHUNK, 1/sr)
bars = ax_fft.bar(freqs, np.zeros_like(freqs), width=freqs[1]-freqs[0], color='magenta')
ax_fft.set_xlim(0, 20000)
ax_fft.set_ylim(-80, 0)
ax_fft.set_title("Spectrum Analyzer", color='white')
ax_fft.set_facecolor('black')
ax_fft.tick_params(colors='white')

# Set figure background dark
fig.patch.set_facecolor('black')

pos = 0
energy_history = []

# colormap for bars
cmap = cm.plasma

# -----------------------
# Update function
# -----------------------
def update(frame):
    global pos, energy_history
    seg = audio[pos:pos + CHUNK]
    if len(seg) < CHUNK:
        seg = np.pad(seg, (0, CHUNK - len(seg)))

    # waveform
    line.set_ydata(seg)

    # FFT
    fft = np.abs(np.fft.rfft(seg))
    fft_db = 20 * np.log10(fft + 1e-6)

    # simple color mapping (amplitude to color)
    fft_norm = (fft_db - np.min(fft_db)) / (np.max(fft_db) - np.min(fft_db) + 1e-6)
    for bar, h, c in zip(bars, fft_db, fft_norm):
        bar.set_height(h)
        bar.set_color(cmap(c))

   
    ax_wave.set_facecolor('black')

    pos += CHUNK
    if pos >= len(audio):
        pos = 0

    return (line, *bars)

# -----------------------
# Animation
# -----------------------
animation = FuncAnimation(fig, update, interval=1000 * CHUNK / sr, blit=True)
plt.show()
play_obj.wait_done()