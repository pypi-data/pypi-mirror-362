from typing import Union, Generator, List, Optional, Dict

from probely.sdk.managers.common import SdkBaseManager
from probely.settings import (
    PROBELY_API_FINDINGS_DETAIL_URL,
    PROBELY_API_FINDINGS_URL,
)
from probely.sdk.models import Finding
from probely.sdk.managers.mixins.list import ListMixin
from probely.sdk.managers.mixins.retrieve import RetrieveByIDMixin
from probely.sdk.managers.mixins.retrieve_multiple import RetrieveMultipleMixin


class FindingManager(
    RetrieveByIDMixin, RetrieveMultipleMixin, ListMixin, SdkBaseManager
):
    resource_url = PROBELY_API_FINDINGS_URL
    resource_detail_url = PROBELY_API_FINDINGS_DETAIL_URL
    listing_ordering = "-last_found"
    model = Finding

    def list(self, filters: Optional[Dict] = None) -> Generator[Finding, None, None]:
        # TODO: add accepted filter
        return self._list(filters=filters, ordering=self.listing_ordering)

    def retrieve_multiple(
        self, findings_or_id: List[Union[Finding, str]]
    ) -> Generator[Finding, None, None]:
        return self._retrieve_multiple(findings_or_id)

    def retrieve(self, finding_or_id: Union[Finding, str]) -> Finding:
        return self._retrieve_by_id(finding_or_id)
