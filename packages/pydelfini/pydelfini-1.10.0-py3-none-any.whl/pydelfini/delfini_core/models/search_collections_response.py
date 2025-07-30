from typing import Any
from typing import Dict
from typing import List
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define

from ..models.pagination import Pagination
from ..models.search_collections_response_hits_item import (
    SearchCollectionsResponseHitsItem,
)
from ..models.termset import Termset


T = TypeVar("T", bound="SearchCollectionsResponse")


@_attrs_define
class SearchCollectionsResponse:
    """SearchCollectionsResponse model

    Attributes:
        hits (List['SearchCollectionsResponseHitsItem']):
        pagination (Pagination):
        terms (Termset):
    """

    hits: List["SearchCollectionsResponseHitsItem"]
    pagination: "Pagination"
    terms: "Termset"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        hits = []
        for hits_item_data in self.hits:
            hits_item = hits_item_data.to_dict()
            hits.append(hits_item)

        pagination = self.pagination.to_dict()
        terms = self.terms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "hits": hits,
                "pagination": pagination,
                "terms": terms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`SearchCollectionsResponse` from a dict"""
        d = src_dict.copy()
        hits = []
        _hits = d.pop("hits")
        for hits_item_data in _hits:
            hits_item = SearchCollectionsResponseHitsItem.from_dict(hits_item_data)

            hits.append(hits_item)

        pagination = Pagination.from_dict(d.pop("pagination"))

        terms = Termset.from_dict(d.pop("terms"))

        search_collections_response = cls(
            hits=hits,
            pagination=pagination,
            terms=terms,
        )

        return search_collections_response
