#GOOGLE CLOUD API DETAILS REQUIRED



import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

# Set the environment variable for the service account key file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/service-account-key.json"

def upload_to_bucket(filename, source_file_name, bucket_name):
    # Implement your upload function here
    pass

def delete_blob(filename, bucket_name):
    # Implement your delete function here
    pass

def noOfSpeakers(speech_file):
    client = speech.SpeechClient()

    # Upload audio file to Google Cloud Storage
    gcs_uri = upload_to_bucket("meet_234", speech_file, "ml_jj1")

    # Configure audio settings
    audio = speech.RecognitionAudio(uri=gcs_uri)
    diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )

    config = speech.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        diarization_config=diarization_config,
    )

    # Perform asynchronous speech recognition
    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=500)

    try:
        for result in response.results:
            words_info = result.alternatives[0].words

        speakers = set()
        for word_info in words_info:
            speakers.add(int(word_info.speaker_tag))

        # Delete audio file from Google Cloud Storage
        delete_blob("meet_234", "ml_jj1")

    except Exception as e:
        # Delete audio file from Google Cloud Storage in case of any exceptions
        delete_blob("meet_234", "ml_jj1")
        print(f"Error: {e}")
        return 0

    return len(speakers)

# Test the function
speech_file = "path/to/your/audio/file.wav"
num_speakers = noOfSpeakers(speech_file)
print("Number of speakers:", num_speakers)
