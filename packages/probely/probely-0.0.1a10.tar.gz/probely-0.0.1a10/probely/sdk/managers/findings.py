from probely.sdk.managers.base_manager import SdkBaseManager
from probely.settings import (
    PROBELY_API_FINDINGS_DETAIL_URL,
    PROBELY_API_FINDINGS_URL,
)
from probely.sdk.managers.mixins import ListMixin, RetrieveMixin
from probely.sdk.models import Finding


class FindingManager(RetrieveMixin, ListMixin, SdkBaseManager):
    resource_url = PROBELY_API_FINDINGS_URL
    resource_detail_url = PROBELY_API_FINDINGS_DETAIL_URL
    listing_ordering = "-last_found"
    model = Finding
