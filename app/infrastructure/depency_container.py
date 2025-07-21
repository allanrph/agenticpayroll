from fastapi import Depends
from app.adapters.outgoing.client.country_profile.country_profile_cilent import CountryProfileClient
from app.use_cases.calculate_payroll_use_case import CalculatePayrollUseCase


def country_profile_client():
    return CountryProfileClient()

def get_calculate_payroll_use_case():
    return CalculatePayrollUseCase(country_profile_client = Depends(country_profile_client))

