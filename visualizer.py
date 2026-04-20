import wave
import time
import numpy as np
import simpleaudio as sa
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

FILENAME = "runaway.wav"
CHUNK = 2048
CHANNEL = 0

# Load WAV

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

# Setup plots

fig, (ax_wave, ax_fft) = plt.subplots(2, 1, figsize=(10, 6))
plt.subplots_adjust(hspace=0.5)

# Waveform Plot
x = np.arange(CHUNK)
line, = ax_wave.plot(x, np.zeros(CHUNK), color='purple', lw=1.5)
ax_wave.set_ylim(-1.0, 1.0)
ax_wave.set_xlim(0, CHUNK)
ax_wave.set_title("Waveform", color='white')
ax_wave.set_facecolor('black')
ax_wave.tick_params(colors='white')

# Spectrum Analyzer Plot
freqs = np.fft.rfftfreq(CHUNK, 1/sr)
line_fft, = ax_fft.plot(freqs, np.zeros_like(freqs), color='magenta', lw=2)
fill_fft = ax_fft.fill_between(freqs, -80, np.zeros_like(freqs), color='magenta', alpha=0.3)

ax_fft.set_xlim(0, 20000)
ax_fft.set_ylim(-80, 0)
ax_fft.set_title("Spectrum Analyzer", color='white')
ax_fft.set_facecolor('black')
ax_fft.tick_params(colors='white')

fig.patch.set_facecolor('black')

start_time = None


# Update function

def update(frame):
    global start_time, fill_fft
    
    if start_time is None:
        return line, line_fft
    
    elapsed = time.time() - start_time
    pos = int(elapsed * sr)
    
    if pos >= len(audio):
        return line, line_fft

    seg = audio[pos:pos + CHUNK]
    if len(seg) < CHUNK:
        seg = np.pad(seg, (0, CHUNK - len(seg)))

    # 1. Update Waveform
    line.set_ydata(seg)

    # 2. Update FFT
    fft = np.abs(np.fft.rfft(seg))
    fft_db = 20 * np.log10(fft + 1e-6)
    line_fft.set_ydata(fft_db)
    
    verts = fill_fft.get_paths()[0].vertices
    verts[1:len(fft_db)+1, 1] = fft_db 

    rms = np.sqrt(np.mean(seg**2))
    pulse = min(rms * 2, 0.2)  
    pulse_color = (pulse, pulse, pulse) 
    ax_wave.set_facecolor(pulse_color)

    return line, line_fft, fill_fft

# Animation & Playback

animation = FuncAnimation(fig, update, interval=30, blit=True)
play_obj = sa.play_buffer((audio * 32767).astype(np.int16), 1, 2, sr)
start_time = time.time() 

plt.show()

if play_obj.is_playing():
    play_obj.stop()