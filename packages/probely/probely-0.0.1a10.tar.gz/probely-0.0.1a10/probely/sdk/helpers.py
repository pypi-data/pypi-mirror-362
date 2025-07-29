from typing import List, Sequence, Type, Union
from urllib.parse import urljoin

from probely import ProbelyException, ProbelyObjectsNotFound, ProbelyRequestFailed
from probely.constants import ID_404_VALIDATION
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.models import SdkBaseModel


def validate_id_404_response(status_code: int, content: dict):
    """
    Validates Custom API response that is triggered by 'is_id_404_validation' flag.
    It expects following response:
    {
        "detail": "Not Found",
        "is_id_404_validation": true,
        "invalid_ids": [
            "9vebyEVLNoZX",
            "6CuzJtJmMp48"
        ]
    }

    It's specific for this content and shouldn't replace other 404 validations
    """
    if status_code == 404:
        if content.get(ID_404_VALIDATION):
            raise ProbelyObjectsNotFound(content["invalid_ids"])


def unoptimized_resource_ids_validation(resource_url: str, resource_ids: List[str]):
    """
    Validates a list of resource IDs by performing GET requests to the API.

    Unoptimized as it requests each ID individually and sequentially.

    Only to be used when API list of resource is not optimized yet.
    """

    for resource_id in resource_ids:
        url = urljoin(resource_url, resource_id)
        resp_status_code, resp_content = ProbelyAPIClient.get(url)

        if resp_status_code == 404:
            raise ProbelyObjectsNotFound(resource_id)
        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)


def retrieve_entity_or_str_id(
    entity_class: Type[SdkBaseModel],
    entity: Union[SdkBaseModel, str],
) -> str:
    if isinstance(entity, entity_class):
        return str(entity.id)
    elif isinstance(entity, str):
        return entity
    else:
        raise ProbelyException(
            f"Invalid type, argument '{str(entity)}'. Must be {entity_class} or str"
        )


def retrieve_entity_or_str_ids(
    entity_class: Type[SdkBaseModel],
    entities: Sequence[Union[SdkBaseModel, str]],
) -> List[str]:
    entity_ids = []
    for entity in entities:
        entity_id: str = retrieve_entity_or_str_id(entity_class, entity)
        entity_ids.append(entity_id)

    return entity_ids
