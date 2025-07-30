from __future__ import annotations

import os
from contextlib import suppress
from typing import List

from numba import cuda
from pyakri_de_utils import logger

try:
    import onnxruntime

    # 0:Verbose, 1:Info, 2:Warning, 3:Error, 4:Fatal
    onnxruntime.set_default_logger_severity(
        int(os.getenv("ONNXRUNTIME_DEFAULT_LOG_LEVEL", "3"))
    )
except ImportError:
    logger.warning("onnxruntime package missing, some functionalities may not work")

DEVICE_TYPE = "cpu"
with suppress(cuda.cudadrv.error.CudaSupportError):
    DEVICE_TYPE = "cuda" if (len(cuda.gpus) > 0) else "cpu"


def get_onnx_session(
    onnx_model: str | bytes | os.PathLike,
    providers: List[str] = None,
    gpu_mem_fraction: str = None,
) -> onnxruntime.InferenceSession:
    if not providers:
        providers = ["CPUExecutionProvider"]
        if DEVICE_TYPE == "cuda":
            if "CUDAExecutionProvider" in onnxruntime.get_available_providers():
                providers = ["CUDAExecutionProvider"]
            else:
                logger.warning(
                    "Detected device type as cuda but onnxruntime-gpu is not installed"
                )
    logger.debug(
        f"Using providers {providers} for device type: {DEVICE_TYPE}, with gpu_mem_fraction: {gpu_mem_fraction}"
    )
    session = onnxruntime.InferenceSession(onnx_model, providers=providers)
    option = session.get_provider_options().get("CUDAExecutionProvider")
    if option:
        # setting gpu memory fraction
        gpu_mem_fraction = float(gpu_mem_fraction) if gpu_mem_fraction else 0.95
        new_mem_limit = int(
            int(cuda.current_context().get_memory_info().total) * gpu_mem_fraction
        )
        option["gpu_mem_limit"] = new_mem_limit
        session.set_providers(["CUDAExecutionProvider"], [option])
    return session
