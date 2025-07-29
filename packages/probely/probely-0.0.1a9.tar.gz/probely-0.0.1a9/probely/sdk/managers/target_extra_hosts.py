from typing import Dict, List, Optional, Generator, Union

from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyRequestFailed,
)
from probely.sdk.managers.common import SdkBaseManager
from probely.sdk.managers.mixins.delete import ParentedDeleteMixin

from probely.settings import (
    PROBELY_API_EXTRA_HOSTS_DETAIL_URL,
    PROBELY_API_ACCOUNT_EXTRA_HOSTS_URL,
    PROBELY_API_EXTRA_HOSTS_URL,
)
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.models import TargetExtraHost
from probely.sdk.managers.mixins.list import ListMixin
from probely.sdk.managers.mixins.retrieve_multiple import RetrieveMultipleMixin
from probely.sdk.managers.mixins.update import ParentedUpdateMixin


class TargetExtraHostManager(
    ListMixin,
    RetrieveMultipleMixin,
    ParentedUpdateMixin,
    ParentedDeleteMixin,
    SdkBaseManager,
):
    resource_url = PROBELY_API_ACCOUNT_EXTRA_HOSTS_URL
    resource_detail_url = PROBELY_API_EXTRA_HOSTS_DETAIL_URL
    parented_resource_url = PROBELY_API_EXTRA_HOSTS_URL
    parented_resource_detail_url = PROBELY_API_EXTRA_HOSTS_DETAIL_URL
    model = TargetExtraHost
    default_query_params = {"include": "target"}

    def list(self, filters: Dict) -> Generator[TargetExtraHost, None, None]:
        # TODO: specific and validate filters
        return self._list(filters=filters)

    def retrieve_multiple(
        self, target_extra_hosts_or_ids: List[Union[TargetExtraHost, str]]
    ) -> Generator[TargetExtraHost, None, None]:
        return self._retrieve_multiple(target_extra_hosts_or_ids)

    def update(
        self, target_extra_host_or_id: Union[TargetExtraHost, str], payload: Dict
    ) -> TargetExtraHost:
        extra_host: TargetExtraHost

        if isinstance(target_extra_host_or_id, TargetExtraHost):
            extra_host = target_extra_host_or_id
        else:
            extra_host = list(self.retrieve_multiple([target_extra_host_or_id]))[0]

        return self._parented_update(
            target_id=extra_host.target.id, entity_id=extra_host.id, payload=payload
        )

    def delete(self, target_extra_host_or_id: Union[TargetExtraHost, str]) -> None:
        extra_host: TargetExtraHost

        if isinstance(target_extra_host_or_id, TargetExtraHost):
            extra_host = target_extra_host_or_id
        else:
            extra_host = list(self.retrieve_multiple([target_extra_host_or_id]))[0]

        self._parented_delete(target_id=extra_host.target.id, entity_id=extra_host.id)

    def create(
        self,
        target_id: str,
        host: Optional[str] = None,
        include: Optional[bool] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        skip_reachability_check: Optional[bool] = False,
        headers: Optional[List[Dict]] = None,
        cookies: Optional[List[Dict]] = None,
        extra_payload: Optional[Dict] = None,
    ) -> TargetExtraHost:
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
            "desc": description,
            "headers": headers,
            "cookies": cookies,
        }
        passed_values = {k: v for k, v in passed_values.items() if v is not None}

        # Merge passed_values into body_data
        body_data.update(passed_values)

        query_params = {"skip_reachability_check": skip_reachability_check}

        url = self.parented_resource_url.format(target_id=target_id)
        resp_status_code, resp_content = ProbelyAPIClient.post(
            url=url, query_params=query_params, payload=body_data
        )

        if resp_status_code == 400:
            raise ProbelyBadRequest(response_payload=resp_content)

        if resp_status_code != 201:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)
