# 🎵 Audio Visualizer
**Demo Image**:
![Demo Image](<Society (bonus).png>)

A real-time audio visualization tool that plays a WAV file and displays both a waveform and a spectrum analyzer. Built to explore digital audio concepts and real-time data rendering in Python.

**Link to project (GitHub repo):** [https://github.com/andysaghbini-jpg/audio-visualizer.git](https://github.com/andysaghbini-jpg/audio-visualizer.git)

---

## How It's Made

**Tech used:** Python, NumPy, Matplotlib, SimpleAudio, Python's built-in `wave` module  

The project starts by reading the audio file using Python’s built-in `wave` module. This module allows us to open a WAV file and extract information like the sample rate, number of channels, sample width, and total number of frames. These details are necessary because they tell the program how to interpret the raw audio data.

Once the WAV file is opened, the raw audio frames are converted into a NumPy array. If the audio is stereo, the code automatically selects a single channel to simplify the visualization. The values are then normalized to the range between -1.0 and 1.0, which makes it easier to plot them and perform calculations like Fast Fourier transforms (FFT) which takes the audio and shows how much energy exists at each frequency.

For audio playback, the program uses the `simpleaudio` library. This library is straightforward and lightweight, and it allows the audio to play in the background while the visualizations update in real time. The audio data is converted to the format that `simpleaudio` expects, which is 16-bit integers, and playback begins in a non-blocking way so the program doesn’t freeze while playing.

The visualizations themselves are built with `matplotlib`. The waveform is displayed on the top subplot, plotting the amplitude of a short chunk of audio samples at a time. Below it, the spectrum analyzer shows the frequency content. This is calculated using a Fast Fourier Transform (FFT), which converts the audio from the time domain to the frequency domain. Each bar in the spectrum represents a frequency bin, and the height of the bar corresponds to the amplitude of that frequency. To make it visually appealing, the bars are colored using a plasma colormap, with higher amplitudes resulting in brighter colors.

The animation is handled by `matplotlib`’s `FuncAnimation`, which repeatedly calls an update function. Each time the function runs, it slices the next chunk of audio, updates the waveform, recalculates the FFT, updates the spectrum bars,and then increments the position in the audio array. When it reaches the end of the file, it loops back to the beginning, allowing the visualizer to run continuously.

---

## Features
- Real-time waveform visualization
- Frequency-domain spectrum analyzer using FFT
- Smooth, continuous playback with looping
- Stereo -> mono handling, normalization, and chunk-based processing
- Color-mapped frequency bars using Matplotlib

---

## Lessons Learned

Building this project taught me a lot about **real-time data processing**, **signal analysis**, and **data visualization**. I learned how FFT works in practice, how to map audio energy to colors and animation, and how to handle audio playback concurrently with visualization. It also reinforced good practices for **Python code structure** and making projects readable and maintainable.  

This project gave me hands-on experience that I can talk about in interviews to show my passion for programming and learning new skills.  

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.