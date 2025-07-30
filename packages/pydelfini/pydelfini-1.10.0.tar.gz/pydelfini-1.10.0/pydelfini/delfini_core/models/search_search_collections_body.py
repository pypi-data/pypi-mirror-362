from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar
from typing import Union

from attrs import define as _attrs_define

from ..models.search_search_collections_body_facets import (
    SearchSearchCollectionsBodyFacets,
)
from ..types import UNSET
from ..types import Unset


T = TypeVar("T", bound="SearchSearchCollectionsBody")


@_attrs_define
class SearchSearchCollectionsBody:
    """SearchSearchCollectionsBody model

    Attributes:
        query (str):
        facets (Union[Unset, SearchSearchCollectionsBodyFacets]):
    """

    query: str
    facets: Union[Unset, "SearchSearchCollectionsBodyFacets"] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        query = self.query
        facets: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.facets, Unset):
            facets = self.facets.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "query": query,
            }
        )
        if facets is not UNSET:
            field_dict["facets"] = facets

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`SearchSearchCollectionsBody` from a dict"""
        d = src_dict.copy()
        query = d.pop("query")

        _facets = d.pop("facets", UNSET)
        facets: Union[Unset, SearchSearchCollectionsBodyFacets]
        if isinstance(_facets, Unset):
            facets = UNSET
        else:
            facets = SearchSearchCollectionsBodyFacets.from_dict(_facets)

        search_search_collections_body = cls(
            query=query,
            facets=facets,
        )

        return search_search_collections_body
