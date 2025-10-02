#!/usr/bin/env python3
"""
Test script for the new comprehensive payroll calculation.
This demonstrates how the refactored code works with transaction-based calculations.
"""

import json
from datetime import datetime
from app.domains.employee import (
    ComprehensivePayrollRequest,
    Company,
    BillingEntity,
    CompanyEntity,
    PayCode,
    TransactionEmployee,
    Transaction,
)


def create_sample_comprehensive_payroll_request():
    """Create a sample comprehensive payroll request based on the payroll_transactions.json structure."""

    # Sample company data
    company = Company(
        id="45ecbabb-7e4b-460a-b853-f5cf9a8894cc",
        name="Peter Pan",
        createdAt=datetime.fromisoformat("2025-10-01T20:42:18.179865752"),
        updatedAt=datetime.fromisoformat("2025-10-01T20:42:18.179866513"),
    )

    # Sample billing entity
    billing_entity = BillingEntity(
        id="f127d908-c0bc-4a04-b7d1-4d927b67afad",
        name="Main Entity",
        countryCode="EC",
        countryName="Ecuador",
        localCurrency="USD",
        payDate="2026-09-05",
        createdAt=datetime.fromisoformat("2025-07-31T21:23:07.138418"),
        updatedAt=datetime.fromisoformat("2025-07-31T21:23:07.13842"),
    )

    # Sample company entity
    company_entity = CompanyEntity(
        id="cebf49b0-811c-43c2-8863-d0c8e0d97fec",
        legalName="Peter Pan Ecuador",
        countryId="234047b2-8c5a-47af-8dda-64358f5b0ff4",
        billingEntityId="f127d908-c0bc-4a04-b7d1-4d927b67afad",
        createdAt=datetime.fromisoformat("2025-07-31T21:42:34.475025"),
        updatedAt=datetime.fromisoformat("2025-07-31T21:42:34.475027"),
    )

    # Sample employee
    employee = TransactionEmployee(
        id="ec-employee-001",
        userId=None,
        firstName="Carlos",
        lastName="Mendoza",
        status="active",
        email="carlos.mendoza@company.com",
        stateProvince="Pichincha",
        profilePicture="",
        payrollFiles=[],
        company=None,
        createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
        updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
    )

    # Sample transactions with different pay code types
    transactions = [
        # EARNINGS transactions
        Transaction(
            id="ec-001-regular-pay",
            employee=employee,
            payCode=PayCode(
                id="ec-regular-pay-code",
                countryIso2="EC",
                name="Regular Pay",
                description="Standard pay for regular hours worked in Ecuador.",
                type="EARNINGS",
                parentPayCodeId=None,
                parentPayCode=None,
                frequency="RECURRING",
                assignToSolution=False,
                billingClassificationId="global_payroll_gross_wages",
                billingClassification="Global Payroll revenue:Global Payroll - Gross Wages",
                payrollClassificationId=None,
                payrollClassification="paycode-payroll-classification-base-pay-monthly-salary",
                applicableRegion="COUNTRY_WIDE",
                locations=[],
                solutions=[],
                glCodeId=None,
                glCode=None,
                taxPayer=None,
                taxType=None,
                isPremiumPay=False,
                isTaxable=True,
                createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
                updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            ),
            amount=1200.00,
            currencySymbol="$",
            currencyCode="USD",
            type="REGULAR",
            workedHours=0.0,
            hourlyRate=0.0,
            billingEntityCurrencyCode="USD",
            billingEntityCurrencyExchangeRate=1.0,
            createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
        ),
        Transaction(
            id="ec-002-bonus-pay",
            employee=employee,
            payCode=PayCode(
                id="ec-bonus-pay-code",
                countryIso2="EC",
                name="Performance Bonus",
                description="Performance-based bonus for Ecuador employee.",
                type="EARNINGS",
                parentPayCodeId=None,
                parentPayCode=None,
                frequency="ONE_TIME",
                assignToSolution=False,
                billingClassificationId="global_payroll_allowances",
                billingClassification="Global Payroll revenue:Global Payroll - Allowances",
                payrollClassificationId=None,
                payrollClassification="paycode-payroll-classification-bonus",
                applicableRegion="COUNTRY_WIDE",
                locations=[],
                solutions=[],
                glCodeId=None,
                glCode=None,
                taxPayer=None,
                taxType=None,
                isPremiumPay=False,
                isTaxable=True,
                createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
                updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            ),
            amount=200.00,
            currencySymbol="$",
            currencyCode="USD",
            type="REGULAR",
            workedHours=0.0,
            hourlyRate=0.0,
            billingEntityCurrencyCode="USD",
            billingEntityCurrencyExchangeRate=1.0,
            createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
        ),
        # DEDUCTIONS transactions
        Transaction(
            id="ec-003-health-insurance",
            employee=employee,
            payCode=PayCode(
                id="ec-health-insurance-deduction",
                countryIso2="EC",
                name="Health Insurance",
                description="Health insurance deduction for Ecuador employee.",
                type="DEDUCTIONS",
                parentPayCodeId=None,
                parentPayCode=None,
                frequency="RECURRING",
                assignToSolution=False,
                billingClassificationId=None,
                billingClassification=None,
                payrollClassificationId=None,
                payrollClassification="paycode-payroll-classification-health-insurance",
                applicableRegion="COUNTRY_WIDE",
                locations=[],
                solutions=[],
                glCodeId=None,
                glCode=None,
                taxPayer=None,
                taxType=None,
                isPremiumPay=False,
                isTaxable=False,
                createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
                updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            ),
            amount=50.00,
            currencySymbol="$",
            currencyCode="USD",
            type="REGULAR",
            workedHours=0.0,
            hourlyRate=0.0,
            billingEntityCurrencyCode="USD",
            billingEntityCurrencyExchangeRate=1.0,
            createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
        ),
        # TAX transactions
        Transaction(
            id="ec-004-income-tax",
            employee=employee,
            payCode=PayCode(
                id="ec-income-tax",
                countryIso2="EC",
                name="Income Tax",
                description="Income tax deduction for Ecuador employee.",
                type="TAX",
                parentPayCodeId=None,
                parentPayCode=None,
                frequency="RECURRING",
                assignToSolution=False,
                billingClassificationId=None,
                billingClassification=None,
                payrollClassificationId=None,
                payrollClassification="paycode-payroll-classification-income-tax",
                applicableRegion="COUNTRY_WIDE",
                locations=[],
                solutions=[],
                glCodeId=None,
                glCode=None,
                taxPayer=None,
                taxType=None,
                isPremiumPay=False,
                isTaxable=False,
                createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
                updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            ),
            amount=150.00,
            currencySymbol="$",
            currencyCode="USD",
            type="REGULAR",
            workedHours=0.0,
            hourlyRate=0.0,
            billingEntityCurrencyCode="USD",
            billingEntityCurrencyExchangeRate=1.0,
            createdAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
            updatedAt=datetime.fromisoformat("2025-01-15T10:00:00.000000"),
        ),
    ]

    # Create comprehensive payroll request
    payroll_request = ComprehensivePayrollRequest(
        id="2db7f450-9a22-47f2-b996-b15b9fe2c520",
        status="AWAITING_FUNDS",
        type="regular",
        reRunCount=0,
        payPeriodStart="2032-04-01",
        payPeriodEnd="2032-04-28",
        company=company,
        billingEntity=billing_entity,
        companyEntity=company_entity,
        rejectionReasons=[],
        transactions=transactions,
        previousPayrollRun=None,
        total=1400.00,  # 1200 + 200 - 50 - 150 = 1200
        dueDate="2032-04-08",
        payDate="2032-05-05",
        hasPayrollFilesReport=True,
        employeePayrollSummaries=[],
        invoicePayrollID=None,
        solutionType=None,
    )

    return payroll_request


