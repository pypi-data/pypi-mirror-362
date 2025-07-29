from ..processing.histogram_cuda import *  # noqa: F403
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.misc.histogram_cuda has been moved to nabu.processing.histogram_cuda",
    do_print=True,
    func_name="histogram_cuda",
)
