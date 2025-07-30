import click
from .commands import (
    check_album_tags,
    merge_xmp,
    refresh_album_metadata,
    run_job,
    version,
    change_owner_photo,
    assign_album_tags
)
import logging
from datetime import datetime
import src
import os


def __setup_logging(debug: bool, log_path: str):
    """Configure logging for the CLI."""
    log = logging.getLogger("immich-tools")
    log_level = logging.DEBUG if debug else logging.INFO
    log.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)-5s - %(message)s")
    log.handlers.clear()
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)

    if log_path:
        log_directory = log_path or "."
        os.makedirs(log_directory, exist_ok=True)
        log_filename = datetime.now().strftime("log_immich-tools_%d_%m_%Y.log")
        file_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    return log


@click.group(help=f"""This is immich-tools version {src.__version__}""")
@click.option("-d", "--debug", is_flag=True, help="Enable debug mode")
@click.option(
    "-l", "--log-path", help="path to directory where logs will be stored, works only if --log-file flag is set to True"
)
@click.pass_context
def main(ctx, debug: bool, log_path: str):
    ctx.ensure_object(dict)
    log = __setup_logging(debug, log_path)
    log.info("Running immich-tools")
    if debug:
        log.debug("Debug mode is ON")


commands = [
    refresh_album_metadata.refresh_album_metadata,
    merge_xmp.merge_xmp,
    run_job.run_job,
    version.version,
    check_album_tags.check_album_tags,
    change_owner_photo.change_owner_photo,
    assign_album_tags.assign_album_tags
]

for command in commands:
    main.add_command(command)
