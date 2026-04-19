"""
VOICE ANALYSIS LAB
Record → Analyze → Compare → Visualize
"""

import threading
import sys
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import speech_recognition as sr
from speech_recognition import AudioData

# Global stop signal
stop_event = threading.Event()


# -------------------------------
# Wait for user to press Enter
# -------------------------------
def wait_for_enter():
    input("\n⏹️ Press Enter to stop recording...\n")
    stop_event.set()


# -------------------------------
# Record audio from microphone
# -------------------------------
def record_audio(label):
    stop_event.clear()  # reset before each recording

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024
    )

    frames = []

    print(f"\n🎤 {label}")
    print("Recording...")

    # Start thread to listen for Enter key
    threading.Thread(target=wait_for_enter, daemon=True).start()

    while not stop_event.is_set():
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    print("✅ Recording stopped")

    # Cleanup
    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()

    return b''.join(frames), 16000, width


# -------------------------------
# Analyze audio properties
# -------------------------------
def analyze_audio(data, rate):
    samples = np.frombuffer(data, dtype=np.int16)

    duration = len(samples) / rate
    avg_volume = np.mean(np.abs(samples))
    max_volume = np.max(np.abs(samples))

    return {
        "duration": duration,
        "avg_volume": avg_volume,
        "max_volume": max_volume,
        "samples": samples
    }


# -------------------------------
# Speech to text
# -------------------------------
def transcribe(data, rate, width):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(AudioData(data, rate, width))
        return text
    except:
        return "[Could not transcribe]"


# -------------------------------
# Display results
# -------------------------------
def display_stats(stats, text, label):
    print("\n" + "=" * 40)
    print(f"📊 {label}")
    print("=" * 40)

    print(f"⏱️ Duration       : {stats['duration']:.2f} sec")
    print(f"🔊 Avg Amplitude  : {stats['avg_volume']:.0f}")
    print(f"📈 Max Amplitude  : {stats['max_volume']:.0f}")
    print(f"📝 Transcription  : {text}")


# -------------------------------
# Compare two recordings
# -------------------------------
def compare(stats1, stats2):
    print("\n" + "=" * 40)
    print("⚖️ COMPARISON")
    print("=" * 40)

    # Duration comparison
    if stats1["duration"] > stats2["duration"]:
        diff = ((stats1["duration"] - stats2["duration"]) / stats2["duration"]) * 100
        print(f"⏱️ Recording 1 is longer by {diff:.1f}%")
    else:
        diff = ((stats2["duration"] - stats1["duration"]) / stats1["duration"]) * 100
        print(f"⏱️ Recording 2 is longer by {diff:.1f}%")

    # Volume comparison
    if stats1["avg_volume"] > stats2["avg_volume"]:
        diff = ((stats1["avg_volume"] - stats2["avg_volume"]) / stats2["avg_volume"]) * 100
        print(f"🔊 Recording 1 is louder by {diff:.1f}%")
    else:
        diff = ((stats2["avg_volume"] - stats1["avg_volume"]) / stats1["avg_volume"]) * 100
        print(f"🔊 Recording 2 is louder by {diff:.1f}%")


# -------------------------------
# Plot waveforms
# -------------------------------
def plot_waveforms(stats1, stats2, rate):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

    # Recording 1
    t1 = np.linspace(0, len(stats1["samples"]) / rate, len(stats1["samples"]))
    ax1.plot(t1, stats1["samples"])
    ax1.set_title("Recording 1 (Normal)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)

    # Recording 2
    t2 = np.linspace(0, len(stats2["samples"]) / rate, len(stats2["samples"]))
    ax2.plot(t2, stats2["samples"])
    ax2.set_title("Recording 2 (Modified)")
    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True)

    plt.tight_layout()
    plt.show()


# -------------------------------
# Main program
# -------------------------------
def main():
    print("=" * 50)
    print("🎤 VOICE ANALYSIS LAB")
    print("=" * 50)

    print("\n👉 Recording 1: Speak normally")
    audio1, rate, width = record_audio("Recording 1")

    stats1 = analyze_audio(audio1, rate)
    text1 = transcribe(audio1, rate, width)
    display_stats(stats1, text1, "Recording 1 Results")

    input("\n👉 Press Enter to continue for Recording 2...")

    print("\n👉 Recording 2: Speak LOUDER or FASTER")
    audio2, rate, width = record_audio("Recording 2")

    stats2 = analyze_audio(audio2, rate)
    text2 = transcribe(audio2, rate, width)
    display_stats(stats2, text2, "Recording 2 Results")

    compare(stats1, stats2)
    plot_waveforms(stats1, stats2, rate)


# Run program
if __name__ == "__main__":
    main()
 
