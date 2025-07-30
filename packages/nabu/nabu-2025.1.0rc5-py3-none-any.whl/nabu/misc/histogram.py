from ..processing.histogram import *  # noqa: F403
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.misc.histogram has been moved to nabu.processing.histogram", do_print=True, func_name="histogram"
)
