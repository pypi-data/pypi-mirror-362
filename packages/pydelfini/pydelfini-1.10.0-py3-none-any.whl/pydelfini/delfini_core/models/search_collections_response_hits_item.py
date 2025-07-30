from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define

from ..models.collection import Collection
from ..models.search_collections_response_hits_item_items_item import (
    SearchCollectionsResponseHitsItemItemsItem,
)


T = TypeVar("T", bound="SearchCollectionsResponseHitsItem")


@_attrs_define
class SearchCollectionsResponseHitsItem:
    """SearchCollectionsResponseHitsItem model

    Attributes:
        collection (Collection): Core collection properties, with IDs
        items (List['SearchCollectionsResponseHitsItemItemsItem']):
    """

    collection: "Collection"
    items: List["SearchCollectionsResponseHitsItemItemsItem"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        collection = self.collection.to_dict()
        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "collection": collection,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`SearchCollectionsResponseHitsItem` from a dict"""
        d = src_dict.copy()
        collection = Collection.from_dict(d.pop("collection"))

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = SearchCollectionsResponseHitsItemItemsItem.from_dict(
                items_item_data
            )

            items.append(items_item)

        search_collections_response_hits_item = cls(
            collection=collection,
            items=items,
        )

        return search_collections_response_hits_item
