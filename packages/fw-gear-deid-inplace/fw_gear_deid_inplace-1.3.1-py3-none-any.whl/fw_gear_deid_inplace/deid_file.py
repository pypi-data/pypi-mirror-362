"""Main module."""

import logging
import os
import tempfile
import typing as type
from pathlib import Path

from flywheel_migration import deidentify

from fw_gear_deid_inplace import utils

logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)


def inplace_deid_file(
    path_to_original_file: type.Union[str, Path],
    path_to_deid_profile: type.Union[str, Path],
) -> type.Union[None, Path]:
    """Runs in-place deidentification on a file.

    Args:
        path_to_original_file: the file to deidentify
        path_to_deid_profile: the profile to use

    Returns:
        0 if successful, >0 otherwise

    """
    log.debug("Processing file %s" % path_to_original_file)
    log.debug("loading profile %s" % path_to_deid_profile)
    deid_profile = deidentify.load_profile(path_to_deid_profile)

    # Some deid protocols delete the original input file in their cleanup,
    # which happens at garbage collection.  Sometimes garbage collection occurs
    # after I've replaced the original, and it deletes that file since they share
    # the same path.  This results in the loss of the deidentified AND the original.
    # To avoid this, we work on a symlink to the original file.
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the symbolic link in a tempdir - this is the only file that the deid
        # profile will be aware of.
        temp_input_directory = Path(temp_dir) / "input"
        temp_input_directory.mkdir(exist_ok=True)

        path_to_symlink_file = temp_input_directory / Path(path_to_original_file).name
        os.symlink(path_to_original_file, path_to_symlink_file)

        # Create our work dir to avoid file conflicts when the profile tries to save
        temp_output_directory = Path(temp_dir) / "deid_work"
        temp_output_directory.mkdir(exist_ok=True)
        try:
            # Try the deidentification.
            deid_path = utils.deidentify_file(
                deid_profile=deid_profile,
                file_path=str(path_to_symlink_file),
                output_directory=str(temp_output_directory),
            )
            if not deid_path:
                log.warning("No files were deidentified")
                return None
        except Exception:
            log.exception("Error deidentifying files, original will remain untouched")
            return None
        log.debug("Success")

        # Replace the original file with the deidentified file.
        output_file_path = utils.replace_file1_with_file2(
            replaced_file=Path(path_to_original_file),
            replacing_file=Path(deid_path),
        )

    return output_file_path
