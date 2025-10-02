from app.domains.employee import (
    ComprehensivePayrollRequest,
    TransactionEmployee,
    Transaction,
)
from app.use_cases.clients.country_profile_client import ICountryProfileClient
from app.use_cases.services.tax_calculation_service import (
    TaxCalculationService,
    TaxCalculation,
)
from app.domains.country_profile import CountryProfile
from typing import Dict, List


class CalculatePayrollUseCase:
    def __init__(self, country_profile_client: ICountryProfileClient):
        self.country_profile_client = country_profile_client
        self.tax_calculation_service = TaxCalculationService()

    def _get_employees_from_transactions(
        self, transactions: List[Transaction]
    ) -> Dict[str, TransactionEmployee]:
        """Create employee data structure for tax calculations from transactions."""
        if not transactions:
            raise ValueError("No transactions provided")

        employees = {}
        for transaction in transactions:
            if transaction.employee.id not in employees:
                employees[transaction.employee.id] = transaction.employee
        return employees

    def _calculate_payroll_for_employee(
        self,
        employees: Dict[str, TransactionEmployee],
        transactions: List[Transaction],
        country_profile: CountryProfile,
        payroll_request: ComprehensivePayrollRequest,
    ) -> List[Transaction]:
        """Calculate tax transactions for all employees."""
        all_tax_transactions = []

        for employee_id, employee in employees.items():
            # Get employee's transactions
            employee_transactions = [
                transaction
                for transaction in transactions
                if transaction.employee.id == employee_id
            ]

            # Calculate gross pay from earnings
            gross_pay = sum(
                transaction.amount
                for transaction in employee_transactions
                if transaction.payCode.type == "EARNINGS"
                and transaction.payCode.isTaxable
            )

            # Calculate taxes
            taxes = self._calculate_taxes(employee, gross_pay, country_profile)

            # Get currency from first transaction
            currency = (
                employee_transactions[0].currencySymbol
                if employee_transactions
                else "USD"
            )
            currency_code = (
                employee_transactions[0].currencyCode
                if employee_transactions
                else "USD"
            )

            # Create tax transactions
            tax_transactions = self._create_tax_transactions(
                employee, payroll_request, taxes, currency, currency_code
            )
            all_tax_transactions.extend(tax_transactions)

        return all_tax_transactions

    async def execute(self, data: ComprehensivePayrollRequest):
        """
        Execute comprehensive payroll processing using transaction-based calculations.

        This method processes payroll transactions, calculates taxes based on country
        profile rules, and creates new tax transactions for all calculated deductions.
        """
        # Validate input
        if not data.transactions:
            raise ValueError("No transactions provided for payroll calculation")

        # Get country configuration
        country_code = data.billingEntity.countryCode
        country_profile = await self._get_country_configuration(country_code)

        # Get employees from transactions
        employees = self._get_employees_from_transactions(data.transactions)

        # Create tax transactions
        tax_transactions = self._calculate_payroll_for_employee(
            employees, data.transactions, country_profile, data
        )
        return tax_transactions

    async def _get_country_configuration(self, country_code: str):
        """Get country profile configuration for tax calculations."""
        return await self.country_profile_client.get_country_profile_config(
            country_code
        )

    def _calculate_taxes(
        self,
        employee_data: TransactionEmployee,
        gross_pay: float,
        country_profile: CountryProfile,
    ) -> List[TaxCalculation]:
        """Calculate taxes using the tax calculation service."""
        return self.tax_calculation_service.calculate_taxes_from_earnings(
            employee_data, gross_pay, country_profile
        )

    def _create_tax_transactions(
        self,
        employee_data: TransactionEmployee,
        payroll_request: ComprehensivePayrollRequest,
        tax_calculations: List[TaxCalculation],
        employee_currency: str,
        employee_currency_code: str,
    ) -> List[Transaction]:
        """Create tax transactions using the tax calculation service."""
        return self.tax_calculation_service.create_tax_transactions(
            employee_data,
            payroll_request,
            tax_calculations,
            employee_currency,
            employee_currency_code,
        )
