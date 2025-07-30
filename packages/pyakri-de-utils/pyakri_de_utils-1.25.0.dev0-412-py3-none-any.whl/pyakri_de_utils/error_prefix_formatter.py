import logging


class ErrorPrefixFormatter(logging.Formatter):
    def __init__(self, prefix, format, *args, **kwargs):
        super().__init__(*args, fmt=format, **kwargs)
        self.prefix = prefix

    def format(self, record):
        if record.levelno == logging.ERROR:
            record.msg = f"{self.prefix} {record.msg}"
        return super().format(record)
