import json
from typing import Dict, List, Union

from mergedeep import Strategy, merge

from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyRequestFailed,
)

from probely import SequenceTypeEnum
from probely.sdk.managers.base_manager import SdkBaseManager
from probely.settings import (
    PROBELY_API_SEQUENCES_DETAIL_URL,
    PROBELY_API_SEQUENCES_URL,
)
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.managers.mixins import (
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    UpdateMixin,
)
from probely.sdk.models import Sequence


class TargetSequenceManager(
    RetrieveMixin,
    ListMixin,
    UpdateMixin,
    DeleteMixin,
    SdkBaseManager,
):
    default_query_params = {"include": "content"}
    resource_url = PROBELY_API_SEQUENCES_URL
    resource_detail_url = PROBELY_API_SEQUENCES_DETAIL_URL
    model = Sequence

    def create(
        self,
        target_id: str,
        name: Union[str, None],
        sequence_steps: List[Dict],
        sequence_type: Union[SequenceTypeEnum, None] = None,
        requires_authentication: Union[bool, None] = None,
        enabled: Union[str, None] = None,
        index: Union[int, None] = None,
        extra_payload: Union[Dict, None] = None,
    ) -> Sequence:
        """Creates new Sequence

        :param target_id :
        :type name: str.
        :param name :
        :type name: str.
        :param sequence_steps :
        :type sequence_steps: list.
        :param sequence_type:
        :type sequence_type: SequenceTypeEnum, optional.
        :param requires_authentication:
        :type requires_authentication: bool, optional.
        :param enabled: Enabled.
        :type enabled: bool, optional.
        :param index:
        :type index: int, optional.
        :param extra_payload: allows customization of request. Content should follow api request body
        :type extra_payload: Optional[Dict].
        :raise: ProbelyBadRequest.
        :return: Created Sequence instance.
        """

        query_params = self.default_query_params.copy()

        body_data = {}
        if extra_payload:
            body_data = extra_payload

        content = json.dumps(sequence_steps)

        passed_values = {
            "name": name,
            "content": content,
            "type": sequence_type.api_request_value if sequence_type else None,
            "requires_authentication": requires_authentication,
            "enabled": enabled,
            "index": index,
        }
        passed_values = {k: v for k, v in passed_values.items() if v is not None}

        merge(body_data, passed_values, strategy=Strategy.REPLACE)

        url = self.resource_url.format(target_id=target_id)
        resp_status_code, resp_content = ProbelyAPIClient.post(
            url=url, query_params=query_params, payload=body_data
        )

        if resp_status_code == 400:
            raise ProbelyBadRequest(response_payload=resp_content)

        if resp_status_code != 201:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)
