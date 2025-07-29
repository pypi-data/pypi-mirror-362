import logging
import os
import shutil
import tempfile
import typing as type
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import flywheel
from flywheel_gear_toolkit import GearToolkitContext
from flywheel_migration import deidentify
from fs import osfs
from ruamel.yaml import YAML

log = logging.getLogger()


DEFAULT_FILENAME = {
    "filenames": [{"input-regex": "(?P<used>.*)$"}, {"output": "MOD-{used}"}]
}

# Based on the valid container deletion reasons, these are the only reasons that
# make sense for deid
# https://api-docs.flywheel.io/latest/tags/20.3.0/python/flywheel.models.html#flywheel.models.container_delete_reason.ContainerDeleteReason
VALID_DELETION_REASONS = ["compliance_data_policy", "compliance_phi"]


@dataclass
class RunConfig:
    input_file_path: os.PathLike
    input_file_id: os.PathLike
    deid_profile_path: os.PathLike
    subject_csv_path: os.PathLike
    key_dict: dict
    tag: str
    output_dir: os.PathLike
    delete_original: bool
    delete_reason: str


def validate_deletion_reason(deletion_reason: str):
    log.debug("Validating deletion reason")
    if deletion_reason not in VALID_DELETION_REASONS:
        raise ValueError(
            "deletion reason %s is not a valid reason: %s"
            % (deletion_reason, str(VALID_DELETION_REASONS))
        )
    log.debug("valid")


def validate_path(deid_path: Path) -> None:
    """Validates the path provided.  Must be a file, not a directory.

    Args:
        deid_path: the path of the file to deidentify

    Returns:
        None but will raise on errors.

    """
    log.debug("Validating input")
    if deid_path.is_dir():
        log.error("Deid directory")
        raise IsADirectoryError("Cannot deid a directory in place")
    if not deid_path.is_file():
        log.error("Input Not Found")
        raise FileNotFoundError("File does not exist")
    log.debug("valid")


def replace_file1_with_file2(replaced_file: Path, replacing_file: Path) -> Path:
    """Replaces the original file with the deidentified file

    This is a tricky thing to do because if you're modifying data directly and
    over-writing, so if something goes wrong you potentially lose all the data.

    Because of this, The following measures are taken:
    1. The original file is read into memory as a binary object, in a backup buffer.
    2. If it can't load the original file, it closes.  This is probably bad
        but I'm in a rush.
    3. if the original file is no longer present, it issues a warning so the user
        knows they may have to go look for it somewhere
    4. if the original file CAN'T be deleted, the program exits without saving the
        deidentified data.  it will try to save an emergency copy of the original file.
    5. if will then try to copy the deidentified file to the original file's location.
        If any exceptions are encountered, the backup buffer is saved back to disk and
        the program exits.

    Args:
        replacing_file: the path of the deid file.
        replaced_file: the path of the original file.

    Returns:
        None but raises a lot.

    """
    new_replacing_file_path = replaced_file.parent / replacing_file.name

    log.debug("Replacing original %s with %s" % (replaced_file, replacing_file))
    try:
        with open(replaced_file, "rb") as fh:
            backup_file_buffer = BytesIO(fh.read())
    except Exception:
        log.warning("Unable to buffer original file, Deid unsuccessful.  Quitting.")
        raise IOError("Unable to safely buffer original file")

    try:
        os.remove(replaced_file)
    except FileNotFoundError:
        log.warning(
            f"Original file {replaced_file} not found for deletion."
            f"Ensure Original file is no longer present."
        )
    except Exception:
        log.warning(
            "Error encountered when deleting original file.  Deid unsuccessful.  Quitting."
        )
        emergency_save(backup_file_buffer, replaced_file)
        raise OSError("Unable to safely remove original")

    try:
        shutil.move(replacing_file, new_replacing_file_path)

        # _ = subprocess.call(
        #     ["mv", replacing_file, new_replacing_file_path], shell=False
        # )

        if not os.path.exists(new_replacing_file_path):
            raise IOError("Unable to save deid file")
        return new_replacing_file_path
    except Exception as e:
        log.warning("Problem saving deidentified file with the following exception:")
        log.exception(e)
        log.warning("Restoring original.")
        emergency_save(backup_file_buffer, replaced_file)
        raise OSError("Unable to save deid'd file")


