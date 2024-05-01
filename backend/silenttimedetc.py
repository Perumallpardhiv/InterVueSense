from pydub import AudioSegment

def detect_silence(audio_file, silence_threshold=-40, min_silence_duration=100):
    sound = AudioSegment.from_wav(audio_file)

    silent_ranges = []

    start = 0
    end = 0
    is_silence = False

    for i, chunk in enumerate(sound[::10]):
        if chunk.dBFS < silence_threshold:
            if not is_silence:
                start = i * 10
                is_silence = True
        elif is_silence:
            end = i * 10
            if end - start >= min_silence_duration:
                silent_ranges.append((start, end))
            is_silence = False

    if is_silence:
        end = len(sound)
        if end - start >= min_silence_duration:
            silent_ranges.append((start, end))

    return silent_ranges

audio_file = "C:\Users\lcs20\Desktop\mini-project\output_audio.wav"
silence_threshold = -40  # Adjust according to your audio
min_silence_duration = 100  # Adjust according to your requirements

silent_ranges = detect_silence(audio_file, silence_threshold, min_silence_duration)

for start, end in silent_ranges:
    print(f"Silent duration: {start / 1000} - {end / 1000} seconds")
