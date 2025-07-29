from ..processing.fft_opencl import *  # noqa: F403
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.opencl.fft has been moved to nabu.processing.fft_opencl", do_print=True, func_name="fft_opencl"
)
