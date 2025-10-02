"""
Payroll Breakdown Service

This service handles the creation of comprehensive payroll breakdowns
with earnings, deductions, taxes, and employer costs.
"""

from typing import Dict, List, Any, Tuple
from app.domains.employee import Transaction


class PayrollBreakdownService:
    """Service responsible for building comprehensive payroll breakdowns."""

    def build_comprehensive_breakdown(
        self,
        earnings_total: float,
        earnings_breakdown: Dict[str, float],
        earnings_grouped: Dict[str, Dict[str, float]],
        deductions_total: float,
        deductions_breakdown: Dict[str, float],
        deductions_grouped: Dict[str, Dict[str, float]],
        taxes_total: float,
        taxes_breakdown: Dict[str, float],
        taxes_grouped: Dict[str, Dict[str, float]],
        gross_pay: float,
        total_deductions: float,
        net_pay: float,
        employer_contributions: Dict[str, float],
        total_employer_cost: float,
        payroll_request,
        tax_calculations: Dict[str, Any],
        original_transaction_count: int,
        calculated_tax_transaction_count: int,
    ) -> Dict[str, Any]:
        """
        Build a comprehensive payroll breakdown with all calculated values.

        Args:
            earnings_total: Total earnings amount
            earnings_breakdown: Breakdown of earnings by pay code
            earnings_grouped: Earnings grouped by parent pay code
            deductions_total: Total deductions amount
            deductions_breakdown: Breakdown of deductions by pay code
            deductions_grouped: Deductions grouped by parent pay code
            taxes_total: Total taxes amount
            taxes_breakdown: Breakdown of taxes by pay code
            taxes_grouped: Taxes grouped by parent pay code
            gross_pay: Total gross pay
            total_deductions: Total deductions including taxes
            net_pay: Net pay after all deductions
            employer_contributions: Employer contribution breakdown
            total_employer_cost: Total employer cost
            payroll_request: Original payroll request for metadata
            tax_calculations: Detailed tax calculation results
            original_transaction_count: Number of original transactions
            calculated_tax_transaction_count: Number of calculated tax transactions

        Returns:
            Comprehensive breakdown dictionary
        """
        return {
            # Earnings breakdown
            "earnings_breakdown": self._round_dict_values(earnings_breakdown),
            "earnings_grouped_by_parent": self._round_grouped_values(earnings_grouped),
            # Deductions breakdown
            "deductions_breakdown": self._round_dict_values(deductions_breakdown),
            "deductions_grouped_by_parent": self._round_grouped_values(
                deductions_grouped
            ),
            # Taxes breakdown
            "taxes_breakdown": self._round_dict_values(taxes_breakdown),
            "taxes_grouped_by_parent": self._round_grouped_values(taxes_grouped),
            # Summary amounts
            "gross_pay": round(gross_pay, 2),
            "total_deductions": round(total_deductions, 2),
            "net_pay": round(net_pay, 2),
            # Employer costs
            "employer_costs": self._round_dict_values(employer_contributions),
            "total_employer_cost": round(total_employer_cost, 2),
            # Payroll metadata
            "pay_period_start": payroll_request.payPeriodStart,
            "pay_period_end": payroll_request.payPeriodEnd,
            "pay_date": payroll_request.payDate,
            "due_date": payroll_request.dueDate,
            "payroll_id": payroll_request.id,
            "status": payroll_request.status,
            "transaction_count": original_transaction_count,
            "calculated_tax_transactions": calculated_tax_transaction_count,
            # Tax calculation details
            "tax_calculation_details": {
                "taxable_income": tax_calculations["taxable_income"],
                "tax_exemptions_applied": tax_calculations["tax_exemptions_applied"],
                "income_tax": tax_calculations["income_tax"],
                "social_security": tax_calculations["social_security"],
                "health_insurance": tax_calculations["health_insurance"],
                "solidarity_fund": tax_calculations["solidarity_fund"],
                "tax_bracket_details": tax_calculations["tax_bracket_details"],
            },
        }

    def _round_dict_values(self, data_dict: Dict[str, float]) -> Dict[str, float]:
        """Round all values in a dictionary to 2 decimal places."""
        return {k: round(v, 2) for k, v in data_dict.items()}

    def _round_grouped_values(
        self, grouped_data: Dict[str, Dict[str, float]]
    ) -> Dict[str, Dict[str, float]]:
        """Round all values in grouped data to 2 decimal places."""
        return {
            parent: {k: round(v, 2) for k, v in children.items()}
            for parent, children in grouped_data.items()
        }
