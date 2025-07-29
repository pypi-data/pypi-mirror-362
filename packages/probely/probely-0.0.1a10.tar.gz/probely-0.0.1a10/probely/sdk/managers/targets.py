from datetime import datetime
from io import BytesIO
from typing import Dict, Generator, List, Union, Optional

import yaml
from mergedeep import Strategy, merge

from probely.exceptions import (
    ProbelyBadRequest,
    ProbelyObjectsNotFound,
    ProbelyRequestFailed,
    ProbelyValidation,
)

from probely import TargetAPISchemaTypeEnum, TargetTypeEnum
from probely.constants import ID_404_VALIDATION
from probely.sdk.managers.base_manager import SdkBaseManager
from probely.settings import (
    PROBELY_API_SCANS_BULK_START_URL,
    PROBELY_API_TARGETS_BULK_DELETE_URL,
    PROBELY_API_TARGETS_BULK_UPDATE_URL,
    PROBELY_API_TARGETS_DETAIL_URL,
    PROBELY_API_TARGETS_START_SCAN_URL,
    PROBELY_API_TARGETS_UPLOAD_API_SCHEMA_FILE_URL,
    PROBELY_API_TARGETS_URL,
)
from probely.sdk.client import ProbelyAPIClient
from probely.sdk.helpers import (
    retrieve_entity_or_str_id,
    retrieve_entity_or_str_ids,
    validate_id_404_response,
)
from probely.sdk.managers.mixins import (
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    UpdateMixin,
)
from probely.sdk.models import Scan, Target


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
