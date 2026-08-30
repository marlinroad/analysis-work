# -----------------------------------------------------------------------------
# Enable autoreload in any IPython/interactive session — ONE-TIME, package-wide
from IPython import get_ipython
try:
    ip = get_ipython()
    ip.run_line_magic("load_ext", "autoreload")
    ip.run_line_magic("autoreload", "2")
except Exception:
    # not running in IPython (plain script), or autoreload not installed
    pass