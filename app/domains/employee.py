from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime

from app.domains.country_profile import CountryPayCode


class CompanyMetadata(BaseModel):
    id: str
    company_name: str
    address: Optional[str] = None
    logo_url: Optional[str] = None


class EmployeeMetadata(BaseModel):
    full_name: str
    job_title: Optional[str] = None
    department: Optional[str] = None
    tax_id: Optional[str] = None
    bank_account_last4: Optional[str] = None


class BenefitsOptIn(BaseModel):
    private_pension: Optional[bool] = False
    health_insurance_top_up: Optional[bool] = False
    meal_subsidy: Optional[bool] = False


class Employee(BaseModel):
    tenant_id: str
    employee_id: str
    country: str
    gross_salary: float
    hourly_rate: float
    hours_worked: float
    overtime_hours: Optional[float] = 0.0
    bonuses: Optional[float] = 0.0
    allowances: Optional[Dict[str, float]] = {}
    benefits_opt_in: Optional[BenefitsOptIn] = BenefitsOptIn()
    metadata: Optional[EmployeeMetadata] = None


# New comprehensive models based on payroll_transactions.json structure


class Company(BaseModel):
    id: str
    name: str
    createdAt: datetime
    updatedAt: datetime


class BillingEntity(BaseModel):
    id: str
    name: str
    countryCode: str
    countryName: str
    localCurrency: str
    payDate: str
    createdAt: datetime
    updatedAt: datetime


class CompanyEntity(BaseModel):
    id: str
    legalName: str
    countryId: str
    billingEntityId: str
    createdAt: datetime
    updatedAt: datetime


class PayCode(BaseModel):
    id: str
    countryIso2: str
    name: str
    description: str
    type: str  # EARNINGS, DEDUCTIONS, etc.
    parentPayCodeId: Optional[str] = None
    parentPayCode: Optional[str] = None
    frequency: str  # RECURRING, ONE_TIME, etc.
    assignToSolution: bool = False
    billingClassificationId: Optional[str] = None
    billingClassification: Optional[str] = None
    payrollClassificationId: Optional[str] = None
    payrollClassification: Optional[str] = None
    applicableRegion: str  # COUNTRY_WIDE, etc.
    locations: List[str] = []
    solutions: List[str] = []
    glCodeId: Optional[str] = None
    glCode: Optional[str] = None
    taxPayer: Optional[str] = None
    taxType: Optional[str] = None
    isPremiumPay: bool = False
    isTaxable: bool = True
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()

    @classmethod
    def from_country_paycode(cls, country_paycode: CountryPayCode):
        return cls(
            id=country_paycode.id,
            countryIso2=country_paycode.countryIso2,
            name=country_paycode.name,
            description=country_paycode.description,
            type=country_paycode.type,
            parentPayCodeId=country_paycode.parentPayCodeId,
            parentPayCode=(
                str(country_paycode.parentPayCode.value)
                if country_paycode.parentPayCode
                else None
            ),
            frequency=country_paycode.frequency,
            assignToSolution=country_paycode.assignToSolution,
            billingClassificationId=country_paycode.billingClassificationId,
            billingClassification=(
                str(country_paycode.billingClassification.billingClassificationName)
                if country_paycode.billingClassification
                else None
            ),
            payrollClassificationId=country_paycode.payrollClassificationId,
            payrollClassification=(
                str(country_paycode.payrollClassification.value)
                if country_paycode.payrollClassification
                else None
            ),
            applicableRegion=country_paycode.applicableRegion,
            locations=country_paycode.locations,
            solutions=(
                [str(solution.solutionId) for solution in country_paycode.solutions]
                if country_paycode.solutions
                else []
            ),
            glCodeId=country_paycode.glCodeId,
            glCode=country_paycode.glCodeId,
            taxPayer=country_paycode.taxPayer,
            taxType=country_paycode.taxType,
            isPremiumPay=(
                country_paycode.isPremiumPay
                if country_paycode.isPremiumPay is not None
                else False
            ),
            isTaxable=(
                country_paycode.isTaxable
                if country_paycode.isTaxable is not None
                else True
            ),
        )


class TransactionEmployee(BaseModel):
    id: str
    userId: Optional[str] = None
    firstName: str
    lastName: str
    status: str
    email: str
    stateProvince: str
    profilePicture: str = ""
    payrollFiles: List[str] = []
    company: Optional[str] = None
    createdAt: datetime
    updatedAt: datetime


class Transaction(BaseModel):
    employee: TransactionEmployee
    payCode: PayCode
    amount: float
    currencySymbol: str
    currencyCode: str
    type: str  # REGULAR, etc.
    workedHours: float
    hourlyRate: float
    billingEntityCurrencyCode: str
    billingEntityCurrencyExchangeRate: float
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()


# Legacy PayrollRequest for backward compatibility
class PayrollRequest(BaseModel):
    employee: Employee
    company: Optional[CompanyMetadata] = None


# New comprehensive PayrollRequest based on payroll_transactions.json structure
class ComprehensivePayrollRequest(BaseModel):
    id: str
    status: str  # AWAITING_FUNDS, etc.
    type: str  # regular, etc.
    reRunCount: int = 0
    payPeriodStart: str
    payPeriodEnd: str
    company: Company
    billingEntity: BillingEntity
    companyEntity: CompanyEntity
    rejectionReasons: List[str] = []
    transactions: List[Transaction]
    previousPayrollRun: Optional[str] = None
    total: float
    dueDate: str
    payDate: str
    hasPayrollFilesReport: bool = False
    employeePayrollSummaries: List[Dict] = []
    invoicePayrollID: Optional[str] = None
    solutionType: Optional[str] = None
