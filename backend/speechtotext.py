from google.cloud import speech_v1p1beta1 as speech

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

    results = []
    for result in response.results:
        alternative = result.alternatives[0]
        results.append(alternative.transcript)

    return results

audio_file = "C:\Users\lcs20\Desktop\mini-project\output_audio.wav"
transcriptions = transcribe_audio(audio_file)

for i, transcription in enumerate(transcriptions):
    print(f"Transcription {i + 1}: {transcription}")
