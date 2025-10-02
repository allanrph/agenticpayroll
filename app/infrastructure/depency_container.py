from app.adapters.outgoing.client.country_profile.country_profile_cilent import (
    CountryProfileClient,
)
from app.use_cases.calculate_payroll_use_case import CalculatePayrollUseCase
from app.adapters.llm.llm_client import GeminiLLMClient, LLMSettings
from app.adapters.llm.data_sources import (
    StaticEmployeeDataSource,
    StaticCountryRulesDataSource,
)
from app.adapters.llm.payroll_agent import PayrollCrewOrchestrator


def country_profile_client():
    return CountryProfileClient()


def get_calculate_payroll_use_case():
    return CalculatePayrollUseCase(
        country_profile_client=country_profile_client(),
    )


def get_llm_settings():
    return LLMSettings()


def get_llm_client():
    settings = get_llm_settings()
    return GeminiLLMClient(settings)


def get_employee_data_source():
    return StaticEmployeeDataSource()


def get_country_rules_data_source():
    return StaticCountryRulesDataSource()


def get_payroll_crew_orchestrator(
    employee_id: str,
    pay_period_start_date: str,
    pay_period_end_date: str,
    country_code: str,
):
    return PayrollCrewOrchestrator(
        employee_id=employee_id,
        pay_period_start_date=pay_period_start_date,
        pay_period_end_date=pay_period_end_date,
        country_code=country_code,
        llm_client=get_llm_client(),
        employee_data_source=get_employee_data_source(),
        country_rules_data_source=get_country_rules_data_source(),
    )
