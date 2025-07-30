from typing import Any
from typing import Dict
from typing import Type
from typing import TypeVar

from attrs import define as _attrs_define

from ..models.termset import Termset


T = TypeVar("T", bound="SearchGetCollectionTermsResponse200")


@_attrs_define
class SearchGetCollectionTermsResponse200:
    """SearchGetCollectionTermsResponse200 model

    Attributes:
        terms (Termset):
    """

    terms: "Termset"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dict"""
        terms = self.terms.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "terms": terms,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        """Create an instance of :py:class:`SearchGetCollectionTermsResponse200` from a dict"""
        d = src_dict.copy()
        terms = Termset.from_dict(d.pop("terms"))

        search_get_collection_terms_response_200 = cls(
            terms=terms,
        )

        return search_get_collection_terms_response_200
