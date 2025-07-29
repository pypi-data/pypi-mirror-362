import json
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, Generator, List, Optional, Union

import yaml
from mergedeep import Strategy, merge

from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyObjectsNotFound,
    ProbelyRequestFailed,
    ProbelyValidation,
)

from .. import SequenceTypeEnum, TargetAPISchemaTypeEnum, TargetTypeEnum
from ..constants import ID_404_VALIDATION
from ..settings import (
    PROBELY_API_EXTRA_HOSTS_DETAIL_URL,
    PROBELY_API_EXTRA_HOSTS_URL,
    PROBELY_API_FINDINGS_DETAIL_URL,
    PROBELY_API_FINDINGS_URL,
    PROBELY_API_SCAN_CANCEL_URL_TEMPLATE,
    PROBELY_API_SCAN_PAUSE_URL_TEMPLATE,
    PROBELY_API_SCAN_RESUME_URL_TEMPLATE,
    PROBELY_API_SCANS_BULK_CANCEL_URL,
    PROBELY_API_SCANS_BULK_PAUSE_URL,
    PROBELY_API_SCANS_BULK_RESUME_URL,
    PROBELY_API_SCANS_BULK_START_URL,
    PROBELY_API_SCANS_DETAIL_URL,
    PROBELY_API_SCANS_URL,
    PROBELY_API_SEQUENCES_DETAIL_URL,
    PROBELY_API_SEQUENCES_URL,
    PROBELY_API_TARGET_LABELS_DETAIL_URL,
    PROBELY_API_TARGET_LABELS_URL,
    PROBELY_API_TARGETS_BULK_DELETE_URL,
    PROBELY_API_TARGETS_BULK_UPDATE_URL,
    PROBELY_API_TARGETS_DETAIL_URL,
    PROBELY_API_TARGETS_START_SCAN_URL,
    PROBELY_API_TARGETS_UPLOAD_API_SCHEMA_FILE_URL,
    PROBELY_API_TARGETS_URL,
)
from .client import ProbelyAPIClient
from .helpers import (
    retrieve_entity_or_str_id,
    retrieve_entity_or_str_ids,
    validate_id_404_response,
)
from .mixins import DeleteMixin, ListMixin, RetrieveMixin, UpdateMixin
from .models import ExtraHost, Finding, Scan, Sequence, Target, TargetLabel


class SdkBaseManager:
    pass


