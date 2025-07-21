import os

from app.domains.country_profile import CountryProfile
from app.infrastructure.HttpClientBase import HttpClientBase
from app.use_cases.clients.country_profile_client import ICountryProfileClient


class CountryProfileClient(HttpClientBase, ICountryProfileClient):
    BASE_URL = os.environ.get('COUNTRY_PROFILE_API_URL', 'https://api.countryprofile.com')

    async def get_country_profile_config(self, country_code):
        url = f'/country/{country_code}/profile'
        response = await self.request('GET', url)
        return CountryProfile(**response.json())
