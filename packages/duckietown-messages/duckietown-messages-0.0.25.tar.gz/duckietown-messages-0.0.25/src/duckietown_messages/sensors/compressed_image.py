from typing import Literal

import numpy as np
from pydantic import Field

from ..base import BaseMessage
from ..standard.header import Header, AUTO
from ..utils.image.jpeg import rgb_to_jpeg, jpeg_to_rgb


class CompressedImage(BaseMessage):
    # header
    header: Header = AUTO

    # format of the image
    #   valid values are:
    #    - "jpeg"
    #    - "png"
    format: Literal["jpeg", "png"] = Field(description="The format of the image data")

    # compressed data buffer
    data: bytes = Field(description="The compressed image data")

    @classmethod
    def from_rgb(cls, im: np.ndarray, encoding: Literal["jpeg", "png"], header: Header) -> 'CompressedImage':
        msg = CompressedImage(
            header=header,
            format=encoding,
            data=rgb_to_jpeg(im),
        )
        # ---
        return msg

    def as_array(self) -> np.ndarray:
        # TODO: implement PNG
        assert self.format == "jpeg"
        return jpeg_to_rgb(self.data)

    def to_rgb(self) -> np.ndarray:
        im: np.ndarray = self.as_array()
        _, _, c, *_ = im.shape + (1,)
        assert c == 3
        return im

    def to_mono8(self) -> np.ndarray:
        im: np.ndarray = self.as_array()
        h, w, c, *_ = im.shape + (1,)
        assert c == 1
        return im.reshape((h, w))
