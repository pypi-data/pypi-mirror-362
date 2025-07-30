from __future__ import annotations
import importlib, os, subprocess, sys, tempfile, time
from types import ModuleType
from importlib.metadata import version as pkg_ver, PackageNotFoundError
from packaging.version import parse as vparse
from contextlib import contextmanager

__all__ = ["__version__"]
__version__ = "0.4.0"

"""
A small shim that ensures the `dbx_hpexts` package (set the name in PACKAGE_NAME) is installed 
and returns that module—both within Databricks and locally—without exposing tokens in the code.
"""


PACKAGE_NAME      = "dbx_hpexts"                          
SECRET_SCOPE      = "si-prod-dataops-hpe"                           
SECRET_PAT_KEY    = "dbxdfexts-token"    
SECRET_REPO_KEY   = "dbxdfexts-url"                                                    
PIP_FLAGS      = ["--quiet", "--upgrade"]
ENV_REPO = "DBXDFEXTS_REPO"
ENV_REF  = "DBXDFEXTS_REF"
# ---------------------------------------------------------------------------

def _running_in_databricks() -> bool:
    return bool(os.getenv("DATABRICKS_RUNTIME_VERSION") or os.getenv("DB_IS_DRIVER"))

def _fetch_dbutils():
    try:
        import IPython
        return IPython.get_ipython().user_ns["dbutils"]          
    except Exception:                                            
        from pyspark.dbutils import DBUtils                      
        from pyspark.sql import SparkSession
        return DBUtils(SparkSession.builder.getOrCreate())

def _pip_install(uri: str):
    pkg = uri
    cmd = [sys.executable, "-m", "pip", "install", *PIP_FLAGS, pkg]
    subprocess.check_call(cmd)
    
def _build_repo_url() -> str:
    _ref = 'main'
    if _running_in_databricks():
        dbutils = _fetch_dbutils()
        base = dbutils.secrets.get(SECRET_SCOPE, SECRET_REPO_KEY)
        pat  = dbutils.secrets.get(SECRET_SCOPE, SECRET_PAT_KEY)
        return f"git+https://{pat}@{base}@{_ref}#egg={PACKAGE_NAME}"
    base = os.getenv(ENV_REPO)
    nref = os.getenv(ENV_REF)
    _ref = nref if nref is not None else _ref
    if base:
        return f"git+ssh://git@{base}@{_ref}#egg={PACKAGE_NAME}"
    return f"git+ssh://git@github.com/ORG/REPO.git#egg={PACKAGE_NAME}"                                

@contextmanager
def _file_lock(name: str, timeout: int = 180):
    lock = os.path.join(tempfile.gettempdir(), f"{name}.lock")
    start = time.time()
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            break
        except FileExistsError:
            if time.time() - start > timeout:
                raise TimeoutError("Timeout waiting for instalation lock.")
            time.sleep(1)
    try:
        yield
    finally:
        os.close(fd)
        os.remove(lock)


def _ensure_latest() -> ModuleType:
    uri = _build_repo_url()
    with _file_lock(PACKAGE_NAME):
        _pip_install(uri)

    if PACKAGE_NAME in sys.modules:
        mod = importlib.reload(sys.modules[PACKAGE_NAME])
    else:
        mod = importlib.import_module(PACKAGE_NAME)
    return mod

_pkg = _ensure_latest()

sys.modules[PACKAGE_NAME] = _pkg
sys.modules[__name__]     = _pkg     

globals().update(_pkg.__dict__)




