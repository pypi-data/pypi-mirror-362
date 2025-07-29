from abc import ABC, abstractmethod
from typing import Dict, Generator, List, Optional, Type, TypeVar

from probely.constants import ID_404_VALIDATION
from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyObjectsNotFound,
    ProbelyRequestFailed,
)
from probely.settings import PROBELY_API_PAGE_SIZE
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.helpers import validate_id_404_response
from probely.sdk.models import SdkBaseModel

SdkBaseModelType = TypeVar("SdkBaseModelType", bound=SdkBaseModel)


class ResourceMixin(ABC):
    default_query_params = None

    def get_resource_url(self, parent_id: Optional[Dict] = None) -> str:
        """
        Construct the URL for a resource collection or a nested resource collection.
        """
        if parent_id:
            return self.resource_url.format(**parent_id)
        return self.resource_url

    def get_resource_detail_url(self, resource_identifiers: Dict) -> str:
        """
        Construct the URL for a single resource entity, optionally nested under a parent
        """
        return self.resource_detail_url.format(**resource_identifiers)

    @property
    @abstractmethod
    def resource_url(self) -> str:
        pass

    @property
    @abstractmethod
    def resource_detail_url(self) -> str:
        pass

    @property
    @abstractmethod
    def model(self) -> Type[SdkBaseModel]:
        pass


class ListMixin(ResourceMixin, ABC):
    """
    Mixin providing a 'list' method to retrieve a list of resources based on filters.
    """

    def list(
        self,
        parent_id: Optional[Dict] = None,
        filters: Optional[Dict] = None,
        ordering: Optional[str] = None,
    ) -> Generator[SdkBaseModelType, None, None]:
        url = self.get_resource_url(parent_id)
        filters = filters or {}
        page = 1

        if not ordering:
            ordering = getattr(self, "listing_ordering", "-changed")

        params = {
            "ordering": ordering,
            "length": PROBELY_API_PAGE_SIZE,
            "page": 1,
            **(self.default_query_params if self.default_query_params else {}),
            **filters,
        }

        while True:
            resp_status_code, resp_content = ProbelyAPIClient.get(
                url, query_params=params
            )

            validate_id_404_response(status_code=resp_status_code, content=resp_content)

            if resp_status_code != 200:
                raise ProbelyRequestFailed(reason=resp_content)

            results = resp_content.get("results", [])
            total_pages_count = resp_content.get("page_total", 1)

            for item in results:
                deserialized_data = self.model.serializer_class(**item)
                yield self.model(deserialized_data)

            if page >= total_pages_count:
                break

            page += 1
            params["page"] = page


class RetrieveMixin(ListMixin, ResourceMixin, ABC):
    def retrieve(self, resource_identifiers: Dict) -> SdkBaseModelType:
        url = self.get_resource_detail_url(resource_identifiers)
        resp_status_code, resp_content = ProbelyAPIClient.get(
            url, query_params=self.default_query_params
        )

        if resp_status_code == 404:
            raise ProbelyObjectsNotFound(resource_identifiers.get("id"))

        if resp_status_code != 200:
            raise ProbelyRequestFailed(reason=resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)

    def retrieve_multiple(
        self,
        entity_ids: List[str],
    ) -> Generator[SdkBaseModelType, None, None]:
        f"""
        Efficient way to retrieve multiple entities by ID.

        Only possible for API endpoints with 'id' filters
        and '{ID_404_VALIDATION}' flag
        """

        filters = {
            "id": entity_ids,
            ID_404_VALIDATION: True,
        }
        return self.list(filters=filters)

    def unoptimized_get_multiple(
        self, entity_ids: List[Dict]
    ) -> List[SdkBaseModelType]:
        """
        Retrieve multiple resources by their IDs.

        Avoid using unless API is not ready for CLI yet.
        """
        values = [self.retrieve(entity_id) for entity_id in entity_ids]
        return values


class DeleteMixin(ResourceMixin, ABC):
    def delete(self, resource_identifiers: Dict) -> None:
        url = self.get_resource_detail_url(resource_identifiers)
        resp_status_code, resp_content = ProbelyAPIClient.delete(url=url)

        if resp_status_code == 404:
            raise ProbelyObjectsNotFound(resource_identifiers.get("id"))

        if resp_status_code != 204:
            raise ProbelyRequestFailed(reason=resp_content)


class UpdateMixin(ResourceMixin, ABC):
    def update(
        self, resource_identifiers: Dict, payload: Dict = None
    ) -> SdkBaseModelType:
        query_params = self.default_query_params
        url = self.get_resource_detail_url(resource_identifiers)

        resp_status_code, resp_content = ProbelyAPIClient.patch(
            url, query_params=query_params, payload=payload
        )

        if resp_status_code == 400:
            raise ProbelyBadRequest(resp_content)
        if resp_status_code == 404:
            raise ProbelyObjectsNotFound(resource_identifiers["id"])
        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)
