# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import unicodedata

import numpy as np
import six
from functools import partial


SPIECE_UNDERLINE = '▁'


def printable_text(text):
  """Returns text encoded in a way suitable for print or `tf.logging`."""

  # These functions want `str` for both Python2 and Python3, but in one case
  # it's a Unicode string and in the other it's a byte string.
  if six.PY3:
    if isinstance(text, str):
      return text
    elif isinstance(text, bytes):
      return text.decode("utf-8", "ignore")
    else:
      raise ValueError("Unsupported string type: %s" % (type(text)))
  elif six.PY2:
    if isinstance(text, str):
      return text
    elif isinstance(text, unicode):
      return text.encode("utf-8")
    else:
      raise ValueError("Unsupported string type: %s" % (type(text)))
  else:
    raise ValueError("Not running on Python2 or Python 3?")


def print_(*args):
  new_args = []
  for arg in args:
    if isinstance(arg, list):
      s = [printable_text(i) for i in arg]
      s = ' '.join(s)
      new_args.append(s)
    else:
      new_args.append(printable_text(arg))
  print(*new_args)


def preprocess_text(inputs, lower=False, remove_space=True, keep_accents=False):
  if remove_space:
    outputs = ' '.join(inputs.strip().split())
  else:
    outputs = inputs
  outputs = outputs.replace("``", '"').replace("''", '"')

  if six.PY2 and isinstance(outputs, str):
    outputs = outputs.decode('utf-8')

  if not keep_accents:
    outputs = unicodedata.normalize('NFKD', outputs)
    outputs = ''.join([c for c in outputs if not unicodedata.combining(c)])
  if lower:
    outputs = outputs.lower()

  return outputs


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
    return np.array([n >> i & 1 for i in range(16 - 1, -1, -1)])


def get_bitfield_from_array(array: np.array) -> np.array:
    """Convert a whole array of unsigned 16 bit ints into a bitfield"""
    return np.array(list(map(lambda x: bitfield(x), array)))


def encode_pieces(arr: np.array) -> np.array:
    return encode_ids(arr)


def encode_ids(array: np.array):
    return get_bitfield_from_array(array)


if __name__ == '__main__':
  import sentencepiece as spm
  #
  # sp = spm.SentencePieceProcessor()
  # sp.load('sp10m.uncased.v3.model')
  #
  # print_(u'I was born in 2000, and this is falsé.')
  # print_(u'ORIGINAL', sp.EncodeAsPieces(u'I was born in 2000, and this is falsé.'))
  # print_(u'OURS', encode_pieces(sp, u'I was born in 2000, and this is falsé.'))
  # print(encode_ids(sp, u'I was born in 2000, and this is falsé.'))
  # print_('')
  # prepro_func = partial(preprocess_text, lower=True)
  # print_(prepro_func('I was born in 2000, and this is falsé.'))
  # print_('ORIGINAL', sp.EncodeAsPieces(prepro_func('I was born in 2000, and this is falsé.')))
  # print_('OURS', encode_pieces(sp, prepro_func('I was born in 2000, and this is falsé.')))
  # print(encode_ids(sp, prepro_func('I was born in 2000, and this is falsé.')))
  # print_('')
  # print_('I was born in 2000, and this is falsé.')
  # print_('ORIGINAL', sp.EncodeAsPieces('I was born in 2000, and this is falsé.'))
  # print_('OURS', encode_pieces(sp, 'I was born in 2000, and this is falsé.'))
  # print(encode_ids(sp, 'I was born in 2000, and this is falsé.'))
  # print_('')
  # print_('I was born in 92000, and this is falsé.')
  # print_('ORIGINAL', sp.EncodeAsPieces('I was born in 92000, and this is falsé.'))
  # print_('OURS', encode_pieces(sp, 'I was born in 92000, and this is falsé.'))
  # print(encode_ids(sp, 'I was born in 92000, and this is falsé.'))
  #
