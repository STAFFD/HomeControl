from os.path import join
import os


class Sounder:
    def __init__(self):
        folder = "sound"
        self.fileNames = [join(folder, "receive.mp3"),
                          join(folder, "receive2.mp3")]

    def play(self, fileName):
        assert type(fileName) == str
        if os.name == "posix":
            os.system(f'afplay {fileName}')
        else:
            os.system(f'mplayer {fileName} -volume 70')

    def receive1(self):
        self.play(self.fileNames[0])

    def receive2(self):
        self.play(self.fileNames[1])


if __name__ == '__main__':
    Sounder().receive2()
