import click
from src.immich.client.ImmichClient import ImmichClient
import logging
import sys

log = logging.getLogger("immich-tools")
global immich


@click.command()
@click.argument("album_id")
@click.option("-k", "--api-key", required=True, envvar="IMMICH_API_KEY")
@click.option("-u", "--url", required=True, envvar="IMMICH_URL")
@click.option(
    "-t", "--tag", "expected_tags", required=True, multiple=True, help="expected tags (use multiple -t/--tag)"
)
@click.option("-a", "--add-missing", is_flag=True, help="will add missing tags")
@click.option("-c", "--create-tag", is_flag=True, help="will create missing tags if needed")
def check_album_tags(album_id, api_key, url, expected_tags, add_missing, create_tag):
    """looking in album for specified tags and return assets without expected tags"""
    log.debug(f"immich url: {url}")
    global immich
    immich = ImmichClient(url, api_key)
    album = immich.get_album(album_id)
    album_name = album.album_name
    log.debug(f"found album: {album_name}")
    assets = list(map(lambda a: a.id, album.assets))
    for asset_id in assets:
        asset = immich.get_asset(asset_id)
        tags = asset.tags if asset.tags else []
        tags = list(map(lambda tag: tag.value, tags))
        if not set(expected_tags).issubset(tags):
            missing_tags = list(set(expected_tags) - set(tags))
            print(f"asset: {asset.id}, actual tags: {tags}, missing tags: {missing_tags}")
            if add_missing:
                all_tags = __get_all_tags_value_id()
                __add_missing_tags(asset.id, missing_tags, all_tags, create_tag)
    log.info("success")


def __get_all_tags_value_id() -> dict:
    all_tags = immich.get_all_tags()
    result = {}
    for tag in all_tags:
        result[tag.value] = tag.id
    return result


def __add_missing_tags(asset_id: str, missing_tags: list[str], all_tags: dict, create_tag: bool):
    for missing_tag in missing_tags:
        log.debug(f"adding tag: {missing_tag} to asset: {asset_id}")
        if missing_tag not in all_tags:
            if create_tag:
                log.debug(f"creating tag: {missing_tag}")
                immich.create_tag(name=missing_tag)
                log.debug("retrying to add tag to asset...")
                __add_missing_tags(asset_id, missing_tags, __get_all_tags_value_id(), create_tag)
                return
            else:
                log.error(f'there is not added tag "{missing_tag}" in immich. Add tag then retry.')
                sys.exit(-1)
        id = all_tags[missing_tag]
        immich.assign_tag_to_assets(id, [asset_id])
