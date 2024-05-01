mport os
from pyaudioanalysis import audioSegmentation as aS

# Function to perform speaker diarization
def noOfSpeakers(speech_file):
    # Perform speaker diarization
    flags_ind, classes_all, acc = aS.speaker_diarization(speech_file, 1, plot_res=False)

    # Determine unique speakers
    unique_speakers = len(set(flags_ind))

    return unique_speakers

# Test the function
speech_file = "C:\Users\lcs20\Desktop\mini-project\output_audio.wav"
num_speakers = noOfSpeakers(speech_file)
print("Number of speakers:", num_speakers)
