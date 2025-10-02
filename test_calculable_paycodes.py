#!/usr/bin/env python3
"""
Test the calculable paycodes implementation.
"""

import json
import asyncio
from app.use_cases.calculate_payroll_use_case import CalculatePayrollUseCase
from app.use_cases.services.deductions_service import DeductionsService
from app.use_cases.services.employer_costs_service import CalculateEmployerCostsService
from app.use_cases.clients.country_profile_client import ICountryProfileClient
from app.use_cases.clients.payroll_client import IPayrollClient


class MockCountryProfileClient(ICountryProfileClient):
    async def get_country_profile_config(self, country_code: str):
        # Load the actual calculable paycodes from the JSON file
        if country_code == "EC":
            from app.domains.country_profile import CountryProfile
            from app.adapters.outgoing.client.country_profile.country_profile_cilent import (
                CountryProfileClient,
            )

            # Use the real client to load calculable paycodes
            real_client = CountryProfileClient()
            return await real_client.get_country_profile_config(country_code)
        return None


class MockPayrollClient(IPayrollClient):
    async def update_payroll_run(self, company_id: str, breakdown: dict):
        return {"id": f"payroll-{company_id}-calculable"}


async def test_calculable_paycodes():
    """Test the calculable paycodes implementation."""

    # Load sample data
    with open(
        "/Users/allanrp/Develop/agenticpayroll/sample_comprehensive_payroll_request.json",
        "r",
    ) as f:
        payroll_data = json.load(f)

    # Initialize services
    country_client = MockCountryProfileClient()
    payroll_client = MockPayrollClient()
    deductions_service = DeductionsService()
    employer_costs_service = CalculateEmployerCostsService()

    # Initialize use case
    use_case = CalculatePayrollUseCase(
        country_profile_client=country_client,
    )

    # Convert to Pydantic model
    from app.domains.employee import ComprehensivePayrollRequest

    payroll_request = ComprehensivePayrollRequest(**payroll_data)

    print("🧮 Testing Calculable Paycodes Implementation")
    print("=" * 50)
    print(f"Input transactions: {len(payroll_request.transactions)}")

    # Execute payroll calculation
    result = await use_case.execute(payroll_request)

    print(f"\n📊 Results:")
    print(f"Type: {type(result)}")
    print(f"Number of tax transactions: {len(result)}")

    for i, transaction in enumerate(result):
        print(f"\n  Transaction {i+1}:")
        print(f"    ID: {transaction.id}")
        print(f"    PayCode: {transaction.payCode.name}")
        print(f"    Amount: ${transaction.amount:,.2f}")
        print(f"    Tax Payer: {transaction.payCode.taxPayer}")
        print(f"    Description: {transaction.payCode.description}")

    return result


if __name__ == "__main__":
    asyncio.run(test_calculable_paycodes())
