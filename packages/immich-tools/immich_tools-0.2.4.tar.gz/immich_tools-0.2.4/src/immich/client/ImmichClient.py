from datetime import datetime

import logging
import mimetypes
import io


from src.immich.model.Album import Album
from src.immich.model.Asset import Asset
from src.immich.model.response.AssetToAlbumResponse import AssetToAlbumResponse
from src.immich.model.response.AssignTagResponse import AssignTagResponse
from src.immich.model.Tag import Tag
from src.immich.model.User import User
from src.immich.model.response.CreateTagResponse import CreateTagResponse
from src.immich.model.response.UploadAssetResponse import UploadAssetResponse
from src.immich.utils.Utils import Utils


class ImmichClient:
    def __init__(self, url, api_key):
        self.log = logging.getLogger("immich-tools")
        self.url = url
        self.api_key = api_key
        self.utils = Utils(url, api_key)

    def get_asset(self, id: str) -> Asset:
        """Returns asset of id \n
        path: /api/asssets/:id

        Parameters:
          id: id of the asset

        Returns:
          asset
        """
        r = self.utils.send_get(f"/api/assets/{id}")
        return self.utils.from_dict(data_class=Asset, data=r.json())

    def get_album(self, id: str) -> Album:
        """Returns album of id \n
        path: /api/albums/:id

        Parameters:
          id: id of the album

        Returns:
          album
        """
        r = self.utils.send_get(f"/api/albums/{id}")
        return self.utils.from_dict(Album, r.json())
      
      
    def get_albums(self) -> list[Album]:
        """Returns album of id \n
        path: /api/albums/:id

        Returns:
          all album
        """
        r = self.utils.send_get(f"/api/albums")
        albums_json = r.json()
        return [self.utils.from_dict(Album, album_json) for album_json in albums_json]

    def get_all_tags(self) -> list[Tag]:
        """Returns all tags \n
        path: /api/tags

        Returns:
          list of tags
        """
        r = self.utils.send_get(f"/api/tags")
        tags_json = r.json()
        return [self.utils.from_dict(Tag, tag_json) for tag_json in tags_json]

    def assign_tag_to_assets(self, tagId: str, assetIds: list[str]) -> list[AssignTagResponse]:
        """assign tags to assets \n
        PUT /api/tags/{tagId}/assets

        Returns:
          Immich Response
        """
        r = self.utils.send_put(f"/api/tags/{tagId}/assets", data={"ids": assetIds})
        responses = r.json()
        return [self.utils.from_dict(AssignTagResponse, response) for response in responses]

    def get_user(self) -> User:
        """Returns owner of the api key \n
        GET /api/users/me

        Returns:
          User
        """
        r = self.utils.send_get(f"/api/users/me")
        return self.utils.from_dict(User, r.json())

    def create_tag(self, name: str, color="", parentId="") -> CreateTagResponse:
        """create tag \n
        POST /api/tags
        """
        data = {"name": name}
        if color and color != "":
            data["color"] = color
        if parentId and parentId != "":
            data["parentId"] = parentId
        r = self.utils.send_post(f"/api/tags", data=data)
        return self.utils.from_dict(CreateTagResponse, r.json())
      
    def upsert_tags(self, names: list[str]) -> list[CreateTagResponse]:
        """create or update tags \n
        PUT /api/tags
        """
        data = {"tags": names}
        r = self.utils.send_put(f"/api/tags", data=data)
        responses = r.json()
        return [self.utils.from_dict(CreateTagResponse, response) for response in responses]

    def get_asset_content(self, assetId: str) -> bytes:
        """Returns owner of the api key \n
        GET /api/assets/{id}/original

        Returns:
          content of asset in bytes
        """
        r = self.utils.send_get(f"/api/assets/{assetId}/original")
        return r.content

    def upload_asset(
        self,
        asset_data: bytes,
        device_asset_id: str,
        device_id: str,
        file_created_at: datetime,
        file_modified_at: datetime,
        filename: str,
    ) -> UploadAssetResponse:
        """upload asset \n
        POST /assets

        Returns:
          UploadAssetResponse
        """
        mime_type, _ = mimetypes.guess_type(filename)
        files = {"assetData": (filename, io.BytesIO(asset_data), mime_type)}
        data = {
            "deviceAssetId": device_asset_id,
            "deviceId": device_id,
            "fileCreatedAt": self.utils.datetime_to_str(file_created_at),
            "fileModifiedAt": self.utils.datetime_to_str(file_modified_at),
        }
        self.log.debug(f"uploading {filename}...")
        r = self.utils.send_multipart("/api/assets", files, data)
        return self.utils.from_dict(UploadAssetResponse, r.json())

    def add_asset_to_album(self, album_id: str, asset_id: str) -> AssetToAlbumResponse:
        """add asset to album \n
        PUT /api/albums/{album_id}/assets

        Returns:
          AddAssetToAlbumResponse
        """
        data = {"ids": [asset_id]}
        r = self.utils.send_put(f"/api/albums/{album_id}/assets", data)
        return self.utils.from_dict(AssetToAlbumResponse, r.json())

    def remove_asset_from_album(self, album_id: str, asset_id: str) -> AssetToAlbumResponse:
        """remove asset from album \n
        DELETE /api/albums/{album_id}/assets

        Returns:
          AssetToAlbumResponse
        """
        data = {"ids": [asset_id]}
        r = self.utils.send_delete(f"/api/albums/{album_id}/assets", data)
        return self.utils.from_dict(AssetToAlbumResponse, r.json())

    def get_original_asset(self, asset_id: str) -> bytes:
        """get original asset \n
        GET /api/assets/{asset_id}/original

        Returns:
          original asset
        """
        r = self.utils.send_get(f"/api/assets/{asset_id}/original")
        return r.content