def find_writeable_directory():
    """Checks common locations for a writeable directory.

    In the event a file needs to be written out but there are permission issues with
    the default directory, attempt to look for a writable directory.

    Returns:
        directory (str): A writeable directory

    """
    # List of directories to check for write access
    directories_to_check = [
        os.path.expanduser("~"),  # User's home directory
        tempfile.gettempdir(),  # System temporary directory
        os.getcwd(),  # Current working directory
        "/tmp",  # Common temporary directory on Unix-like systems
    ]

    for directory in directories_to_check:
        if os.path.isdir(directory) and os.access(directory, os.W_OK):
            return directory

    # If no directory in the list is writeable, raise an error
    raise RuntimeError("No writeable directory found in the filesystem.")


def emergency_save(backup_buffer: BytesIO, original_path: Path) -> None:
    """Attempts to dump a backup buffer into a file.

    Args:
        backup_buffer: the bytes buffer to dump
        original_path: the path to dump to.

    Returns:

    """
    try:
        # Case 1 & 2: Attempt to restore the original file or write to its parent directory
        if original_path.exists() or (
            original_path.parent.exists() and os.access(original_path.parent, os.W_OK)
        ):
            log.debug("original dir exists with write access, saving...")
            save_path = original_path
        else:
            # Case 3: Try to create the original directory, if that fails, find a writeable directory
            if not original_path.parent.exists():
                os.makedirs(original_path.parent, exist_ok=True)
            save_path = (
                original_path
                if os.access(original_path.parent, os.W_OK)
                else Path(find_writeable_directory()) / original_path.name
            )
            log.debug("Found writable path: %s" % save_path)

        # Write buffer to determined path
        with open(save_path, "wb") as fh:
            fh.write(backup_buffer.getvalue())
            log.info(f"Original restored to: {save_path}")

    except Exception as e:
        log.error(f"Failed to save file: {str(e)}")


def load_yaml_profile(profile_path: Path) -> dict:
    """Loads a yaml profile as a simple dict.

    Args:
        profile_path:  the path of the yaml profile to load

    Returns:
        the loaded yaml profile

    """
    yaml = YAML()
    with open(profile_path, "r") as open_yaml:
        profile = yaml.load(open_yaml)
    return profile


def save_yaml_profile(profile_path: Path, profile: dict) -> None:
    """Saves a dictionary object as a yaml file"""
    yaml = YAML()
    yaml.dump(profile, profile_path)


def profile_has_filenames(path_to_deid_profile: type.Union[str, Path]) -> bool:
    """Checks to see if the deidprofile has the filenames section

    Args:
        path_to_deid_profile: the path to the profile to check

    Returns:
        true if present else false

    """
    profile = deidentify.load_profile(path_to_deid_profile)
    for file_profile in profile.file_profiles:
        if not file_profile.filenames:
            log.debug("profile has no filenames component")
            return False
    log.debug("profile has filenames component")
    return True


def deidentify_file(
    deid_profile: deidentify.deid_profile.DeIdProfile,
    file_path: str,
    output_directory: str,
):
    """perform deidentification on a single file

    Args:
        deid_profile(DeIdProfile): the de-identification profile to use to process the file
        file_path (str): the path to the file to be de-identified
        output_directory(str): the directory to which to output the de-identified file

    Returns:
        str: path to the de-identified file
    """
    dirname, basename = os.path.split(file_path)
    with osfs.OSFS(dirname) as src_fs:
        with osfs.OSFS(output_directory) as dst_fs:
            deid_profile.process_file(src_fs=src_fs, src_file=basename, dst_fs=dst_fs)
            deid_files = [dst_fs.getsyspath(fp) for fp in dst_fs.walk.files()]
    if deid_files:
        # Because this is deid-inplace, this result should always only be a single file.
        deid_path = deid_files[0]
    else:
        deid_path = ""

    return deid_path


def create_tag(valid, base_tag):
    suffix = "PASS" if valid else "FAIL"
    return f"{base_tag}-{suffix}"


