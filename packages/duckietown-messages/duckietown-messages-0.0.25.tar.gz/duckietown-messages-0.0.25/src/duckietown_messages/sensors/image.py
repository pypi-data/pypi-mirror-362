import dataclasses
from typing import Callable, Dict, Literal

import numpy as np
from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO
from ..utils.image.pil import np_to_pil, pil_to_np


@dataclasses.dataclass
class ImageEncoding:
    pil_encoding: str
    num_channels: int
    channel_size_bits: int = 8
    order: Callable[[np.ndarray], np.ndarray] = lambda i: i
    unpack: Callable[[np.ndarray], np.ndarray] = lambda i: i
    pack: Callable[[np.ndarray], np.ndarray] = lambda i: i


SUPPORTED_ENCODINGS: Dict[str, ImageEncoding] = {
    "rgb8": ImageEncoding("RGB",
                          num_channels=3),
    "rgba8": ImageEncoding("RGBA",
                           num_channels=4),
    "bgr8": ImageEncoding("RGB",
                          num_channels=3,
                          order=lambda i: np.transpose(i, (2, 1, 0))),
    "bgra8": ImageEncoding("RGBA",
                           num_channels=4,
                           order=lambda i: np.transpose(i, (2, 1, 0, 3))),
    "mono1": ImageEncoding("L",
                           num_channels=1,
                           channel_size_bits=1,
                           unpack=lambda i: np.unpackbits(i).astype(np.uint8),
                           pack=lambda b: np.packbits(b)),
    "mono8": ImageEncoding("L",
                           num_channels=1)
}


class Image(BaseMessage):
    # header
    header: Header = AUTO

    # image width, that is, number of columns
    width: int = Field(description="Width of the image", ge=0)

    # image height, that is, number of rows
    height: int = Field(description="Height of the image", ge=0)

    # encoding of pixels: channel meaning, ordering, and size
    #   valid values are:
    #    - "rgb8"
    #    - "rgba8"
    #    - "bgr8"
    #    - "bgra8"
    #    - "mono1"
    #    - "mono8"
    #    - "mono16"
    encoding: Literal["rgb8", "rgba8", "bgr8", "bgra8", "mono1", "mono8", "mono16"] = \
        Field(description="The encoding of the pixels")

    # length of a full row in bytes
    step: int = Field(description="Full row length in bytes", ge=0)

    # actual data, size is (step * rows)
    data: bytes = Field(description="Pixel data. Size must be (step * rows)")

    # is this data bigendian?
    is_bigendian: bool = Field(description="Is the data bigendian?")

    @classmethod
    def from_np(cls,
                im: np.ndarray,
                encoding: Literal["rgb8", "rgba8", "bgr8", "bgra8", "mono1", "mono8", "mono16"],
                header: Header = None) -> 'Image':
        assert encoding in SUPPORTED_ENCODINGS
        encoder: ImageEncoding = SUPPORTED_ENCODINGS[encoding]
        h, w, c, *_ = im.shape + (1,)
        msg = Image(
            header=header or Header(),
            width=w,
            height=h,
            encoding=encoding,
            step=w * c * int(encoder.channel_size_bits / 8),
            data=encoder.pack(im).tobytes(),
            # TODO: this always True?
            is_bigendian=False
        )
        # ---
        return msg

    @classmethod
    def from_rgb(cls, im: np.ndarray, header: Header = None) -> 'Image':
        # validate image shape and number of channels
        assert len(im.shape) == 3 and im.shape[2] == 3
        # ---
        return cls.from_np(im, "rgb8", header)

    @classmethod
    def from_rgba(cls, im: np.ndarray, header: Header = None) -> 'Image':
        # validate image shape and number of channels
        assert len(im.shape) == 3 and im.shape[2] == 4
        # ---
        return cls.from_np(im, "rgba8", header)

    @classmethod
    def from_mono8(cls, im: np.ndarray, header: Header = None) -> 'Image':
        # validate image shape
        assert len(im.shape) == 2
        # ---
        return cls.from_np(im, "mono8", header)

    @classmethod
    def from_mono1(cls, im: np.ndarray, header: Header = None) -> 'Image':
        # validate image shape
        assert len(im.shape) == 2
        # convert mono8 to mono1
        im = (im > 125).astype(np.uint8)
        # ---
        return cls.from_np(im, "mono1", header)

    def as_array(self) -> np.ndarray:
        # get image encoder
        if self.encoding not in SUPPORTED_ENCODINGS:
            raise ValueError(f"Image encoding '{self.encoding}' not supported.")
        encoder: ImageEncoding = SUPPORTED_ENCODINGS[self.encoding]
        # get image shape
        if self.encoding == "mono1":
            w, h, c = (self.width, self.height, 1)
        else:
            w, h, c = (self.width, self.height, int(self.step / (self.width * (encoder.channel_size_bits / 8))))
        # validate number of channel
        assert c == encoder.num_channels, "Number of channels does not match the encoding. Expected %d, got %d." % (
            encoder.num_channels, c)
        # turn bytes into array
        im = np.frombuffer(self.data, dtype=np.uint8)
        # unpack data
        im = encoder.unpack(im)
        # shape array
        im = im.reshape((h, w, c)) if c > 1 else im.reshape((h, w))
        # reorder channels
        im = encoder.order(im)
        # color space conversion
        im = np_to_pil(im, mode=encoder.pil_encoding)
        # go back to numpy
        im = pil_to_np(im)
        # ---
        return im

    def as_rgb(self) -> np.ndarray:
        # validate encoding
        assert self.encoding == "rgb8"
        # ---
        return self.as_array()

    def as_rgba(self) -> np.ndarray:
        # validate encoding
        assert self.encoding == "rgba8"
        # ---
        return self.as_array()

    def as_mono8(self) -> np.ndarray:
        # validate encoding
        assert self.encoding in ["mono1", "mono8"]
        # get np array
        im = self.as_array()
        # turn mono1 into mono8
        if self.encoding == "mono1":
            im *= 255
        # ---
        return im

    def as_mono1(self) -> np.ndarray:
        # validate encoding
        assert self.encoding == "mono1"
        # convert mono8 to mono1
        im = self.as_array()
        im = pil_to_np(np_to_pil(im).convert("1"))
        # ---
        return im
