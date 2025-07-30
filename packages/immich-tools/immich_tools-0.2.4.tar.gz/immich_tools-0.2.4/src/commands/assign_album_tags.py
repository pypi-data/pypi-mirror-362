import click
from src.immich.client.ImmichClient import ImmichClient, Album
import logging
import sys

log = logging.getLogger("immich-tools")
global immich


@click.command()
@click.argument("album_id")
@click.option("-k", "--api-key", required=True, envvar="IMMICH_API_KEY")
@click.option("-u", "--url", required=True, envvar="IMMICH_URL")
@click.option("-c", "--create-tag", is_flag=True, help="will create missing tags if needed")
def assign_album_tags(album_id, api_key, url, create_tag):
    """looking in album for specified tags and return assets without expected tags. Use all as album id to assign tags in all albums"""
    log.debug(f"immich url: {url}")
    global immich
    immich = ImmichClient(url, api_key)
    if album_id == "all":
        albums = immich.get_albums()
        for album in albums:
            __handle_album(immich.get_album(album.id))
    else:
        album = immich.get_album(album_id)
        __handle_album(album)
    log.info("success")

def __handle_album(album: Album):
    album_name = album.album_name
    log.debug(f"found album: {album_name}")
    tags = __get_tags_from_discription(album.description)
    asset_ids = list(map(lambda a: a.id, album.assets))
    log.debug("creating tags if necessary")
    create_tag_responses = immich.upsert_tags(tags)
    for response in create_tag_responses:
        log.debug(f"assigning tag: {response.value}")
        immich.assign_tag_to_assets(response.id, asset_ids)

def __get_tags_from_discription(description: str) -> list[str]:
    tags = []
    for line in description.split("\n"):
        if "=" in line and line.split("=")[0] == "tag":
            tag = line.split("=")[1]
            log.debug(f"found tag in description: {tag}")
            tags.append(tag)
            
    return tags

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
