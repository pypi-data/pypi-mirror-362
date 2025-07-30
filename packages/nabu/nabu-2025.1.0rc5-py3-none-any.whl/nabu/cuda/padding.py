from ..processing.padding_cuda import *  # noqa: F403
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.cuda.padding has been moved to nabu.processing.padding_cuda", do_print=True, func_name="padding_cuda"
)
