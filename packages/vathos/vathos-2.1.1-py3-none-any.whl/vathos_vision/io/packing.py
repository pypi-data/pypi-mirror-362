# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2019-2025, Vathos GmbH
#
# All rights reserved.
#
###############################################################################
"""Various byte packing algorithms."""

import numpy as np


def pack_short(short_array):
  """Pack two bytes of a single short channel into RG channels of an RGB image."""
  short = np.zeros(tuple(short_array.shape) + (3,), dtype=np.uint8)
  short[:, :,
        0:2] = np.reshape(np.frombuffer(short_array.tobytes(), dtype=np.uint8),
                          short_array.shape + (2,))
  return short


def unpack_short(rgb):
  """Unpack two byte channels into a single channel of type short."""
  return rgb[:, :, 0] + 255 * rgb[:, :, 1]


def pack_float(float_array):
  """Pack four bytes of a single float channel into an RGBA image."""
  dump = float_array.tobytes()
  r_channel = np.frombuffer(dump[0::4], dtype='uint8')
  g_channel = np.frombuffer(dump[1::4], dtype='uint8')
  b_channel = np.frombuffer(dump[2::4], dtype='uint8')
  a_channel = np.frombuffer(dump[3::4], dtype='uint8')
  return np.dstack((r_channel, g_channel, b_channel, a_channel))


def unpack_float(rgba):
  """Unpack four byte channels into a single channel of type float."""
  return np.reshape(np.frombuffer(rgba.flatten().tobytes(), dtype='f'),
                    rgba.shape[:2])
