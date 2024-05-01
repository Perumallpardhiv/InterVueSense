import math
from google.cloud import speech_v1p1beta1 as speech

class isQuestion:
    def predict_question(self, sentence):
        # Implement your logic here to predict whether the sentence is a question
        # Example: return 1 if it's a question, 0 otherwise
        if "?" in sentence:
            return 1
        else:
            return 0

def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    with open(audio_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Adjust according to your audio
        language_code="en-US",  # Adjust for language code
    )

    response = client.recognize(config=config, audio=audio)

    transcriptions = []
    for result in response.results:
        alternative = result.alternatives[0]
        transcriptions.append(alternative.transcript)

    return transcriptions

def calculate_word_stamps(transcript, audio_duration):
    words = transcript.split()  # Split the transcript into individual words
    word_count = len(words)
    word_duration = audio_duration / word_count  # Calculate the duration of each word

    word_stamps = []
    current_time = 0
    for word in words:
        word_stamps.append((word, current_time, current_time + word_duration))
        current_time += word_duration

    return word_stamps

def calculate_response_times(transcript, word_stamps):
    obj = isQuestion()
    response_times = []
    words = 0
    try:
        for i in range(len(transcript)):
            if obj.predict_question(transcript[i]) == 1:
                word_end_of_question = word_stamps[words - 1][2]
                passed = words
                j = i
                while j < len(transcript) and obj.predict_question(transcript[j]) == 1:
                    passed += len(transcript[j].split(" "))
                    j += 1
                if passed < len(word_stamps):
                    word_start_of_response = word_stamps[passed - 1][1]
                    responsetime = word_start_of_response - word_end_of_question
                    response_times.append(math.ceil(responsetime.total_seconds()))
            words += len(transcript[i].split(" "))
    except Exception as e:
        print("Error:", e)
        print("Index:", i)
    return response_times

def average_response_time(response_times):
    if response_times:
        return sum(response_times) / len(response_times)
    else:
        return 0

# Example usage
audio_file = "your_audio_file.wav"  # Replace with your audio file path

transcriptions = transcribe_audio(audio_file)
audio_duration = 60  # Replace with the duration of your audio file
word_stamps = calculate_word_stamps(" ".join(transcriptions), audio_duration)
response_times = calculate_response_times(transcriptions, word_stamps)
avg_response = average_response_time(response_times)
print("Average response time:", avg_response)
