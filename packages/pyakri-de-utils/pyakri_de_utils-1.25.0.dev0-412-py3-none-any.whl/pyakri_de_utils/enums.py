from enum import Enum

from PIL import Image as PILImage
import cv2


class FilterTypes(Enum):
    Partitioner = "partitioner"
    Preprocessor = "preprocessor"
    Featurizer = "featurizer"
    DataIngest = "data_ingest"
    Thumbnail = "thumbnail"
    ThumbnailAggregator = "thumbnail_aggregator"


class DataType(Enum):
    """Supported Data types"""

    IMAGE = "image/*"
    VIDEO = "video/*"


class ResampleAlgoEnum(Enum):
    """
    Enum for resampling algorithms used by OpenCV.
    The values are compatible with OpenCV and Pillows' interpolation flags.
    """

    CUBIC = (PILImage.Resampling.BICUBIC, cv2.INTER_CUBIC)
    LINEAR = (PILImage.Resampling.BILINEAR, cv2.INTER_LINEAR)
    NEAREST = (PILImage.Resampling.NEAREST, cv2.INTER_NEAREST)
    LANCZOS = (PILImage.Resampling.LANCZOS, cv2.INTER_LANCZOS4)

    def __init__(self, pil: PILImage.Resampling, cv2_: int):
        self._pil = pil
        self._cv2 = cv2_

    @property
    def cv2(self):
        return self._cv2

    @property
    def pil(self):
        return self._pil


class FileTypeEnum(Enum):
    """
    Enum for supported file types.

    The values are used to determine the MIME type of files.
    """

    JPEG = ("JPEG", ".jpeg")
    PNG = ("PNG", ".png")

    def __init__(self, file_type: str, extension: str):
        self._file_type = file_type
        self._extension = extension

    @property
    def file_type(self):
        return self._file_type

    @property
    def extension(self):
        return self._extension
