import ffmpy
import subprocess
import glob, os
from pydub import AudioSegment

def convertUsingFfmpy():
     ff = ffmpy.FFmpeg(
          inputs={'foo.webm': None},
          outputs={'foo.avi': None}
     )
     ff.run()


def convertUsingFFmpeg(filename, cmd=None):
    # cmd = "ffmpeg -i C:/test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    # cmd = "ffmpeg -i foo.webm -vn -acodec copy output.oga"
    # cmd = "ffmpeg -i " + filename + " -vn -acodec copy " + filename + ".oga"
    cmd = "ffmpeg -i " + filename + " " + filename + ".flac"
    print cmd
    subprocess.call(cmd, shell=True)


def convertUsingSox(filename, cmd=None):
    # cmd = "ffmpeg -i C:/test.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    # cmd = "ffmpeg -i foo.webm -vn -acodec copy output.oga"
    # cmd = "ffmpeg -i " + filename + " -vn -acodec copy " + filename + ".oga"
    cmd = "sox " + filename + " --channels=1 --bits=16 --rate=16000 --endian=little " + filename + ".flac"
    print cmd
    subprocess.call(cmd, shell=True)

def splitUsingSox(folder, file_type, o_file_type, o_folder, th):
    folder = 'data/transcribed-split'
    o_folder = 'split'
    file_type = 'flac'
    o_file_type = 'wav'
    th = 60

    #th in milliseconds
    os.chdir(folder)
    for file in glob.glob("*." + file_type):
        print(file)
        audio_file = AudioSegment.from_file(file, file_type)

        if (len(audio_file) < th):
            audio_file.export(o_folder + '\\' + file + '.' + o_file_type, o_file_type)
            continue

        start = 0
        end = th
        audio_left = len(audio_file)
        file_num = 1
        while (audio_left > 0):
            trimmed_file = audio_file[start:end]
            trimmed_file.export(o_folder + '\\' + file + str(file_num) + '.' + o_file_type, o_file_type)
            audio_left = audio_left - (end - start)
            start = end
            end = start + min(audio_left, th)
            file_num = file_num + 1

if __name__ == '__main__':
    #splitUsingSox('a', 'b', 'c', 12)
    pass

