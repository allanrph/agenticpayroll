import json
import os
from typing import Dict, Any, List

from app.domains.country_profile import (
    CountryProfile,
    CountryPayCode,
    ParentPayCode,
    BillingClassification,
    Solution,
    PayrollClassification,
    TaxBracket,
)
from app.infrastructure.HttpClientBase import HttpClientBase
from app.use_cases.clients.country_profile_client import ICountryProfileClient

ECUADOR_DETAILED_TAX_BRACKETS = [
    # Exempt income
    TaxBracket(from_amount=0.0, up_to=11200.0, rate=0.0, fixed=0.0),
    # 5% bracket
    TaxBracket(from_amount=11200.01, up_to=14400.0, rate=0.05, fixed=0.0),
    # 10% bracket
    TaxBracket(from_amount=14400.01, up_to=18000.0, rate=0.10, fixed=160.0),
    # 12% bracket
    TaxBracket(from_amount=18000.01, up_to=21600.0, rate=0.12, fixed=520.0),
    # 15% bracket
    TaxBracket(from_amount=21600.01, up_to=24000.0, rate=0.15, fixed=952.0),
    # 20% bracket
    TaxBracket(from_amount=24000.01, up_to=27600.0, rate=0.20, fixed=1312.0),
    # 25% bracket
    TaxBracket(from_amount=27600.01, up_to=36000.0, rate=0.25, fixed=2024.0),
    # 30% bracket
    TaxBracket(from_amount=36000.01, up_to=48000.0, rate=0.30, fixed=3134.0),
    # 35% bracket
    TaxBracket(from_amount=48000.01, up_to=60000.0, rate=0.35, fixed=6734.0),
    # 37% bracket (highest)
    TaxBracket(from_amount=60000.01, up_to=None, rate=0.37, fixed=10934.0),
]


class CountryProfileClient(HttpClientBase, ICountryProfileClient):
    BASE_URL = os.environ.get(
        "COUNTRY_PROFILE_API_URL", "https://api.countryprofile.com"
    )

    def __init__(self):
        super().__init__()
        # Use absolute path to the calculable paycodes file
        self.paycodes_path = (
            "/Users/allanrp/Develop/agenticpayroll/tests/calculable_paycodes.json"
        )
        print(f"DEBUG: Paycodes path: {self.paycodes_path}")
        print(f"DEBUG: File exists: {os.path.exists(self.paycodes_path)}")
        self._paycodes_cache: Dict[str, List[CountryPayCode]] = {}

    def _load_calculable_paycodes(self) -> List[Dict[str, Any]]:
        """Load calculable paycodes from JSON file"""
        with open(self.paycodes_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _get_paycodes_for_country(self, country_code: str) -> List[CountryPayCode]:
        """Get paycodes for a specific country"""
        if country_code in self._paycodes_cache:
            return self._paycodes_cache[country_code]

        paycodes_data = self._load_calculable_paycodes()
        country_paycodes = [
            paycode
            for paycode in paycodes_data
            if paycode.get("countryIso2") == country_code
        ]

        parsed_paycodes = self._parse_calculable_paycodes(country_paycodes)
        self._paycodes_cache[country_code] = parsed_paycodes

        return parsed_paycodes

    def _parse_calculable_paycodes(self, paycodes_data: list) -> list:
        """Parse calculable paycodes from JSON data"""
        return [
            CountryPayCode(
                id=paycode["id"],
                countryIso2=paycode["countryIso2"],
                name=paycode["name"],
                description=paycode["description"],
                type=paycode["type"],
                parentPayCodeId=paycode.get("parentPayCodeId"),
                parentPayCode=(
                    ParentPayCode(
                        id=paycode["parentPayCode"]["id"],
                        value=paycode["parentPayCode"]["value"],
                        payCodeType=paycode["parentPayCode"]["payCodeType"],
                    )
                    if paycode.get("parentPayCode")
                    else None
                ),
                frequency=paycode["frequency"],
                assignToSolution=paycode["assignToSolution"],
                billingClassificationId=paycode.get("billingClassificationId"),
                payrollClassificationId=paycode["payrollClassificationId"],
                applicableRegion=paycode["applicableRegion"],
                locations=paycode["locations"],
                solutions=[
                    Solution(
                        id=solution["id"],
                        solutionId=solution["solutionId"],
                        paymentBy=solution["paymentBy"],
                        billingClassification=BillingClassification(
                            billingClassificationCode=solution["billingClassification"][
                                "billingClassificationCode"
                            ],
                            billingClassificationName=solution["billingClassification"][
                                "billingClassificationName"
                            ],
                            billingClassificationAccountName=solution[
                                "billingClassification"
                            ]["billingClassificationAccountName"],
                            billingClassificationAccountNumber=solution[
                                "billingClassification"
                            ]["billingClassificationAccountNumber"],
                        ),
                        glCodeId=solution["glCodeId"],
                    )
                    for solution in paycode["solutions"]
                ],
                taxPayer=paycode["taxPayer"],
                taxType=paycode.get("taxType"),
                isPremiumPay=paycode.get("isPremiumPay"),
                isTaxable=paycode.get("isTaxable"),
                payrollClassification=PayrollClassification(
                    id=paycode["payrollClassification"]["id"],
                    value=paycode["payrollClassification"]["value"],
                    payCodeType=paycode["payrollClassification"]["payCodeType"],
                ),
                billingClassification=BillingClassification(
                    billingClassificationCode=paycode["billingClassification"][
                        "billingClassificationCode"
                    ],
                    billingClassificationName=paycode["billingClassification"][
                        "billingClassificationName"
                    ],
                    billingClassificationAccountName=paycode["billingClassification"][
                        "billingClassificationAccountName"
                    ],
                    billingClassificationAccountNumber=paycode["billingClassification"][
                        "billingClassificationAccountNumber"
                    ],
                ),
                glCodeId=paycode["glCodeId"],
                calculationFormula=paycode["calculationFormula"],
                calculationCodeBlock=paycode["calculationCodeBlock"],
            )
            for paycode in paycodes_data
        ]

    async def get_country_profile_config(self, country_code: str) -> CountryProfile:
        """Get country profile configuration from API and merge with paycodes"""
        # url = f"/country/{country_code}/profile"
        # response = await self.request("GET", url)
        # country_profile = CountryProfile(**response.json())

        # Add paycodes from separate JSON file
        country_profile = CountryProfile()
        country_profile.paycodes = self._get_paycodes_for_country(country_code)
        country_profile.tax_table = ECUADOR_DETAILED_TAX_BRACKETS
        return country_profile
