from os import listdir
from os.path import isfile, join
import ffmpeg
import numpy as np


def get_training_files(folder: str) -> np.array:
    print("getting files in folder", folder)
    files = [f for f in listdir(folder) if (isfile(join(folder, f)) & f.endswith(".mp3"))]
    return np.array(files)


def extract_samples_from_mp3(in_name: str):
    """
    Convert a MP3 file at the location `in_name` to a PCM encoded WAV with only one channel (mono)
    and extract the numeric 16-bit signed little indian integers as a numpy array.

    The function invokes ffmpeg which pipes the results to STDOUT from where it is read back in into
    a numpy array.


    """
    process1 = (ffmpeg.input(in_name)
         .output("pipe:", format='s16le', ac=1, ar='16k')
         .overwrite_output()
         .run_async(pipe_stdout=True))
    in_bytes = process1.stdout.read()
    array = np.frombuffer(in_bytes, np.int16)
    return array

def raise_min(n: int) -> int:
    return n + 32768

def raise_min_of_array(array: np.array) -> np.array:
    return np.array(list(map(lambda x: raise_min(x), array)))

def bitfield(n):
    """
    Convert an unsigned 16-bit integer into a bitfield of size 16.
    Example: 7 -> [ 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 ]
    This will only work for unsigned integers so you need to make sure
    to raise signed integers by INT_MIN.
    """
    return np.array([n >> i & 1 for i in range(16 - 1, -1, -1)]).astype(dtype=np.bool)


def convert_mp3_to_bitfield(file: str, seq_len: int) -> np.array:
    samples = extract_samples_from_mp3(file)
    samples = raise_min_of_array(samples)
    np.split()
    return get_bitfield_from_array(samples)


def get_bitfield_from_array(array: np.array)-> np.array:
    """Convert a whole array of unsigned 16 bit ints into a bitfield"""
    return np.array(list(map(lambda x: bitfield(x), array)))
