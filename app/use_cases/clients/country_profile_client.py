from abc import ABC

from app.domains.country_profile import CountryProfile


class ICountryProfileClient(ABC):
    async def get_country_profile_config(self, country_code: str) -> CountryProfile:
        pass