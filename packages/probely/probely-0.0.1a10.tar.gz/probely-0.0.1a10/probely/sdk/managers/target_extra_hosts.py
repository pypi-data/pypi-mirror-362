from typing import Dict, List, Optional


from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyRequestFailed,
)
from probely.sdk.managers.base_manager import SdkBaseManager

from probely.settings import (
    PROBELY_API_EXTRA_HOSTS_DETAIL_URL,
    PROBELY_API_EXTRA_HOSTS_URL,
)
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.managers.mixins import (
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    UpdateMixin,
)
from probely.sdk.models import ExtraHost


class TargetExtraHostManager(
    RetrieveMixin, ListMixin, UpdateMixin, DeleteMixin, SdkBaseManager
):
    resource_url = PROBELY_API_EXTRA_HOSTS_URL
    resource_detail_url = PROBELY_API_EXTRA_HOSTS_DETAIL_URL
    model = ExtraHost

    def create(
        self,
        target_id: str,
        host: Optional[str] = None,
        include: Optional[bool] = None,
        name: Optional[str] = None,
        desc: Optional[str] = None,
        headers: Optional[List[Dict]] = None,
        cookies: Optional[List[Dict]] = None,
        extra_payload: Optional[Dict] = None,
    ) -> ExtraHost:
        """
        Create a new Extra Host for a Target.

        :param target_id: The target ID.
        :type target_id: str.
        :param host: The host to be added.
        :type host: str, optional.
        :param include: Whether to include the host in the scan.
        :type include: bool, optional.
        :param name: The name of the Extra Host.
        :type name: str, optional.
        :param desc: The description of the Extra Host.
        :type desc: str, optional.
        :param headers: Custom headers to be sent."
        :type headers: List[Dict], optional.
        :param cookies: Custom cookies to be sent.
        :type cookies: List[Dict], optional.
        :param extra_payload: Allows customization of request. Content should follow api request body.
        :type extra_payload: Optional[Dict].
        :raise: ProbelyBadRequest.
        :return: Created Extra Host instance.
        """

        body_data = {}
        if extra_payload:
            body_data = extra_payload

        # Update body_data with explicitly passed arguments, overriding extra_payload if necessary
        passed_values = {
            "host": host,
            "include": include,
            "name": name,
            "desc": desc,
            "headers": headers,
            "cookies": cookies,
        }
        passed_values = {k: v for k, v in passed_values.items() if v is not None}

        # Merge passed_values into body_data
        body_data.update(passed_values)

        url = self.resource_url.format(target_id=target_id)
        resp_status_code, resp_content = ProbelyAPIClient.post(
            url=url, payload=body_data
        )

        if resp_status_code == 400:
            raise ProbelyBadRequest(response_payload=resp_content)

        if resp_status_code != 201:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)
