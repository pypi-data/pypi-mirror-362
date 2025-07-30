import os
import sys
import shutil
from contextlib import suppress
from pathlib import Path
from typing import Tuple, Optional

import cv2
import exif
import numpy as np
from exif import Image as ImageExif
import pydicom
from filetype import filetype
from filetype.types import image as ImageTypes
from PIL import Image as PILImage
from plum.exceptions import UnpackError

from pyakri_de_utils import logger
from pydicom.errors import InvalidDicomError

from pyakri_de_utils.enums import ResampleAlgoEnum, FileTypeEnum

MIN_THUMBNAIL_DIM = 108
MAX_THUMBNAIL_DIM = 324
THUMBNAIL_DIM_PCT = 0.15


class ImgReadError(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return f"AKRI_ERROR: {self._msg}"


class ImgFormatUnknownError(ImgReadError):
    pass


def image_exception_handler(func):
    def meth(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ImgFormatUnknownError as ex:
            logger.debug(f"Unknown image format {ex}")
            raise ex
        except Exception as ex:
            logger.debug(f"Error reading image file {ex}")
            raise ImgReadError(f"Error Reading image {str(ex)}")

    return meth


class ImageUtils:
    @classmethod
    def default_read(cls, file_path: Path) -> np.ndarray:
        """
        Reads an image file using OpenCV.

        This function reads an image file using OpenCV and handles rotation
        based on the image's Exif orientation flag. It returns the image as a
        numpy array.

        Parameters:
            file_path (Path): The path to the image file.

        Returns:
            np.ndarray: The image as a numpy array.
        """
        try:

            def rotate_image(img_np):
                img = None
                with suppress(UnpackError):
                    img = ImageExif(str(file_path))
                if img and img.has_exif:
                    orientation: int = img.get(
                        "orientation", exif.Orientation.TOP_LEFT
                    ).value
                    if orientation == 3:
                        logger.info(f"Rotating image {file_path} by 180 degrees")
                        img_np = cv2.rotate(img_np, cv2.ROTATE_180)
                    elif orientation == 6:
                        logger.info(
                            f"Rotating image {file_path} by 90 degrees counter clockwise"
                        )
                        img_np = cv2.rotate(img_np, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    elif orientation == 8:
                        logger.info(
                            f"Rotating image {file_path} by 90 degrees clockwise"
                        )
                        img_np = cv2.rotate(img_np, cv2.ROTATE_90_CLOCKWISE)
                return img_np

            img = cv2.imread(str(file_path))
            if img is None:
                raise ImgFormatUnknownError(f"File {file_path} format not supported")
            # Rotate the image based on the orientation if required
            img = rotate_image(img)
            return img
        except Exception as ex:
            raise ImgReadError(str(ex))

    @classmethod
    def sequence_read(cls, file_path: Path):
        """
        Reads an image sequence using OpenCV.

        This function reads an image sequence using OpenCV and returns the
        first frame as a numpy array.

        Parameters:
            file_path (Path): The path to the image sequence.

        Returns:
            np.ndarray: The first frame as a numpy array.
        """
        try:
            cap = cv2.VideoCapture(str(file_path))
            ret, frame = cap.read()
            if not ret:
                raise ImgFormatUnknownError(f"File {str(file_path)} can't be read")
            return frame
        except Exception as ex:
            raise ImgReadError(str(ex))

    @classmethod
    def dicom_read(cls, file_path: Path) -> np.ndarray:
        try:
            # Read the dcm file
            dcm_img = pydicom.dcmread(file_path)

            # If no image data, then treat the file as corrupted file to skip processing
            if "PixelData" not in dcm_img:
                logger.info(f"No pixel data in {file_path}")
                raise ImgReadError(f"Not dicom image file {file_path}")
            img = dcm_img.pixel_array.astype(float)

            # Fetch the 1st frame if there are more than 1 frames
            if dcm_img.get("NumberOfFrames", 1) > 1:
                img = img[0, :, :]

            # scale Image
            scaled_img = (
                (img - np.min(img)) / (np.max(img) - np.min(img)) * 255
            ).astype(np.uint8)

            return scaled_img
        except InvalidDicomError as ex:
            raise ImgFormatUnknownError(str(ex))
        except Exception as ex:
            raise ImgReadError(str(ex))

    @staticmethod
    def get_image_from_file(file: Path) -> np.ndarray:
        """
        Reads an image from a file path.

        This function determines the type of the image file based on the file's
        MIME type. It supports DICOM and GIF files. For other file types, it
        falls back to the default image reader.

        Parameters:
            file (Path): The path of the file to read.

        Returns:
            numpy.ndarray: The image data as a NumPy array.
        """
        file_type = filetype.guess(file)
        if file_type:
            file_type_mime = file_type.mime
            if file_type_mime == ImageTypes.Dcm.MIME:
                return ImageUtils.dicom_read(file)
            elif file_type_mime == ImageTypes.Gif.MIME:
                return ImageUtils.sequence_read(file)
        return ImageUtils.default_read(file)

    @classmethod
    def is_image_corrupted(cls, file: Path) -> bool:
        """
        Checks if an image file is corrupted.

        Parameters:
            file (Path): The path of the image file to check.

        Returns:
            bool: True if the image file is corrupted, False otherwise.
        """
        try:
            cls.get_image_from_file(file)
            return False
        except Exception as e:
            logger.info(
                "Failure in is_image_corrupted for file:%s with error %r", file, e
            )
            return True

    @classmethod
    def get_image_size(cls, file: Path) -> Optional[Tuple[int, int]]:
        """
        Returns the size of an image file.

        Parameters:
            file (Path): The path of the image file to check.

        Returns:
            Optional[Tuple[int, int]]: The size of the image file as a tuple
            (width, height).
        """
        try:

            img = cls.get_image_from_file(file)
            return img.shape[1], img.shape[0]
        except Exception as e:
            logger.info("Failure in get_image_size for file:%s with error %r", file, e)
            return None

    @classmethod
    @image_exception_handler
    def get_image_thumbnail(
        cls,
        file: Path,
        resize_dim: Tuple[int, int],
        resample_algo: ResampleAlgoEnum = ResampleAlgoEnum.LANCZOS,
    ) -> np.ndarray:
        """
        Generate a thumbnail image from a given image file.

        The function generates a thumbnail image from the given image file. It takes
        the image file path, the desired thumbnail size, and the resampling algorithm as
        parameters. The function preserves the aspect ratio of the original image.
        If desired size is -1 or dynamic, then below is applied
        1. Find the shortest edge(height or width) in the input image.
        2. Set the shortest edge of the thumbnail to 15% of the input image
           width with some minimum value(108 pixels) and maximum value(324 pixels)
        3. Set the longest edge of the thumbnail based on above calculation
           with aspect ratio preserved.

        Parameters:
            file (Path): The path of the image file.
            resize_dim (Tuple[int, int]): The desired thumbnail size. -1 indicates dynamic size
            resample_algo (ResampleAlgoEnum, optional): The resampling algorithm to
                use. Defaults to ResampleAlgoEnum.LANCZOS.

        Returns:
            np.ndarray: The thumbnail image as a NumPy array.
        """

        img = cls.get_image_from_file(file)
        img = PILImage.fromarray(img)

        # Dynamically compute the resize dim if requested
        if resize_dim[0] == -1 or resize_dim[1] == -1:
            w, h = img.size
            shortest_edge = min(w, h)
            shortest_edge = shortest_edge * THUMBNAIL_DIM_PCT
            shortest_edge = min(shortest_edge, MAX_THUMBNAIL_DIM)
            shortest_edge = max(shortest_edge, MIN_THUMBNAIL_DIM)
            if w < h:
                resize_dim = (shortest_edge, sys.maxsize)
            else:
                resize_dim = (sys.maxsize, shortest_edge)

        img.thumbnail(resize_dim, resample=resample_algo.pil)
        return np.array(img)

    @staticmethod
    @image_exception_handler
    def convert_image_to_grayscale(img: np.ndarray) -> np.ndarray:
        """
        Convert an RGB image to grayscale.

        This function converts an RGB image to grayscale. It takes an RGB image as
        input and returns a grayscale image.

        Parameters:
            img (np.ndarray): The RGB image to be converted to grayscale.

        Returns:
            np.ndarray: The grayscale image.
        """
        if len(img.shape) == 2:
            # already a grayscale image
            return img
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    @image_exception_handler
    def convert_image_to_rgb(img: np.ndarray) -> np.ndarray:
        """
        Convert an image to RGB.

        This function converts an image to RGB. It takes an image as input and
        returns an RGB image. Depending on the input image, it can
        convert a gray scale image or a BGR image to an RGB image.
        Note: this function does not know the actual channel color of the input image

        Parameters:
            img (np.ndarray): The image to be converted to RGB.

        Returns:
            np.ndarray: The RGB image.
        """
        if len(img.shape) == 2:
            return cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    @staticmethod
    @image_exception_handler
    def save(file_path: Path, image: np.ndarray, output_format: FileTypeEnum):
        """
        Save an image to a file.

        This function saves an image to a file. It takes the path of the file to
        save, the image data, and the output format of the image. The function
        preserves the filename extension provided by the user.

        Parameters:
            file_path (Path): The path of the file to save the image.
            image (np.ndarray): The image data to be saved.
            output_format (FileTypeEnum): The format of the output image.

        """
        file_name, file_extn = os.path.splitext(str(file_path))
        target_file = file_name + file_extn.replace(".", "_") + output_format.extension
        cv2.imwrite(str(target_file), image)
        # revert back the extension in which users want to write the image
        if target_file != file_path:
            shutil.move(target_file, file_path)

    @staticmethod
    @image_exception_handler
    def resize(
        img: np.ndarray,
        resize_dim: Tuple[int, int],
        resample_algo: ResampleAlgoEnum = ResampleAlgoEnum.CUBIC,
        flatten_img=False,
    ) -> np.ndarray:
        """
        Resize an image.

        This function resizes an image to a given dimension. It takes the image
        to be resized, the desired dimension, and the resampling algorithm. The
        function also allows the user to decide whether to flatten the image
        or not.

        Parameters:
            img (np.ndarray): The image to be resized.
            resize_dim (Tuple[int, int]): The desired dimension of the resized
                image.
            resample_algo (ResampleAlgoEnum): The resampling algorithm to use.
                Defaults to ResampleAlgoEnum.CUBIC.
            flatten_img (bool): Whether to flatten the image or not. Defaults to
                False.

        Returns:
            np.ndarray: The resized image. If flatten_img is True, the image is
                flattened and the pixel values are normalized between 0 and 1.
                Otherwise, the image is returned as is.
        """
        im_np = cv2.resize(img, resize_dim, interpolation=resample_algo.cv2)
        if flatten_img:
            im_arr = im_np.flatten()
            im_arr = im_arr / 255
            return im_arr

        return im_np