def add_tags_metadata(
    context: GearToolkitContext,
    file_name: str,
    valid: int,
    tag: str,
) -> None:
    """Add gear completion tags to metadata.

    Add the specified base tag to the target fw object's metadata,
    appended with "-PASS" if the validation succeeded, "-FAIL" otherwise

    Args:
        context: the gear toolkit context
        file_name: The name of the file to add the tag to
        valid: True if validation passed, else False
        tag: the base to use for the tag

    """
    log.debug("adding tags using metadata.json")

    fail_tag = create_tag(valid=False, base_tag=tag)
    pass_tag = create_tag(valid=True, base_tag=tag)
    new_tag = create_tag(valid=valid, base_tag=tag)

    original_input = context.get_input("input-file")
    # Get previous tags to copy them over to the new file (for pipelineing)
    previous_tags = original_input["object"]["tags"]
    parent_container = original_input["hierarchy"]["type"]

    for old_tag in [fail_tag, pass_tag]:
        if old_tag in previous_tags:
            previous_tags.remove(old_tag)

    previous_tags.append(new_tag)
    log.info(f"adding tag {new_tag} to {file_name}")
    context.metadata.update_file_metadata(
        file_name, tags=previous_tags, container_type=parent_container
    )
    context.metadata.log()


def validate_destination(context: GearToolkitContext) -> bool:
    """Validate the destination of the gear.

    If the destination is not the parent of the input file, then the engine
    upload will not work.  This function will check for that and return
    a boolean.

    Returns:
        int: 0 if the destination is the parent of the input file, 1 otherwise.

    """
    input_file_object = context.get_input("input-file")
    dest_id = context.destination.get("id", "")
    file_parent = input_file_object.get("hierarchy").get("id", "")

    valid = True if dest_id == file_parent else False
    if not valid:
        log.error(
            "\nDestination is not the parent of the input file.  \n"
            "Engine upload will not work.  To prevent this, ensure that the \n"
            "output destination is set to the parent container of the \n"
            "input file.  This can be done manually, or simply by selecting \n"
            "the input file first"
        )
    return valid


def create_key_dict(gear_context: GearToolkitContext) -> dict:
    """Creates dictionary of keys to be inserted into the deid profile."""

    key_dict = dict()
    public_key_input = gear_context.config.get("public_key")
    if public_key_input:
        public_key_path = get_keys_from_path(
            gear_context.client,
            public_key_input,
            "public",
            gear_context.work_dir,
        )
        key_dict["PUBLIC_KEY"] = public_key_path
    private_key_input = gear_context.config.get("private_key")
    if private_key_input:
        private_key_path = get_keys_from_path(
            gear_context.client,
            private_key_input,
            "private",
            gear_context.work_dir,
        )
        key_dict["PRIVATE_KEY"] = private_key_path
    secret_key_input = gear_context.config.get("secret_key")
    if secret_key_input:
        secret_key_path = get_keys_from_path(
            gear_context.client,
            secret_key_input,
            "secret",
            gear_context.work_dir,
        )
        with open(secret_key_path) as f:
            secret_key = f.read()
        key_dict["SECRET_KEY"] = secret_key

    return key_dict


def get_keys_from_path(
    fw_client: flywheel.Client, key_input: str, key_type: str, workdir: str
) -> str:
    """Retrieves key file(s) from given path, saves to workdir, returns path(s)

    Args:
        fw_client: An instance of the Flywheel client
        key_input: Path to key(s), formatted as `group/project:filename`, multiple values separated by `, `
        key_type: "public" or "private"
        workdir: Path to work directory

    Returns:
        str: String representation of path(s) to downloaded key(s)
    """
    try:
        keys = key_input.split(", ")
        downloaded_keys = []
        for key in keys:
            result = fw_client.lookup(key)
            downloaded_key = f"{workdir}/{result.name}"
            file = fw_client.get_file(result.file_id)
            file.download(downloaded_key)
            downloaded_keys.append(downloaded_key)
        if key_type == "public":
            return repr(downloaded_keys)
        else:  # key_type in "private", "secret"
            return downloaded_keys[0]
    except flywheel.rest.ApiException as e:
        log.error(e, exc_info=True)
        log.error(f"Unable to download {key_type} key from {key_input}. Exiting.")
        os.sys.exit(1)
