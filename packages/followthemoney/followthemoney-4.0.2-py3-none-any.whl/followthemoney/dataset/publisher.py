from typing import Optional

from pydantic import BaseModel

from followthemoney.dataset.util import CountryCode, Url
from followthemoney.types import registry


class DataPublisher(BaseModel):
    """Publisher information, eg. the government authority."""

    name: str
    url: Optional[Url] = None
    name_en: Optional[str] = None
    acronym: Optional[str] = None
    description: Optional[str] = None
    country: Optional[CountryCode] = None
    official: Optional[bool] = False
    logo_url: Optional[Url] = None

    @property
    def country_label(self) -> Optional[str]:
        if self.country is None:
            return None
        return registry.country.caption(self.country)
