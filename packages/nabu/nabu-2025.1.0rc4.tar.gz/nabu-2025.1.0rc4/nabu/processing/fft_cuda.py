import os
import warnings
from functools import lru_cache
from multiprocessing import get_context
from multiprocessing.pool import Pool
from ..utils import BaseClassError, check_supported, no_decorator
from .fft_base import _BaseVKFFT

try:
    from pyvkfft.cuda import VkFFTApp as CudaVkFFTApp

    __has_vkfft__ = True
except (ImportError, OSError):
    __has_vkfft__ = False
    CudaVkFFTApp = BaseClassError
from ..cuda.processing import CudaProcessing

n_cached_ffts = int(os.getenv("NABU_FFT_CACHE", "0"))


maybe_cached = lru_cache(maxsize=n_cached_ffts) if n_cached_ffts > 0 else no_decorator


@maybe_cached
def _get_vkfft_cuda(*args, **kwargs):
    return CudaVkFFTApp(*args, **kwargs)


def get_vkfft_cuda(slf, *args, **kwargs):
    return _get_vkfft_cuda(*args, **kwargs)


class VKCUFFT(_BaseVKFFT):
    """
    Cuda FFT, using VKFFT backend
    """

    implem = "vkfft"
    backend = "cuda"
    ProcessingCls = CudaProcessing
    get_fft_obj = get_vkfft_cuda

    def _init_backend(self, backend_options):
        super()._init_backend(backend_options)
        self._vkfft_other_init_kwargs = {"stream": self.processing.stream}


def _has_vkfft(x):
    # should be run from within a Process
    try:
        from nabu.processing.fft_cuda import VKCUFFT, __has_vkfft__

        if not __has_vkfft__:
            return False
        _ = VKCUFFT((16,), "f")
        avail = True
    except (ImportError, RuntimeError, OSError, NameError):
        avail = False
    return avail


@lru_cache(maxsize=2)
def has_vkfft(safe=True):
    """
    Determine whether pyvkfft is available.
    For Cuda GPUs, vkfft relies on nvrtc which supports a narrow range of Cuda devices.
    Unfortunately, it's not possible to determine whether vkfft is available before creating a Cuda context.
    So we create a process (from scratch, i.e no fork), do the test within, and exit.
    This function cannot be tested from a notebook/console, a proper entry point has to be created (if __name__ == "__main__").
    """
    if not safe:
        return _has_vkfft(None)
    try:
        ctx = get_context("spawn")
        with Pool(1, context=ctx) as p:
            v = p.map(_has_vkfft, [1])[0]
    except AssertionError:
        # Can get AssertionError: daemonic processes are not allowed to have children
        # if the calling code is already a subprocess
        return _has_vkfft(None)
    return v


@lru_cache(maxsize=2)
def get_fft_class(backend="vkfft"):
    backends = {
        "vkfft": VKCUFFT,
        "pyvkfft": VKCUFFT,
    }

    def get_fft_cls(asked_fft_backend):
        asked_fft_backend = asked_fft_backend.lower()
        check_supported(asked_fft_backend, list(backends.keys()), "Cuda FFT backend name")
        return backends[asked_fft_backend]

    asked_fft_backend_env = os.environ.get("NABU_FFT_BACKEND", "")
    if asked_fft_backend_env != "":
        return get_fft_cls(asked_fft_backend_env)

    avail_fft_implems = get_available_fft_implems()
    if len(avail_fft_implems) == 0:
        raise RuntimeError("Could not any Cuda FFT implementation. Please install pyvkfft")
    if backend not in avail_fft_implems:
        warnings.warn("Could not get FFT backend '%s'" % backend, RuntimeWarning)
        backend = avail_fft_implems[0]

    return get_fft_cls(backend)


@lru_cache(maxsize=1)
def get_available_fft_implems():
    avail_implems = []
    if has_vkfft(safe=True):
        avail_implems.append("vkfft")
    return avail_implems
