from dataclasses import dataclass
from typing import List, Dict, Optional, Any


@dataclass
class TaxBracket:
    from_amount: Optional[float] = None
    up_to: Optional[float]
    rate: float
    fixed: Optional[float] = None


@dataclass
class EmployerContributions:
    social_security_employer: float
    health_insurance_employer: float
    occupational_risk_employer: float
    family_compensation_fund: float
    icbf: float
    sena: float


@dataclass
class CountrySpecificBenefit:
    name: str
    description: Optional[str] = None
    employee_rate: Optional[float] = None
    employer_rate: Optional[float] = None
    eligible: Optional[bool] = None
    exemption_rule: Optional[str] = None


@dataclass
class BenefitsOptInOption:
    employee_rate: Optional[float] = None
    employer_rate: Optional[float] = None
    employee_fixed: Optional[float] = None
    employer_fixed: Optional[float] = None
    pre_tax: Optional[bool] = None


@dataclass
class TaxExemption:
    type: str
    rate: Optional[float] = None
    amount: Optional[float] = None


@dataclass
class ParentPayCode:
    id: str
    value: str
    payCodeType: str


@dataclass
class BillingClassification:
    billingClassificationCode: str
    billingClassificationName: str
    billingClassificationAccountName: str
    billingClassificationAccountNumber: str


@dataclass
class Solution:
    id: str
    solutionId: str
    paymentBy: str
    billingClassification: BillingClassification
    glCodeId: str


@dataclass
class PayrollClassification:
    id: str
    value: str
    payCodeType: str


@dataclass
class CountryPayCode:
    id: str
    countryIso2: str
    name: str
    description: str
    type: str
    parentPayCodeId: Optional[str]
    parentPayCode: Optional[ParentPayCode]
    frequency: str
    assignToSolution: bool
    billingClassificationId: Optional[str]
    payrollClassificationId: str
    applicableRegion: str
    locations: list
    solutions: List[Solution]
    taxPayer: str
    taxType: Optional[str]
    isPremiumPay: Optional[bool]
    isTaxable: Optional[bool]
    payrollClassification: PayrollClassification
    billingClassification: BillingClassification
    glCodeId: str
    calculationFormula: str
    calculationCodeBlock: str


@dataclass
class CountryProfile:
    # Paycodes
    paycodes: Optional[List[CountryPayCode]] = None
    tax_table: Optional[List[TaxBracket]] = None
