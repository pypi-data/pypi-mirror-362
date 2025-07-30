import click
import os
import sys
import logging
import exiftool
from exiftool.exceptions import ExifToolExecuteError

log = logging.getLogger("immich-tools")

IMAGE_EXTENSIONS = {".mp4", ".jpg", ".jpeg", ".png", ".tiff", ".bmp", ".gif", ".heic", ".webp", ".mov", ".wmv"}


def find_matches(path: str) -> list[tuple[str, str]]:
    matches = []
    log.info(f"Looking for XMP files in: {path}")

    # Traverse the directory tree
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            _, ext = os.path.splitext(filepath)
            if ext.lower() in IMAGE_EXTENSIONS:
                xmp_counterpart = f"{filepath}.xmp"
                if os.path.exists(xmp_counterpart):
                    log.debug(f"file {xmp_counterpart} exists")
                    matches.append((filepath, xmp_counterpart))
    return matches


@click.command()
@click.argument("path")
@click.option("-x", "--leave-xmp", is_flag=True, help="use to leave xmp files and do not remove them")
@click.option("-o", "--leave-original", is_flag=True, help="will create copy of original file with '_original' suffix")
@click.option("--dry-run", is_flag=True, help="will run without modifying or removing any file")
def merge_xmp(path: str, leave_xmp: bool, leave_original: bool, dry_run: bool):
    """Merge xmp sidecards to original image file from PATH recursively"""
    overwrite_original = "-overwrite_original"
    if leave_original:
        overwrite_original = ""
        log.debug("option -o/--leave-original is turned on - will create copy of original file with '_original' suffix")
    if leave_xmp:
        log.debug("option -x/--leave-xmp is turned on - will not remove xmp sidecards")
    matches = find_matches(path)
    for image, xmp in matches:
        with exiftool.ExifToolHelper() as ex:
            log.debug(f"merging {xmp} with {image}")
            try:
                if dry_run:
                    log.info(f"[DRY-RUN] writing tags from {xmp} to {image}")
                else:
                    ex.execute("-tagsfromfile", f"{xmp}", "-all:all", f"{overwrite_original}", f"{image}")
                if not leave_xmp:
                    if dry_run:
                        log.info(f"[DRY-RUN] removing {xmp}")
                    else:
                        log.debug(f"removing: {xmp}")
                        os.remove(xmp)
            except ExifToolExecuteError as er:
                log.error(ex.last_stderr.strip())
                log.error(f"error while executing exiftool command: {er}")
                sys.exit(-1)
    log.info(f"merged {len(matches)} files")
