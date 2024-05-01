import ffmpeg

class FFMConvertor:
    def convert_webm_mp4(self, input_file_path, output_file_path):
        try:
            stream = ffmpeg.input(input_file_path)
            stream = ffmpeg.output(stream, output_file_path)
            ffmpeg.run(stream)
        except Exception as e:
            print("e", e)

ffmconvertor = FFMConvertor()
# ffmConvertor.convert_webm_mp4('test.webm', 'test.mp4')
