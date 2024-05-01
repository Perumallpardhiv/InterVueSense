from moviepy.editor import VideoFileClip

def extract_audio(video_file, output_audio_file):
    # Load the video clip
    video_clip = VideoFileClip(video_file)

    # Extract audio
    audio_clip = video_clip.audio

    # Save the audio clip to a file
    audio_clip.write_audiofile(output_audio_file)

    # Close the video clip
    video_clip.close()

# Example usage:
video_file = r"C:\Users\lcs20\Desktop\mini-project\Focus-main\Video.mp4"
output_audio_file = "output_audio.wav"
extract_audio(video_file, output_audio_file)
