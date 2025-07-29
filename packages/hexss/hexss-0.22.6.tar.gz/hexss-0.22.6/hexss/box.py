from typing import Sequence, Tuple, Union
import numpy as np

def xywh2xyxy(
    *args: Union[Sequence[float], np.ndarray, float]
) -> np.ndarray:
    """
    Convert (x_center, y_center, width, height) to (x_min, y_min, x_max, y_max).
    Accepts either a single sequence/array of 4 elements or 4 separate float arguments.
    Returns:
        np.ndarray: (x_min, y_min, x_max, y_max)
    """
    if len(args) == 1:
        arr = np.asarray(args[0], dtype=float)
        if arr.shape != (4,):
            raise ValueError("Input sequence/array must have 4 elements.")
        x, y, w, h = arr
    elif len(args) == 4:
        x, y, w, h = map(float, args)
    else:
        raise ValueError("Expected either a sequence/array of 4 elements or 4 separate arguments.")
    x_min = x - w / 2
    y_min = y - h / 2
    x_max = x + w / 2
    y_max = y + h / 2
    return np.array([x_min, y_min, x_max, y_max], dtype=float)

def xyxy2xywh(
    *args: Union[Sequence[float], np.ndarray, float]
) -> np.ndarray:
    """
    Convert (x_min, y_min, x_max, y_max) to (x_center, y_center, width, height).
    Accepts either a single sequence/array of 4 elements or 4 separate float arguments.
    Returns:
        np.ndarray: (x_center, y_center, width, height)
    """
    if len(args) == 1:
        arr = np.asarray(args[0], dtype=float)
        if arr.shape != (4,):
            raise ValueError("Input sequence/array must have 4 elements.")
        x_min, y_min, x_max, y_max = arr
    elif len(args) == 4:
        x_min, y_min, x_max, y_max = map(float, args)
    else:
        raise ValueError("Expected either a sequence/array of 4 elements or 4 separate arguments.")
    w = x_max - x_min
    h = y_max - y_min
    x = x_min + w / 2
    y = y_min + h / 2
    return np.array([x, y, w, h], dtype=float)

if __name__ == "__main__":
    # xywh2xyxy tests
    print(xywh2xyxy((2, 5, 4, 6)))                     # [0. 2. 4. 8.]
    print(xywh2xyxy(2, 5, 4, 6))                 # [0. 2. 4. 8.]
    print(xywh2xyxy(np.array((2, 5, 4, 6))))           # [0. 2. 4. 8.]
    # xyxy2xywh tests
    print(xyxy2xywh((0.0, 2.0, 4.0, 8.0)))             # [2. 5. 4. 6.]
    print(xyxy2xywh(0.0, 2.0, 4.0, 8.0))         # [2. 5. 4. 6.]
    print(xyxy2xywh(np.array((0.0, 2.0, 4.0, 8.0))))   # [2. 5. 4. 6.]