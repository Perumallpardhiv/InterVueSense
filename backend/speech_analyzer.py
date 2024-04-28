import os
import wave
import librosa
import numpy as np
from uuid import uuid1
import speech_recognition as sr

from utils import cprint


def video_to_text(file_path):
    audio_path = f'uploads\\{uuid1()}.wav'
    text_file_path = f'uploads\\{uuid1()}.txt'
    command2wav = f"support\\ffmpeg -i {file_path} -v quiet -vn -acodec pcm_s16le -ar 44100 -ac 2 {audio_path}"
    cprint(command2wav)
    os.system(command2wav)
    r = sr.Recognizer()
    audio = sr.AudioFile(audio_path)

    speech_text = []
    with audio as source:
        audio = r.record(source, duration=300)
        try:
            text = r.recognize_google(audio)
        except sr.UnknownValueError:
            text = ''

        with open(text_file_path, "w+") as file:
            file.write(text)
            speech_text.append(text)

    speech_text = ' '.join(speech_text)
    return audio_path, speech_text


def speech_speed(audio_path, speech_text):
    word_count = len(speech_text.split())
    with wave.open(audio_path, 'r') as f:
        frames = f.getnframes()
        rate = f.getframerate()

    duration_min = frames / (rate * 60)
    wpm = word_count / duration_min
    speed = 'Slow'
    if wpm > 120 and wpm <= 160:
        speed = 'Medium'
    elif (wpm > 160):
        speed = 'Fast'

    return wpm, speed


def pause_detection(audio_path):
    # Load the audio file
    x, sr = librosa.load(audio_path, sr=None)

    # Calculate the top decibel threshold dynamically
    topDB = np.max(librosa.amplitude_to_db(np.abs(x), ref=np.max))

    # Use librosa.effects.split without specifying topDB as an argument
    nonMuteSections = librosa.effects.split(x)
    
    # Calculate initial pause and mute percentages based on nonMuteSections
    total_frames = len(x)
    pause_frames = sum(stop - start for start, stop in nonMuteSections)
    
    initial_pause_percent = (nonMuteSections[0][0] / total_frames) * 100
    mute_percent = (pause_frames / total_frames) * 100

    return initial_pause_percent, mute_percent


def find_filler_words(speech_text):
    speech_text = speech_text.split()

    filler_words = ["like", "um", "might", "aa", "aaa", "mean", "know", "well", "totally",
                    "really", "basically", "no", "oh", "so", "maybe", "somehow", "some", "okay", "very"]

    total_filler_words = 0
    for word in filler_words:
        total_filler_words += speech_text.count(word)
    percent = (total_filler_words / max(len(speech_text), 1)) * 100
    return total_filler_words, percent


def analize_audio(file_path):
    audio_path, speech_text = video_to_text(file_path)

    wpm, speed = speech_speed(audio_path, speech_text)
    initial_pause_percent, mute_percent = pause_detection(audio_path)
    total_filler_words, filler_percent = find_filler_words(speech_text)

    output = {
        'wpm': wpm,
        'speed': speed,
        'initial_pause_percent': initial_pause_percent,
        'mute_percent': mute_percent,
        'total_filler_words': total_filler_words,
        'filler_percent': filler_percent
    }

    return output
