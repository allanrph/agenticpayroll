from app.domains.employee import PayrollRequest
from app.use_cases.clients.country_profile_client import ICountryProfileClient
from app.use_cases.clients.payroll_client import IPayrollClient
from app.use_cases.services.benefits_service import BenefitsService
from app.use_cases.services.deductions_service import DeductionsService
from app.use_cases.services.employer_costs_service import CalculateEmployerCostsService
from app.use_cases.services.gross_pay_service import GrossPayService
from app.use_cases.services.payslip import generate_payslip

class CalculatePayrollUseCase:
    def __init__(
            self,
            country_profile_client: ICountryProfileClient,
            payroll_client: IPayrollClient,
            gross_pay_service: GrossPayService,
            deductions_service: DeductionsService,
            benefits_service: BenefitsService,
            employer_costs_service: CalculateEmployerCostsService
    ):
        self.country_profile_client = country_profile_client
        self.payroll_client = payroll_client
        self.gross_pay_service = gross_pay_service
        self.deductions_service = deductions_service
        self.benefits_service = benefits_service
        self.employer_costs_service = employer_costs_service

    async def execute(self, data: PayrollRequest):
        employee = data.employee
        company = data.company

        config = await self.country_profile_client.get_country_profile_config(employee.country)
        print(f'Looking for: {employee.country}')

        # 1. Gross Pay and Allowances
        gross_pay, base_pay, overtime_pay, allowances_breakdown = self.gross_pay_service.calculate_gross_pay(employee)

        # 2. Deductions (with tax exemptions support)
        deductions = self.deductions_service.calculate_deductions(employee, gross_pay, config)

        # 3. Benefits
        country_benefits = self.benefits_service.calculate_country_specific_benefits(gross_pay, config)
        total_benefit_deductions = country_benefits['employee_total']
        total_benefit_employer = country_benefits['employer_total']

        # 4. Add benefit deductions
        total_deductions = deductions['total_deductions'] + total_benefit_deductions
        net_pay = gross_pay - total_deductions

        # 5. Employer Costs
        base_employer_cost, employer_contributions = self.employer_costs_service.calculate_employer_costs(gross_pay, employee.country)
        total_employer_cost = base_employer_cost + total_benefit_employer

        # 6. Build breakdown
        breakdown = {
            'base_pay': round(base_pay, 2),
            'overtime_pay': round(overtime_pay, 2),
            'allowances_breakdown': {k: round(v, 2) for k, v in allowances_breakdown.items()},
            'gross_pay': round(gross_pay, 2),
            'taxable_income': deductions['taxable_income'],
            'tax_exemptions_applied': deductions['tax_exemptions_applied'],
            'income_tax': deductions['income_tax'],
            'social_security': deductions['social_security'],
            'health_insurance': deductions['health_insurance'],
            'solidarity_fund': deductions['solidarity_fund'],
            'total_deductions': round(total_deductions, 2),
            'net_pay': round(net_pay, 2),
            'employer_costs': {k: round(v, 2) for k, v in employer_contributions.items()},
            'total_employer_cost': round(total_employer_cost, 2),
            'tax_bracket_details': deductions['tax_bracket_details'],
            'country_specific_benefits': country_benefits,
            'pay_period': 'March 2025',
            'pay_type': 'Monthly',
            'benefits_deductions': {
                'pre_tax': deductions['pre_tax_breakdown'],
                'post_tax': deductions['post_tax_breakdown'],
                'total_pre_tax': deductions['total_pre_tax_deductions'],
                'total_post_tax': deductions['total_post_tax_deductions']
            }
        }

        # 7. Generate Payslip
        payslip_path = generate_payslip(employee, breakdown, net_pay, {'total_employer_cost': total_employer_cost},
                                        company)

        # 8. Persist
        record = await self.payroll_client.update_payroll_run(company.id, breakdown)

        return {
            'net_pay': net_pay,
            'gross_pay': gross_pay,
            'total_employer_cost': total_employer_cost,
            'breakdown': breakdown,
            'payslip_url': f'/payslip/{record["id"]}'
        }
