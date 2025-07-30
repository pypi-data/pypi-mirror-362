from pyakri_de_utils.enums import FileTypeEnum
from pyakri_de_utils.enums import ResampleAlgoEnum


class Constants:
    DEFAULT_LOG_CONFIG_FILE_NAME = "pylogconf.yaml"

    AKRIDATA_LOG_PATH = "/var/log/akridata"

    DEFAULT_FILTER_INPUT_DIR = "/input/i1/"
    DEFAULT_FILTER_OUTPUT_DIR = "/output/o1/"

    DEFAULT_LOG_MODULE = "pyakri_de_filters"

    DEFAULT_THUMBNAIL_RESIZED_DIM = (192, 108)
    DEFAULT_THUMBNAIL_QUALITY = 95
    DEFAULT_THUMBNAIL_OUTPUT_FORMAT = FileTypeEnum.JPEG
    DEFAULT_THUMBNAIL_RESAMPLE_ALGO = ResampleAlgoEnum.LANCZOS

    FEATURIZER_DEFAULT_RESIZED_DIM = (224, 224)
    FEATURIZER_PROCESS_BATCH_SIZE = 256

    PRE_PROCESSOR_BATCH_SIZE = 1
