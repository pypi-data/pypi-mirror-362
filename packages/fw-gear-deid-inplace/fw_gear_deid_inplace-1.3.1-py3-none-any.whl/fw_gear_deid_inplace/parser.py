"""Parser module to parse gear config.json."""

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_deid_inplace.utils import RunConfig, create_key_dict


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> RunConfig:
    """Parses the gear context

    Returns:
        RunConfig: Dataclass with paths and config args
    """

    input_file_object = gear_context.get_input("input-file")

    run_config = RunConfig(
        input_file_path=gear_context.get_input_path("input-file"),
        input_file_id=input_file_object.get("object", {}).get("file_id", ""),
        deid_profile_path=gear_context.get_input_path("deid-profile"),
        subject_csv_path=gear_context.get_input_path("subject-csv"),
        key_dict=create_key_dict(gear_context),
        tag=gear_context.config.get("tag"),
        delete_original=gear_context.config.get("delete-original"),
        output_dir=gear_context.output_dir,
        delete_reason=gear_context.config.get("delete-reason"),
    )

    return run_config
