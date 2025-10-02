import json
from typing import Dict, Any, List
from app.adapters.llm.data_sources import EMPLOYEE_DB, COUNTRY_RULES
from app.adapters.llm.llm_client_interface import ILLMClient
from app.domains.country_profile import CountryProfile
from app.domains.employee import Transaction, TransactionEmployee

# --- Base Agent for Crew ---


class AgentBase:
    """Base class for all specialized payroll agents in the Crew."""

    ROLE: str = "Base Payroll Agent"
    INSTRUCTIONS: str = "Perform the specified financial calculation."

    def __init__(self, data: Dict[str, Any], llm_client: ILLMClient):
        self.data = data
        self.llm_client = llm_client

    async def process(self) -> Dict[str, Any]:
        """Runs the specific LLM process for this agent's role."""
        return await self.llm_client.run_crew_agent(
            self.ROLE, self.INSTRUCTIONS, self.data
        )


# --- Specialized Agents (The Crew) ---


class GrossPayAgent(AgentBase):
    """Calculates all earnings and determines the Gross Salary Base for contributions."""

    ROLE = "Gross Pay Calculator Agent"
    INSTRUCTIONS = """
    1. Determine the Gross Salary subject to IESS
    2. Determine the taxable salary.
    3. Add results to the 'Calculated_Components' dictionary.
    """


class TaxAgent(AgentBase):
    """Calculates both Employee and Employer IESS Contributions."""

    ROLE = "General Tax Agent Expert"
    INSTRUCTIONS = """
    1. Analiza el bloque de codigo que te enviare en el parametro data.
    2. Evalua que tipo de informacion necesitas de la informacion del payroll enviada
    3. Ejecuta el bloque de codigo que te enviare en el parametro instructions.
    4. Retorna el resultado de la ejecucion del bloque de codigo.
    """


class IncomeTaxAgent(AgentBase):
    """Calculates the Employee Income Tax (Retención en la Fuente)."""

    ROLE = "Income Tax Agent (SRI Expert)"
    INSTRUCTIONS = """
    1. Determine the correct bracket for the given anual taxable income in the tax table.
    3. Calculate the Tax having the right bracket for the taxable income.
    4. Divide the Tax by 12 to get the Monthly Taxes Retention.
    5. If the projected income is below the taxable threshold, the result must be 0.00.
    6. Add the result to 'Calculated_Components'.
    """


class NetPayAndFormatterAgent(AgentBase):
    """Calculates the final Net Pay and formats the output into required groupings."""

    ROLE = "Net Pay and Final Formatter Agent"
    INSTRUCTIONS = """
    1. SUM all components in 'Calculated_Components' to determine Total Earnings and Total Deductions.
    2. Calculate the net payment for the employee.
    3. Calculate the total costs for the employeer.
    5. IMPORTANT: Generate a detailed step-by-step list explaining how Gross Base, Overtime, IESS Deduction, and Income Tax were derived (add here the applicable_bracket and calculations). Store this list in a new key called 'Calculation_Trace'.
    4. Group all components into the final required output structure:
       - Earnings for the Employee
       - Deductions for the Employee
       - Taxes charged to the Employee
       - Taxes charged to the Employer
       - Net payment for the Employee
    5. Return the full structured JSON output.
    """


# --- Data Collector Agent (Agent 1) ---


class DataCollectorAgent:
    """
    Agent 1: Responsible for I/O and data consolidation with dependency injection.
    """

    def __init__(
        self,
        employee_id: str,
        country_code: str,
        employee_data_source,
    ):
        self.employee_id = employee_id
        self.country_code = country_code
        self.employee_data_source = employee_data_source

    async def collect_data(
        self,
        country_profile: CountryProfile,
        transactions: List[Transaction],
        employee_data: TransactionEmployee,
    ):
        """Collect and consolidate data from various sources."""
        employee_data = await self.employee_data_source.get_employee_data(
            self.employee_id
        )
        calculable_paycodes = country_profile.paycodes

        # Initialize the state dictionary with necessary raw data and rules
        consolidated_data = {
            "employee": employee_data,
            "country_code": self.country_code,
            "calculable_paycodes": calculable_paycodes,
            "tax_table": country_profile.tax_table,
            "Calculated_Components": {},  # Container for sequential results
        }
        return consolidated_data


# --- Payroll Crew Orchestrator (Flow Manager) ---


class PayrollCrewOrchestrator:
    """
    Agent Flow Manager: Coordinates the execution of the sequence of specialized agents.
    """

    def __init__(
        self,
        llm_client: ILLMClient,
    ):
        self.llm_client = llm_client

    async def run_payroll(
        self,
        employee: TransactionEmployee,
        country_profile: CountryProfile,
        transactions: List[Transaction],
    ):
        """Executes the payroll process sequentially through the crew."""

        # 1. Data Collection (Non-LLM Agent)
        collector = DataCollectorAgent()
        payroll_state = await collector.collect_data(
            employee, country_profile, transactions
        )

        # 2. Sequential Processing by the Crew (LLM Agents)
        print("Orchestrator: Starting Crew Model Processing...")
        calculable_paycodes = country_profile.paycodes
        crew_sequence = [GrossPayAgent]
        for paycode in calculable_paycodes:
            crew_sequence.append(TaxAgent)
        crew_sequence.append(IncomeTaxAgent)
        ##        crew_sequence.append(NetPayAndFormatterAgent)

        for agent_class in crew_sequence:
            agent = agent_class(payroll_state, self.llm_client)
            print(f"  -> Executing {agent.ROLE}...")

            # The agent modifies the state and returns the updated state
            payroll_state = await agent.process()

            if "error" in payroll_state:
                return json.dumps(
                    {
                        "status": "Failed",
                        "stage": agent.ROLE,
                        "error": payroll_state["error"],
                    },
                    indent=4,
                )

        return {
            "paycodeId": 457,
        }
