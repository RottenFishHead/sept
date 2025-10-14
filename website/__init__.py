from .base import *
import os

if os.environ.get("mod") == "production":
    from .prod import *
else:
    from .dev import *