from typing import Union

from mergedeep import Strategy, merge

from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyRequestFailed,
)

from probely.sdk.managers.base_manager import SdkBaseManager
from probely.settings import (
    PROBELY_API_TARGET_LABELS_DETAIL_URL,
    PROBELY_API_TARGET_LABELS_URL,
)
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.managers.mixins import (
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    UpdateMixin,
)
from probely.sdk.models import TargetLabel


class TargetLabelManager(
    RetrieveMixin, ListMixin, DeleteMixin, UpdateMixin, SdkBaseManager
):
    resource_url = PROBELY_API_TARGET_LABELS_URL
    resource_detail_url = PROBELY_API_TARGET_LABELS_DETAIL_URL
    model = TargetLabel

    def create(
        self,
        name: str,
        color: Union[str, None] = None,
        extra_payload: Union[dict, None] = None,
    ) -> TargetLabel:
        """Creates new target label

        :param name: label name.
        :type name: str.
        :param color: color of target label.
        :type color: str, optional.
        :param extra_payload: allows customization of request. Content should follow api request body
        :type extra_payload: Optional[dict].
        :raise: ProbelyBadRequest.
        :return: Created target label content.

        """

        body_data = {}
        if extra_payload:
            body_data = extra_payload

        arguments_settings = {
            "name": name,
        }
        if color:
            arguments_settings["color"] = color

        merge(body_data, arguments_settings, strategy=Strategy.REPLACE)

        resp_status_code, resp_content = ProbelyAPIClient.post(
            url=self.resource_url, payload=body_data
        )

        if resp_status_code == 400:
            raise ProbelyBadRequest(response_payload=resp_content)

        if resp_status_code != 201:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)
