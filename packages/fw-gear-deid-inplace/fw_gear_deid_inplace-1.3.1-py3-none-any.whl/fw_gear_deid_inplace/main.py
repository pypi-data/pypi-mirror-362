"""Main module."""

import logging
import os
import shutil
import typing as type
from pathlib import Path

import flywheel
from fw_gear_deid_export.container_export import load_template_dict
from fw_gear_deid_export.metadata_export import get_deid_fw_container_metadata

from fw_gear_deid_inplace import deid_file, utils
from fw_gear_deid_inplace.utils import RunConfig

logging.basicConfig(level="DEBUG")
log = logging.getLogger(__name__)


def deid_metadata(
    client: flywheel.Client, input_file_id: str, deid_profile_path: str
) -> dict:
    """deid flywheel file metadata if the deid profile has a "flywheel" section

    Args:
        client: the flywheel sdk client
        input_file_id: the file_id of the file to deidentify
        deid_profile_path: the path to the deid profile

    Returns:
        dict: the deidentified metadata

    """

    # The deid export gear heavily couples the deidentifaction with the export process
    # so we can't just copy the methods exactly.  Here are the key actions
    # 1. Load the deid profile
    deid_profile = load_template_dict(deid_profile_path)
    # 2. Extrac the flywheel section
    fw_metadata_profile = deid_profile.get("flywheel", None)
    if fw_metadata_profile is None:
        return {}
    # 3. Extract the "file" section
    config = fw_metadata_profile.get("file", {})
    fw_file = client.get_file(input_file_id)
    # 4. call the method from the deid export gear that does the work.
    metadata = get_deid_fw_container_metadata(
        client=client, config=config, container=fw_file
    )
    # 5. the deid export gear adds an "export" seciton to the metadata that we don't want.
    metadata["info"].pop("export")
    return metadata


def process_output(  # noqa: PLR0913
    client: flywheel.Client,
    output_file_path: type.Union[Path, None],
    input_file_id: str,
    output_dir: Path,
    delete_original: bool = True,
    delete_reason: str = None,
) -> int:
    """Upload using the more reliable engine upload OR the SDK upload.

    Depending on the original file location and the gear's destination, use the
    appropriate method to get the file to the right place.

    Args:
        client: the flywheel sdk client.
        output_file_path: the path to the output file that will be uploaded.
        input_file_id: the file_id of the original file to be replaced.
        output_dir: the output directory recognized by the flywheel engine.
        delete_original: If true, delete the original flywheel file

    Returns:
        int: 0 if successful, >0 otherwise.

        1 = output file does not exist
        2 = engine upload failed when trying to move file to output folder
        3 = engine upload failed when trying to delete original file from flywheel

    """

    log.debug("processing output")
    if output_file_path is None:
        log.warning("No files were deinidentified")
        return 1
    if not os.path.isfile(output_file_path):
        log.warning(
            "Output file %s does not exist, Deid unsuccessful" % output_file_path
        )
        return 1

    try:
        move_file_to_output(output_file_path, output_dir)
    except Exception as e:
        log.exception(e)
        return 2

    if not delete_original:
        return 0

    try:
        delete_flywheel_file(client, input_file_id, delete_reason)
    except Exception as e:
        log.exception(e)
        return 3

    return 0


def delete_flywheel_file(client: flywheel.Client, file_id: str, delete_reason: str):
    """Deletes a file from flywheel

    Args:
        client: the flywheel sdk client
        file_id: the flywheel file ID to delete

    Returns:
        None

    """
    if delete_reason is not None:
        delete_reason = flywheel.models.container_delete_reason.ContainerDeleteReason(
            delete_reason
        )
        client.delete_file(file_id=file_id, delete_reason=delete_reason)
    else:
        client.delete_file(file_id=file_id)


def move_file_to_output(output_file_path: Path, output_dir: Path):
    """to minimize api calls, move the output file to the "output" directory
    and allow the engine to perform the uplaod.

    Returns: None

    """

    new_output_path = output_dir / output_file_path.name
    log.debug("moving file %s to %s" % (str(output_file_path), str(new_output_path)))
    shutil.move(output_file_path, new_output_path)
    log.debug("success")


def run(
    client: flywheel.Client,
    flywheel_file_id: str,
    path_to_file: os.PathLike,
    path_to_deid_profile: os.PathLike,
    run_config: RunConfig,
) -> type.Union[None, Path]:
    """Runs the main deidentify inplace workflow.

    Returns:
        [type]: [description]
    """

    output_dir = run_config.output_dir
    delete_original = run_config.delete_original
    delete_reason = run_config.delete_reason
    output_file_metadata = None
    output_file_path = None
    e_code = 0

    # Validate the input path
    utils.validate_path(Path(path_to_deid_profile))
    utils.validate_deletion_reason(delete_reason)

    try:
        # Deidentify the file.
        output_file_path = deid_file.inplace_deid_file(
            path_to_file, path_to_deid_profile
        )
        output_file_metadata = deid_metadata(
            client, flywheel_file_id, path_to_deid_profile
        )

    except Exception as e:
        log.exception(e)
        # if we failed here, the deidentification didn't work for some reason.
        # we will tag the original file with a fail tag.
        output_file_path = None

    try:
        e_code = process_output(
            client,
            output_file_path,
            flywheel_file_id,
            output_dir,
            delete_original,
            delete_reason,
        )
    except Exception as e:
        log.exception(e)
        # if we failed here, the final upload/deletion of the original file didn't work.
        # That information will be captured in the exception logging.
        # The important thing is to tag the original file, not the target file.
        output_file_path = path_to_file

    return output_file_path, output_file_metadata, e_code
