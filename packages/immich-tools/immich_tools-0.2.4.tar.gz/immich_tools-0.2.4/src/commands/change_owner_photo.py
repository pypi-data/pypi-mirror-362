import click
from src.immich.client.ImmichClient import ImmichClient
from src.immich.model.Album import Album
from src.immich.model.Asset import Asset
from src.utils.utils import send_get, send_put, send_post, send_multipart, send_delete
import logging
import io
import mimetypes

log = logging.getLogger("immich-tools")
global immich


@click.command()
@click.argument("album_id")
@click.option("-k", "--api-key", required=True, envvar="IMMICH_API_KEY")
@click.option("-u", "--url", required=True, envvar="IMMICH_URL")
def change_owner_photo(album_id, api_key, url):
    """change ownership of all assets in the album to you. Use all as album id to change ownership of all albums"""
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
    log.debug(f"found album: {album.album_name}")
    owner_id = __get_owner_of_api_key()
    assets = album.assets
    for asset in assets:
        old_asset_id = asset.id
        old_asset_info = immich.get_asset(asset.id)
        if old_asset_info.owner_id != owner_id:
            log.debug(f"asset: {old_asset_id} is not yours, downloading...")
            asset_content = immich.get_original_asset(old_asset_id)
            live_video_id = asset.live_photo_video_id
            if live_video_id != None:
                log.debug(f"asset have live video related: {live_video_id}, downloading...")
                live_video_asset = immich.get_asset(live_video_id)
                live_video_content = immich.get_asset_content(live_video_id)
                __upload_file(live_video_content, live_video_asset)
            new_asset_id = __upload_file(asset_content, asset)
            log.debug(f"adding new asset {new_asset_id} to album...")
            immich.add_asset_to_album(album.id, new_asset_id)
            log.debug(f"new asset added, now removing old asset from album: {old_asset_id}")
            immich.remove_asset_from_album(album.id, old_asset_id)

def __get_owner_of_api_key():
    return immich.get_user().id


def __upload_file_old(url: str, api_key: str, content: bytes, asset: Asset):
    filename = asset.original_file_name
    mime_type, _ = mimetypes.guess_type(filename)
    files = {"assetData": (filename, io.BytesIO(content), mime_type)}
    data = {
        "deviceAssetId": asset.device_asset_id,
        "deviceId": asset.device_id,
        "fileCreatedAt": asset.file_created_at,
        "fileModifiedAt": asset.file_modified_at,
    }
    log.debug(f"uploading {filename}...")
    r = send_multipart("/api/assets", url, api_key, files, data)
    return r.json()["id"]


def __upload_file(content: bytes, asset: Asset):
    return immich.upload_asset(
        content,
        asset.device_asset_id,
        asset.device_id,
        asset.file_created_at,
        asset.file_modified_at,
        asset.original_file_name,
    ).id
