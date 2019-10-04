from os import listdir
from os.path import isfile, join

import ffmpeg
import numpy as np


class Mp3Converter:
    """
    Read in a .mp3 encoded file, convert it into a PCM 16bit signed little endian WAVE and
    extract the amplitudes over time.
    This will
    """

    def __init__(self, folder: str, step_size: int):
        self.training_files = self.get_training_files(folder)
        self.buffer = None
        self.pos = None
        self.step_size = step_size
        self.buffer_length = None


    def start_next_file(self):
        if len(self.training_files) > 0:
            self.pos = 0
            self.buffer = Mp3Converter.extract_samples_from_mp3(self.training_files[0])
            self.buffer_length = len(self.buffer)
            self.training_files = self.training_files[1:len(self.training_files)]
        else:
            raise StopIteration()

    def __next__(self):
        return self.next()

    def print_status(self):
        print("pos: ", self.pos)
        print("buffer remaining: ", self.buffer_length - self.pos)


    # def read_raw_wave(self, filename):
    #     np.memmap(filename,  dtype='h', mode = 'c', offset = 0)

    def next(self):
        if self.pos is None:
            self.start_next_file()

        if (self.pos + self.step_size) >= self.buffer_length:
            self.start_next_file()

        result = self.buffer[self.pos]
        self.pos += 1
        return result


    def __iter__(self):
        return self

    def __call__(self, *args, **kwargs):
        return self