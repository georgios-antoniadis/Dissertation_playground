# Shape Similarity
# Dynamic Time Warping (DTW)
from fastdtw import fastdtw

def dtw(predicted, real):
  distance, path = fastdtw(predicted, real)

  # print(f"DTW Distance {distance}")
  # print(f"Optimal Alignment Path: {path}")
  # return distance, path
  return distance