import os
from .Singleton import Singleton

class ffmpegService(metaclass=Singleton):

    def __init__(self):
        pass

    def generate_mp4(self, mp3_path, png_path, output_path):
        os_command = f"ffmpeg -i {mp3_path} -loop 1 -i {png_path} -c:v libx264 -preset veryslow -tune stillimage -crf 18 -pix_fmt yuv420p -vf scale=300:300 -c:a aac -b:a 192k -shortest {output_path}"
        os.system(os_command)
        return True