class TargetManager(
    RetrieveMixin,
    ListMixin,
    DeleteMixin,
    UpdateMixin,
    SdkBaseManager,
):
    resource_url = PROBELY_API_TARGETS_URL
    resource_detail_url = PROBELY_API_TARGETS_DETAIL_URL
    model = Target

    def bulk_delete(
        self,
        targets: List[Union[Target, str]],
    ) -> List[str]:
        """Delete targets

        :param targets: targets to be deleted.
        :type targets:List[Union[Target, str]].
        """

        target_ids = retrieve_entity_or_str_ids(Target, targets)

        resp_status_code, resp_content = ProbelyAPIClient.post(
            url=PROBELY_API_TARGETS_BULK_DELETE_URL,
            query_params={ID_404_VALIDATION: True},
            payload={
                "ids": target_ids,
            },
        )

        validate_id_404_response(status_code=resp_status_code, content=resp_content)

        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        deleted_targets_ids = resp_content.get("ids", [])

        return deleted_targets_ids

    def bulk_update(
        self,
        targets: List[Union[Target, str]],
        payload: Dict,
    ) -> Generator[Target, None, None]:
        target_ids = retrieve_entity_or_str_ids(Target, targets)

        resp_status_code, resp_content = ProbelyAPIClient.post(
            url=PROBELY_API_TARGETS_BULK_UPDATE_URL,
            query_params={ID_404_VALIDATION: True},
            payload={"ids": target_ids, **payload},
        )

        validate_id_404_response(status_code=resp_status_code, content=resp_content)

        if resp_status_code == 400:
            raise ProbelyBadRequest(resp_content)

        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        updated_targets_ids = resp_content.get("ids", [])

        targets: Generator[Target] = self.retrieve_multiple(updated_targets_ids)

        return targets

    def _upload_api_schema_file(self, target_id, api_schema_file_content: Dict):
        url = PROBELY_API_TARGETS_UPLOAD_API_SCHEMA_FILE_URL.format(target_id=target_id)

        yaml_data = yaml.dump(api_schema_file_content)
        yaml_file = BytesIO(yaml_data.encode("utf-8"))

        file_name = f"{target_id}-api_schema_file-{datetime.now()}.yaml"
        files = {"file": (file_name, yaml_file, "application/yaml")}

        resp_status_code, resp_content = ProbelyAPIClient.post(url=url, files=files)

        if resp_status_code != 201:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)

    def create(
        self,
        target_url: str,
        target_name: Union[str, None] = None,
        target_type: TargetTypeEnum = TargetTypeEnum.WEB,
        api_schema_type: Union[TargetAPISchemaTypeEnum, None] = None,
        api_schema_file_url: Union[str, None] = None,
        api_schema_file_content: dict = None,
        extra_payload: Union[dict, None] = None,
    ) -> Target:
        """Creates new target

        :param api_schema_type:
        :type api_schema_type: APISchemaTypeEnum, optional.
        :param api_schema_file_url:
        :type api_schema_file_url: str, optional.
        :param api_schema_file_content:
        :type api_schema_file_content: dict, optional.
        :param target_type:
        :type target_type: TargetTypeEnum, optional.
        :param target_url: url to be scanned.
        :type target_url: str.
        :param target_name: name of target.
        :type target_name: str, optional.
        :param extra_payload: allows customization of request. Content should follow api request body
        :type extra_payload: Optional[dict].
        :raise: ProbelyBadRequest.
        :return: Created target content.

        """
        if api_schema_file_url and api_schema_file_content:
            raise ProbelyValidation(
                "Parameters 'api_schema_file_url' and 'api_schema_file_content' are mutually exclusive"
            )

        query_params = {
            "duplicate_check": False,
            "skip_reachability_check": True,
        }

        body_data = {}
        if extra_payload:
            body_data = extra_payload

        arguments_settings = {
            "site": {"url": target_url},
            "type": target_type.api_request_value,
        }
        if target_name:
            arguments_settings["site"]["name"] = target_name

        if target_type == TargetTypeEnum.API:
            api_scan_settings = {}

            if api_schema_file_url:
                api_scan_settings["api_schema_url"] = api_schema_file_url

            if api_schema_type:
                api_scan_settings["api_schema_type"] = api_schema_type.api_request_value

            arguments_settings["site"]["api_scan_settings"] = api_scan_settings

        merge(body_data, arguments_settings, strategy=Strategy.REPLACE)

        resp_status_code, resp_content = ProbelyAPIClient.post(
            url=self.resource_url, query_params=query_params, payload=body_data
        )

        if resp_status_code == 400:
            raise ProbelyBadRequest(response_payload=resp_content)

        if resp_status_code != 201:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        target = self.model(deserialized_data)

        if api_schema_file_content:
            target = self._upload_api_schema_file(target.id, api_schema_file_content)

        return target

    def start_scan(
        self,
        target: Union[Target, str],
        extra_payload: Optional[Dict] = None,
    ) -> Scan:
        target_id = retrieve_entity_or_str_id(Target, target)

        scan_target_url = PROBELY_API_TARGETS_START_SCAN_URL.format(target_id=target_id)

        resp_status_code, resp_content = ProbelyAPIClient.post(
            scan_target_url, payload=extra_payload
        )

        if resp_status_code == 400:
            raise ProbelyBadRequest(resp_content)
        if resp_status_code == 404:
            raise ProbelyObjectsNotFound(target_id)
        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        deserialized_data = Scan.serializer_class(**resp_content)
        return Scan(deserialized_data)

    def bulk_start_scan(
        self,
        targets: List[Union[Target, str]],
        extra_payload: Optional[Dict] = None,
    ) -> List[Scan]:
        target_ids = retrieve_entity_or_str_ids(Target, targets)

        extra_payload = extra_payload or {}

        payload = {
            "targets": [{"id": target_id} for target_id in target_ids],
            **extra_payload,
        }

        resp_status_code, resp_content = ProbelyAPIClient.post(
            PROBELY_API_SCANS_BULK_START_URL,
            query_params={ID_404_VALIDATION: True},
            payload=payload,
        )

        validate_id_404_response(status_code=resp_status_code, content=resp_content)
        if resp_status_code == 400:
            raise ProbelyBadRequest(resp_content)
        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        scans = [Scan.serializer_class(**scan_content) for scan_content in resp_content]
        scans = [Scan(scan) for scan in scans]
        return scans


