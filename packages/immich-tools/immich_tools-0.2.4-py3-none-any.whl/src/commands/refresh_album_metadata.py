import click
from src.immich.client.ImmichClient import ImmichClient
from src.utils.utils import send_get, send_post
import logging

log = logging.getLogger("immich-tools")


@click.command()
@click.argument("album_id")
@click.option("-k", "--api-key", required=True, envvar="IMMICH_API_KEY")
@click.option("-u", "--url", required=True, envvar="IMMICH_URL")
def refresh_album_metadata(album_id, api_key, url):
    """Refresh metada in all assets in album"""
    log.debug(f"immich url: {url}")
    immich = ImmichClient(url, api_key)
    album = immich.get_album(album_id)
    log.debug(f"found album: {album.album_name}")
    asset_ids = list()
    for asset in album.assets:
        asset_ids.append(asset.id)
    data = {"assetIds": asset_ids, "name": "refresh-metadata"}
    log.debug(f"refreshing metadata for {len(album.assets)} assets")
    send_post("/api/assets/jobs", url, api_key, data)
    log.info("success")
