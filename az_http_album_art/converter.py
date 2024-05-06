import os
import tempfile

def convert_to_mp4(request):
    tmp_file = tempfile.NamedTemporaryFile(dir=f'{os.getcwd()}')
    try:
        if not request.get_body():
            return "Empty request body", None
        file_binary = request.get_body()
        tmp_file.write(file_binary)
    except Exception as e:
        return str(e), None
    try:
        image_path = '/Users/sohan/Desktop/Coke/script-albumArt-ffmpeg/cover.png'
        output_path = '/Users/sohan/Desktop/Coke/script-albumArt-ffmpeg/output.mp4'
        mp3_path = '/Users/sohan/Desktop/Coke/script-albumArt-ffmpeg/sample.mp3'
        cli_command = f"ffmpeg -i {mp3_path} -loop 1 -i {image_path} -c:v libx264 -preset veryslow -tune stillimage -crf 18 -pix_fmt yuv420p -vf scale=300:300 -c:a aac -b:a 192k -shortest {output_path}"

        os.system(cli_command)
        return None, output_path
    except Exception as e:
        return str(e), None