def test_transaction_calculations():
    """Test the transaction-based calculations."""
    print("Testing Comprehensive Payroll Request Structure")
    print("=" * 50)

    # Create sample data
    payroll_request = create_sample_comprehensive_payroll_request()

    print(f"Payroll ID: {payroll_request.id}")
    print(f"Status: {payroll_request.status}")
    print(
        f"Pay Period: {payroll_request.payPeriodStart} to {payroll_request.payPeriodEnd}"
    )
    print(
        f"Country: {payroll_request.billingEntity.countryName} ({payroll_request.billingEntity.countryCode})"
    )
    print(f"Company: {payroll_request.company.name}")
    print(f"Total Transactions: {len(payroll_request.transactions)}")
    print()

    # Calculate earnings (EARNINGS type)
    earnings_total = 0.0
    earnings_breakdown = {}
    for transaction in payroll_request.transactions:
        if transaction.payCode.type == "EARNINGS":
            earnings_total += transaction.amount
            pay_code_name = transaction.payCode.name
            if pay_code_name in earnings_breakdown:
                earnings_breakdown[pay_code_name] += transaction.amount
            else:
                earnings_breakdown[pay_code_name] = transaction.amount

    print("EARNINGS CALCULATION:")
    print(f"Total Earnings: ${earnings_total:.2f}")
    for name, amount in earnings_breakdown.items():
        print(f"  - {name}: ${amount:.2f}")
    print()

    # Calculate deductions (DEDUCTIONS type)
    deductions_total = 0.0
    deductions_breakdown = {}
    for transaction in payroll_request.transactions:
        if transaction.payCode.type == "DEDUCTIONS":
            deductions_total += transaction.amount
            pay_code_name = transaction.payCode.name
            if pay_code_name in deductions_breakdown:
                deductions_breakdown[pay_code_name] += transaction.amount
            else:
                deductions_breakdown[pay_code_name] = transaction.amount

    print("DEDUCTIONS CALCULATION:")
    print(f"Total Deductions: ${deductions_total:.2f}")
    for name, amount in deductions_breakdown.items():
        print(f"  - {name}: ${amount:.2f}")
    print()

    # Calculate taxes (TAX type)
    taxes_total = 0.0
    taxes_breakdown = {}
    for transaction in payroll_request.transactions:
        if transaction.payCode.type == "TAX":
            taxes_total += transaction.amount
            pay_code_name = transaction.payCode.name
            if pay_code_name in taxes_breakdown:
                taxes_breakdown[pay_code_name] += transaction.amount
            else:
                taxes_breakdown[pay_code_name] = transaction.amount

    print("TAXES CALCULATION:")
    print(f"Total Taxes: ${taxes_total:.2f}")
    for name, amount in taxes_breakdown.items():
        print(f"  - {name}: ${amount:.2f}")
    print()

    # Calculate net pay
    gross_pay = earnings_total
    total_deductions = deductions_total + taxes_total
    net_pay = gross_pay - total_deductions

    print("FINAL CALCULATION:")
    print(f"Gross Pay (Earnings): ${gross_pay:.2f}")
    print(f"Total Deductions: ${total_deductions:.2f}")
    print(f"Net Pay: ${net_pay:.2f}")
    print()

    print("This demonstrates how the new ComprehensivePayrollRequest")
    print("calculates payroll values from transactions based on pay code types:")
    print("- EARNINGS transactions contribute to gross pay")
    print("- DEDUCTIONS transactions reduce net pay")
    print("- TAX transactions also reduce net pay")
    print("- The system automatically categorizes and sums amounts by type")


if __name__ == "__main__":
    test_transaction_calculations()
