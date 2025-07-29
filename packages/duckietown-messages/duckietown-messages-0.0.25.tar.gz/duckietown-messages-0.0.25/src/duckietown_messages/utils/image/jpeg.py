import io
import warnings
from abc import ABC, abstractmethod
from typing import Type, List

import numpy as np

from duckietown_messages.utils.image.pil import pil_to_np


class JPEGEngineAbs(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def encode(self, im: np.ndarray) -> bytes:
        pass

    @abstractmethod
    def decode(self, im: bytes) -> np.ndarray:
        pass


class TurboJPEGEngine(JPEGEngineAbs):

    def __init__(self):
        from turbojpeg import TurboJPEG
        self.engine = TurboJPEG()

    @property
    def name(self) -> str:
        return "turbojpeg"

    def encode(self, im: np.ndarray) -> bytes:
        return self.engine.encode(im)

    def decode(self, im: bytes) -> np.ndarray:
        return self.engine.decode(im)


class PillowJPEGEngine(JPEGEngineAbs):

    def __init__(self):
        from PIL import Image
        self.Image: Type[Image] = Image

    @property
    def name(self) -> str:
        return "Pillow"

    def encode(self, im: np.ndarray) -> bytes:
        # convert numpy to Image
        im = self.Image.fromarray(im)
        # export as JPEG bytes
        buffer = io.BytesIO()
        im.save(buffer, format='JPEG')
        return buffer.getvalue()

    def decode(self, im: bytes) -> np.ndarray:
        # convert bytes to stream (file-like object in memory)
        buffer = io.BytesIO(im)
        # create Image object
        image = self.Image.open(buffer)
        # convert to numpy
        return pil_to_np(image)


class JPEG:
    __engines: List[Type[JPEGEngineAbs]] = [
        TurboJPEGEngine,
        PillowJPEGEngine,
    ]
    engine: JPEGEngineAbs = None

    @classmethod
    def init(cls):
        if cls.engine is None:
            for engine in cls.__engines:
                try:
                    cls.engine = engine()
                    break
                except (ImportError, RuntimeError):
                    warnings.warn(f"JPEG engine '{engine.__name__}' not available. Expect lower performance.")
                    pass
            # if no engine was found
            if cls.engine is None:
                raise RuntimeError("No JPEG engine available.")


def rgb_to_jpeg(im: np.ndarray) -> bytes:
    JPEG.init()
    return JPEG.engine.encode(im)


def jpeg_to_rgb(im: bytes) -> np.ndarray:
    JPEG.init()
    return JPEG.engine.decode(im)


__all__ = [
    'rgb_to_jpeg',
    'jpeg_to_rgb',
]
