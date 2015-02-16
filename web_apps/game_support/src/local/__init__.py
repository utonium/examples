# In case there are other code directories that scope modules under
# the 'local' namespace, have this extend that namespace.
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