class FindingManager(RetrieveMixin, ListMixin, SdkBaseManager):
    resource_url = PROBELY_API_FINDINGS_URL
    resource_detail_url = PROBELY_API_FINDINGS_DETAIL_URL
    listing_ordering = "-last_found"
    model = Finding


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


class ScanManager(RetrieveMixin, ListMixin, SdkBaseManager):
    resource_url = PROBELY_API_SCANS_URL
    resource_detail_url = PROBELY_API_SCANS_DETAIL_URL
    model = Scan

    def _single_action(
        self,
        scan: Union[Scan, str],
        endpoint_template: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Scan:
        """
        Perform a single action (cancel, pause, resume) on a Scan.

        :param scan: The Scan object or scan ID.
        :param endpoint_template: The endpoint URL template with placeholders.
        :param payload: Optional payload for actions that require additional data.
        :return: The updated Scan object
        """

        if isinstance(scan, str):
            scan = self.retrieve({"id": scan})

        action_endpoint = endpoint_template.format(target_id=scan.target.id, id=scan.id)
        resp_status_code, resp_content = ProbelyAPIClient.post(
            action_endpoint, payload=payload
        )

        if resp_status_code == 404:
            raise ProbelyObjectsNotFound(scan.id)

        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content, resp_status_code)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)

    def _bulk_action(
        self,
        scans: List[Union[str, Scan]],
        bulk_action_url: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Generator[Scan, None, None]:
        """
        Perform a bulk action (cancel, pause, resume) on multiple scans.

        :param scans: A list of Scan objects or scan IDs.
        :param bulk_action_url: The bulk action endpoint URL.
        :param payload: Optional payload for actions that require additional data.
        :return: A list of updated Scan objects.
        """
        scan_ids = retrieve_entity_or_str_ids(Scan, scans)

        payload_data = {"scans": [{"id": scan_id} for scan_id in scan_ids]}

        if payload:
            payload_data.update(payload)

        resp_status_code, resp_content = ProbelyAPIClient.post(
            bulk_action_url,
            payload=payload_data,
            query_params={ID_404_VALIDATION: True},
        )

        validate_id_404_response(status_code=resp_status_code, content=resp_content)

        if resp_status_code != 200:
            raise ProbelyRequestFailed(resp_content)

        return self.retrieve_multiple(scan_ids)

    def cancel(self, scan: Union[Scan, str]) -> Scan:
        return self._single_action(scan, PROBELY_API_SCAN_CANCEL_URL_TEMPLATE)

    def pause(self, scan: Union[Scan, str]) -> Scan:
        return self._single_action(scan, PROBELY_API_SCAN_PAUSE_URL_TEMPLATE)

    def resume(
        self, scan: Union[Scan, str], ignore_blackout_period: bool = False
    ) -> Scan:
        return self._single_action(
            scan,
            PROBELY_API_SCAN_RESUME_URL_TEMPLATE,
            payload={"ignore_blackout_period": ignore_blackout_period},
        )

    def bulk_cancel(self, scans: List[Union[str, Scan]]) -> Generator[Scan, None, None]:
        return self._bulk_action(scans, PROBELY_API_SCANS_BULK_CANCEL_URL)

    def bulk_pause(self, scans: List[Union[str, Scan]]) -> Generator[Scan, None, None]:
        return self._bulk_action(scans, PROBELY_API_SCANS_BULK_PAUSE_URL)

    def bulk_resume(
        self,
        scans: List[Union[str, Scan]],
        ignore_blackout_period: bool = False,
    ) -> Generator[Scan, None, None]:
        return self._bulk_action(
            scans,
            PROBELY_API_SCANS_BULK_RESUME_URL,
            payload={
                "overrides": {"ignore_blackout_period": ignore_blackout_period},
            },
        )


class SequenceManager(
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


class ExtraHostManager(
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
