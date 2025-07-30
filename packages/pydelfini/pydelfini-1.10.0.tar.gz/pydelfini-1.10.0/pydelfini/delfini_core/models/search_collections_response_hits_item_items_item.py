from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define

from ..models.item_type import ItemType


T = TypeVar("T", bound="SearchCollectionsResponseHitsItemItemsItem")


@_attrs_define
class SearchCollectionsResponseHitsItemItemsItem:
    """SearchCollectionsResponseHitsItemItemsItem model

    Attributes:
        id (str):
        name (str):
        path (str):
        type (ItemType):
        version_id (str):
    """

    id: str
    name: str
    path: str
    type: ItemType
    version_id: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        id = self.id
        name = self.name
        path = self.path
        type = self.type.value
        version_id = self.version_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "name": name,
                "path": path,
                "type": type,
                "versionId": version_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`SearchCollectionsResponseHitsItemItemsItem` from a dict"""
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        path = d.pop("path")

        type = ItemType(d.pop("type"))

        version_id = d.pop("versionId")

        search_collections_response_hits_item_items_item = cls(
            id=id,
            name=name,
            path=path,
            type=type,
            version_id=version_id,
        )

        return search_collections_response_hits_item_items_item
