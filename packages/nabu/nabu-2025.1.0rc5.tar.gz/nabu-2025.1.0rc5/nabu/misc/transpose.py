from ..processing.transpose import *  # noqa: F403
from ..utils import deprecation_warning

deprecation_warning(
    "nabu.misc.transpose has been moved to nabu.processing.transpose", do_print=True, func_name="transpose"
)
