"""
Tax Calculation Service

This service handles the calculation and creation of tax transactions
based on calculable paycodes from country profile and employee earnings.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from app.domains.employee import Transaction, PayCode, TransactionEmployee
from app.domains.country_profile import CountryPayCode, CountryProfile


@dataclass
class TaxCalculation:
    """Represents a calculated tax with its associated paycode and amount."""

    paycode: CountryPayCode
    amount: float


@dataclass
class PayrollCalculationResult:
    """Represents the result of payroll calculation for an employee."""

    employee_id: str
    gross_pay: float
    tax_calculations: List[TaxCalculation]
    currency: str
    currency_code: str


class TaxCalculationService:
    """Service responsible for calculating taxes and creating tax transactions."""

    def __init__(self):
        pass

    def calculate_taxes_from_earnings(
        self,
        employee_data: TransactionEmployee,
        gross_pay: float,
        country_profile: CountryProfile,
    ) -> List[TaxCalculation]:
        """Calculate taxes from employee earnings using country profile paycodes."""
        tax_calculations = []

        # Find calculable tax paycodes
        er_iess = next(
            (x for x in country_profile.paycodes if x.name == "ER-IESS"), None
        )
        ee_iess = next(
            (x for x in country_profile.paycodes if x.name == "EE-IESS"), None
        )

        # Calculate ER-IESS (Employer contribution)
        if er_iess:
            tax_calculations.append(
                TaxCalculation(
                    paycode=er_iess,
                    amount=gross_pay * 0.1125,  # 11.25%
                )
            )

        # Calculate EE-IESS (Employee contribution)
        if ee_iess:
            tax_calculations.append(
                TaxCalculation(
                    paycode=ee_iess,
                    amount=gross_pay * 0.0945,  # 9.45%
                )
            )

        return tax_calculations

    def create_tax_transactions(
        self,
        employee_data: TransactionEmployee,
        payroll_request,
        tax_calculations: List[TaxCalculation],
        employee_currency: str,
        employee_currency_code: str,
    ) -> List[Transaction]:
        """Create tax transaction objects from calculated taxes."""
        tax_transactions = []
        for tax_calculation in tax_calculations:
            tax_transactions.append(
                self._create_tax_transaction(
                    employee_data,
                    payroll_request,
                    tax_calculation.amount,
                    tax_calculation.paycode,
                    employee_currency,
                    employee_currency_code,
                )
            )
        return tax_transactions

    def _create_tax_transaction(
        self,
        employee_data: TransactionEmployee,
        payroll_request,
        amount: float,
        paycode: CountryPayCode,
        employeeCurrency: str,
        employeeCurrencyCode: str,
    ) -> Transaction:
        return Transaction(
            employee=employee_data,
            payCode=PayCode.from_country_paycode(paycode),
            amount=amount,
            currencySymbol=employeeCurrency,
            currencyCode=employeeCurrencyCode,
            type="REGULAR",
            workedHours=0.0,
            hourlyRate=0.0,
            billingEntityCurrencyCode=payroll_request.billingEntity.localCurrency,
            billingEntityCurrencyExchangeRate=1.0,
        )
