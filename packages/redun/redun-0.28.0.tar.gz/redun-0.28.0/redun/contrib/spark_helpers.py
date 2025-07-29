"""
Decorators that make libraries available to glue jobs.
"""

import importlib
import os
import site
import time
import zipfile

import s3fs

RDKIT_ZIP_LOCATION = "s3://insitro-user-robin/glue_scripts/rdkit_full_env.zip"


def enable_rdkit(zipfile: str = RDKIT_ZIP_LOCATION) -> None:
    """
    Installs the rdkit "binary zipfile" to user's site packages.
    Safe to call from Spark workers: will install on individual node
    and is thread and process safe.

    This CANNOT be a decorator as decorators aren't picklable and
    you might want to use rdkit in a Spark UDF, etc, which is pickled.
    """
    try:
        from rdkit import Chem  # noqa: F401

    except (ImportError, ModuleNotFoundError):
        print("Installing zipped module")
        install_zipped_module(zipfile)


def install_zipped_module(s3_path: str) -> None:
    """
    Installs a zip file from S3 to user's site packages.
    Thread and process safe- can be called from Spark.
    """

    # Try to get the "unzip lock"
    lockfile = os.path.join(str(site.USER_BASE), ".unzip_lock")
    try:
        lock_fd = os.open(lockfile, os.O_CREAT | os.O_EXCL)

        # Download the module from S3.
        s3 = s3fs.S3FileSystem()
        local_fn = "./tmp_zipmod.zip"
        s3.get(s3_path, local_fn)
        print("Downloaded zipfile")

        # Unpack the module to site packages.
        with zipfile.ZipFile(local_fn, mode="r") as zf:
            zf.extractall(site.USER_BASE)
        print("Extracted zipfile")

        # Release lock
        os.close(lock_fd)
        os.remove(lockfile)

    # If someone else has the lock, wait for them to install the module.
    except FileExistsError:
        while os.path.exists(lockfile):
            time.sleep(1.0)

    importlib.invalidate_caches()
