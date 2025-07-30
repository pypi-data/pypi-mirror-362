from wimlib._global import *
import wimlib.file as file
import wimlib.image as image
import wimlib.info as info
import wimlib.compression as compression
from wimlib.error import WIMError
import atexit as _atexit
from wimlib.backend import WIMBackend as _WIMBackend

__version__ = "0.0.0"

_backend = _WIMBackend()
ENCODING = _backend.encoding


_atexit.register(global_cleanup)
